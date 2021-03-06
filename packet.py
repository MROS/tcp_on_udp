import pickle


class Packet:
    def __init__(self, content):
        self.content = content

    def to_binary(self):
        return pickle.dumps(self.content)


def parse_packet(s):
    return Packet(pickle.loads(s))


def create_ack(ack):
    return Packet({"ack": ack})


def create_packet(seq, data):
    return Packet({"seq": seq, "data": data})

FIN = Packet({"seq": "fin"})
FIN_ACK = Packet({"ack": "fin"})


def is_finack(pkt):
    return "ack" in pkt.content and pkt.content["ack"] == "fin"


def is_fin(pkt):
    return "seq" in pkt.content and pkt.content["seq"] == "fin"


def is_ack(pkt):
    return "ack" in pkt.content


def is_data(pkt):
    return "data" in pkt.content
