import socket
import sys
from setting import *
from packet import *

threshold = 16

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
        self.file = open(filename, "rb")
        self.threshold = threshold
        self.window_size = 1
        self.data_sent = 0
        self.seq = 0

    def start(self):
        data = self.file.read(DATA_SIZE)
        while data != b'':
            to_send = create_packet(self.seq, data).to_binary()
            self.sock.sendto(to_send, AGENT_ADDRESS)
            self.data_sent += 1
            print("send data #{0}".format(self.data_sent))

            data = self.file.read(DATA_SIZE)
        self.sock.sendto(FIN.to_binary(), AGENT_ADDRESS)

Sender().start()
