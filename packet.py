import pickle


class Packet:
    def __init__(self, content):
        self.content = content

    def to_binary(self):
        return pickle.dumps(self.content)


def parse_packet(s):
    return Packet(pickle.loads(s))


def create_ack(seq, ack):
    return Packet({"seq": seq, "ack": ack})


def create_packet(seq, data):
    return Packet({"seq": seq, "data": data})

FIN = Packet({"fin": True})
