import json


class Packet:
    def __init__(self, content):
        self.content = content
    def to_s(self):
        return json.dumps(self.content)


def parse_packet(s):
    return json.loads(s)


def create_ack(seq, ack):
    return Packet({"seq": seq, "ack": ack})


def create_packet(seq, data):
    return Packet({"seq": seq, "data": data})
