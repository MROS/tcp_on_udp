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
        print("agent bind on {0}".format(setting.AGENT_PORT))

    def shutdown(self):
        self.sock.close()

    def drop_rate(self):
        return (self.data_get - self.data_transfer) / self.data_get

    def handle_data(self, raw_data):
        self.data_get += 1
        print("get data #{0}".format(self.data_transfer + 1))
        if random.random() < drop_rate:
            print("drop data #{0}, loss rate #{1}".format(self.data_transfer + 1, self.drop_rate()))
        else:
            self.data_transfer += 1
            self.sock.sendto(raw_data, setting.RECEIVER_ADDRESS)
            print("forward data #{0}, loss rate #{1}".format(self.data_transfer, self.drop_rate()))

    def handle_ack(self, raw_data):
        print("-------------- handle ack ----------------")
        self.ack_num += 1
        print("get ack #{0}".format(self.ack_num))
        self.sock.sendto(raw_data, setting.SENDER_ADDRESS)
        print("forward ack #{0}".format(self.ack_num))

    def start(self):
        while True:
            (raw_data, recv) = self.sock.recvfrom(BUF_SIZE)
            pkt = parse_packet(raw_data)
            if is_ack(pkt):
                self.handle_ack(raw_data)
            else:
                # include fin and data
                self.handle_data(raw_data)

Agent().start()

