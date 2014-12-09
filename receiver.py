import socket
import sys
from packet import *
from setting import *


if len(sys.argv) != 2:
    print("usage: python agent.py filename")
    exit()
else:
    filename = sys.argv[1]
    print("write to file {0}".format(filename))


class Reciever:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(SENDER_ADDRESS)
        self.file_write = open(filename)
        self.target_addr = AGENT_ADDRESS
        self.seq = 0

    def start(self):
        pass

    def ack(self, n):
        ack_pkt = create_ack()
        self.sock.sendto(bytes())
