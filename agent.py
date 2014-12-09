import setting
import packet
import socket
import random
import sys
# import time
import json

# TODO: bytes, string conversion may cause problem?

BUF_SIZE = setting.DATA_SIZE * 2

if len(sys.argv) != 2:
    print("usage: python agent.py drop_rate")
    exit()
else:
    drop_rate = float(sys.argv[1])
print("drop rate is {0}".format(drop_rate))

agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
agent.bind(('localhost', setting.AGENT_PORT))
print("agent bind on {0}".format(setting.AGENT_PORT))

transfer = 0
total = 0
while True:
    (raw_data, recv) = agent.recvfrom(BUF_SIZE)
    pkt = packet.Packet(json.loads(raw_data.decode("utf-8")))
    print(pkt.content)
    total += 1
    transfer += 1
    print("get data #{0}".format(transfer))
    if random.random() < drop_rate:
        print("drop data #{0}, loss rate #{1}".format(transfer, (total - transfer) / total))
        transfer -= 1
    else:
        print("forward data #{0}, loss rate #{1}".format(transfer, (total - transfer) / total))
    # agent.sendto()
