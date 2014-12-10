import socket
from packet import *
from setting import *

DEFAULT_BUF = 32


# if len(sys.argv) != 2:
#     print("usage: python agent.py filename")
#     exit()
# else:
#     filename = sys.argv[1]
#     print("write to file {0}".format(filename))


class Reciever:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(RECEIVER_ADDRESS)
        self.target_addr = AGENT_ADDRESS
        self.output = open("/tmp/output", "wb")
        self.data_get = 0

    def shutdown(self):
        self.sock.close()
        self.output.close()

    def start(self):
        while True:
            (raw_data, recv) = self.sock.recvfrom(DATA_SIZE * 2)
            self.data_get += 1
            print("recv data #{0}".format(self.data_get))
            pkt = parse_packet(raw_data)
            if "fin" in pkt.content:
                self.shutdown()
                break
            self.output.write(pkt.content["data"])
            self.ack_back(pkt)

    def ack_back(self, pkt):
        seq = pkt.content["seq"]
        ack_pkt = create_ack(seq)
        self.sock.sendto(ack_pkt.to_binary(), self.target_addr)
        print("send ack #{0}".format(self.data_get))

Reciever().start()