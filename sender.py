import socket
import select
import sys
from setting import *
from packet import *
import threading
import time

# 投機取巧一次讀取整個檔案到buffer好了

retransmit_time = 10**(-3)
threshold = 16

if len(sys.argv) != 2:
    print("usage: python agent.py filename")
    exit()
else:
    filename = sys.argv[1]
    print("file {0} to be send".format(filename))


class CongestionWindow:
    def __init__(self, buf):
        self.size = 1
        self.threshold = threshold
        self.leftmost = 0
        self.buf = buf

    # leftmost 有包含， rightmost 沒包含
    def rightmost(self):
        return min(self.leftmost + self.size, len(self.buf))

    def contain(self, n):
        return self.leftmost <= n <= self.rightmost()

    def available_data(self):
        return self.buf[self.leftmost:self.rightmost()]

    def decrease(self):
        (self.threshold, _) = divmod(self.size, 2)
        self.size = 1
        return self.available_data()

    def inc_size(self):
        if self.size < self.threshold:
            self.size *= 2
        else:
            self.size += 1

    def increase(self):
        old_right = self.rightmost()
        self.inc_size()
        return self.buf[old_right:self.rightmost()]

    def increase_then_pop(self):
        old_right = self.rightmost()
        self.inc_size()
        self.leftmost += 1
        return self.buf[old_right:self.rightmost()]


class Sender:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(SENDER_ADDRESS)
        self.lock = threading.Lock()

        buf = []
        file = open(filename, "rb")
        data = file.read(DATA_SIZE)
        count = 0
        while data != b'':
            count += 1
            buf.append(create_packet(count, data))
            data = file.read(DATA_SIZE)
        file.close()

        self.window = CongestionWindow(buf)
        print("file read, total {0} packet".format(len(buf)))

    def send_data(self, buf):
        if buf == []:
            return False
        print("send from {0} to {1}".format(buf[0].content["seq"], buf[-1].content["seq"]))
        for pkt in buf:
            self.sock.sendto(pkt.to_binary(), AGENT_ADDRESS)
        return True

    def read_a_pkt(self):
        (raw_data, _) = self.sock.recvfrom(DATA_SIZE * 2)
        return parse_packet(raw_data)

    def timeout(self):
        print("time out")
        return self.window.decrease()

    def parse_ack(self, ack):
        print("recv ack #{0}".format(ack))
        print("leftmost = {0}".format(self.window.leftmost))
        if self.window.leftmost + 1 == ack == len(self.window.buf):
            return "finish"
        elif ack == self.window.leftmost + 1:
            return "leftmost"
        return "normal"

    def finish(self):
        # 假設 ack 一定送到
        self.sock.sendto(FIN.to_binary(), AGENT_ADDRESS)
        time_remain = retransmit_time
        while True:
            start = time.time()
            if time_remain > 0:
                (avai, _, _) = select.select([self.sock], [], [], time_remain)
            if avai == [] or time_remain <= 0:
                print("fin timeout")
                self.sock.sendto(FIN.to_binary(), AGENT_ADDRESS)
                time_remain = retransmit_time
            else:
                pkt = self.read_a_pkt()
                if is_finack(pkt):
                    break
                else:
                    time_remain -= (time.time() - start)

        self.sock.close()

    def start(self):
        time_remain = retransmit_time
        res = self.send_data(self.window.available_data())
        if not res:
            return

        while True:
            if time_remain > 0:
                start = time.time()
                (avai, _, _) = select.select([self.sock], [], [], time_remain)
                time_remain -= (time.time() - start)
                print("time remain {0}".format(time_remain))
                start = time.time()

            # 將 self.sock 讀乾淨

            if not avai or time_remain <= 0:
                # time out
                buf = self.timeout()
                self.send_data(buf)
                time_remain = retransmit_time
            else:
                pkt = self.read_a_pkt()
                ack = pkt.content["ack"]
                r = self.parse_ack(ack)
                if r == "finish":
                    print("finish")
                    self.finish()
                    break
                elif r == "leftmost":
                    print("hit leftmost")
                    buf = self.window.increase_then_pop()
                    self.send_data(buf)
                    time_remain = retransmit_time
                else:
                    buf = self.window.increase()
                    self.send_data(buf)
                    time_remain -= (time.time() - start)

                (avai, _, _) = select.select([self.sock], [], [], 0)


Sender().start()
