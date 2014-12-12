import socket
from packet import *
from setting import *

DEFAULT_BUF = 32


class Buffer:
    def __init__(self):
        self.SIZE = 16
        self.data = [None] * self.SIZE
        self.base = 1
        # self.index = 1

    def is_full(self):
        # print(self.data)
        for i in self.data:
            if i == None:
                return False
        return True

    def right(self):
        return self.base + self.SIZE

    def flush(self):
        self.data = [None] * self.SIZE
        self.base += self.SIZE

    def push(self, pkt):
        seq = pkt.content["seq"]
        # print("push {0}".format(seq))
        if self.base <= seq < self.right() and self.data[seq - self.base] == None:
            self.data[seq - self.base] = pkt
            return True
        return False

    def is_exceed(self, seq):
        return seq >= self.right()


class Reciever:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(RECEIVER_ADDRESS)
        self.target_addr = AGENT_ADDRESS
        self.output = open("/tmp/output", "wb")
        self.data_get = 0
        self.buffer = Buffer()

    def shutdown(self):
        self.flush()
        self.sock.close()
        self.output.close()

    def send_fin_ack(self):
        self.sock.sendto(FIN_ACK.to_binary(), AGENT_ADDRESS)
        print("send fin ack")

    def flush(self):
        # full 之後才能呼叫
        for i in self.buffer.data:
            if i == None:
                break
            data = i.content["data"]
            self.output.write(data)

        self.buffer.flush()
        print("flush")

    def send_ack(self, seq):
        ack_pkt = create_ack(seq)
        self.sock.sendto(ack_pkt.to_binary(), self.target_addr)

    def handle_data(self, pkt):
        seq = pkt.content["seq"]
        if self.buffer.is_exceed(seq):
            print("drop data #{0}".format(seq))
            if self.buffer.is_full():
                self.flush()
        elif not self.buffer.is_exceed(seq):
            res = self.buffer.push(pkt)
            self.send_ack(seq)
            print("send ack #{0}".format(seq))
            if not res:
                print("ignore data #{0}".format(seq))

    def start(self):
        while True:
            (raw_data, _) = self.sock.recvfrom(DATA_SIZE * 2)
            pkt = parse_packet(raw_data)
            if is_fin(pkt):
                print("recv fin")
                self.send_fin_ack()
                self.shutdown()
                break
            else:
                print("recv data #{0}".format(pkt.content["seq"]))
                self.handle_data(pkt)

Reciever().start()