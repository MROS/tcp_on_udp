import setting
from packet import *
import socket
import random
import sys

BUF_SIZE = setting.DATA_SIZE * 2

if len(sys.argv) != 2:
    print("usage: python agent.py drop_rate")
    exit()
else:
    drop_rate = float(sys.argv[1])
    print("drop rate is {0}".format(drop_rate))


class Agent:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', setting.AGENT_PORT))
        self.data_get = 0
        self.data_transfer = 0
        self.ack_num = 0
        self.last_seq = 0
        print("agent bind on {0}".format(setting.AGENT_PORT))

    def shutdown(self):
        self.sock.close()

    def drop_rate(self):
        return (self.data_get - self.data_transfer) / self.data_get

    def handle_data(self, pkt):
        self.data_get += 1
        seq = pkt.content["seq"]
        if self.last_seq.__class__.__name__ == "int" and self.last_seq + 1 != seq:
            print("not in order")
        self.last_seq = seq
        print("get data #{0}".format(seq))
        if random.random() < drop_rate:
            print("drop data #{0}, loss rate #{1}".format(seq, self.drop_rate()))
        else:
            self.data_transfer += 1
            self.sock.sendto(pkt.to_binary(), setting.RECEIVER_ADDRESS)
            print("forward data #{0}, loss rate #{1}".format(seq, self.drop_rate()))

    def handle_ack(self, pkt):
        print("-------------- handle ack ----------------")
        self.ack_num += 1
        print("get ack #{0}".format(pkt.content["ack"]))
        self.sock.sendto(pkt.to_binary(), setting.SENDER_ADDRESS)
        print("forward ack #{0}".format(pkt.content["ack"]))

    def start(self):
        while True:
            (raw_data, recv) = self.sock.recvfrom(BUF_SIZE)
            pkt = parse_packet(raw_data)
            if is_ack(pkt):
                self.handle_ack(pkt)
            else:
                # include fin and data
                self.handle_data(pkt)


Agent().start()
