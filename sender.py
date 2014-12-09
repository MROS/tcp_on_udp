import socket
import sys
from setting import *
from packet import *

threshold = 16
receiver_buf = 32

if len(sys.argv) != 2:
    print("usage: python agent.py filename")
    exit()
else:
    filename = sys.argv[1]
    print("file {0} to be send".format(filename))


class Sender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(SENDER_ADDRESS)
        self.file = open(filename)
        self.target_addr = AGENT_ADDRESS
        self.seq = 0

    def start(self):
        data = self.file.read(DATA_SIZE)
        while data != '':
            to_send = create_packet(self.seq, data).to_s()
            self.sock.sendto(bytes(to_send, "utf-8"), AGENT_ADDRESS)

            data = self.file.read(DATA_SIZE)

Sender().start()
