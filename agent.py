import setting
import packet
import socket
import random
import sys
# import time
import json


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
        print("agent bind on {0}".format(setting.AGENT_PORT))
        self.output = open("/tmp/output", "wb")

    def shutdown(self):
        self.output.close()
        self.sock.close()

    def start(self):
        transfer = 0
        total = 0
        while True:
            (raw_data, recv) = self.sock.recvfrom(BUF_SIZE)
            pkt = packet.parse_packet(raw_data)
            if "fin" in pkt.content:
                self.shutdown()
                break
            self.output.write(pkt.content["data"])
            total += 1; transfer += 1
            print("get data #{0}".format(transfer))
            if random.random() < drop_rate:
                print("drop data #{0}, loss rate #{1}".format(transfer, (total - transfer) / total))
                transfer -= 1
            else:
                print("forward data #{0}, loss rate #{1}".format(transfer, (total - transfer) / total))
                # agent.sendto()

Agent().start()

