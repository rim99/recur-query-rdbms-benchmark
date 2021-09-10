import uuid
import random

nodes = [random.getrandbits(48) for i in range(8)]
class UUID1:    
    @staticmethod
    def get():
        index = random.randint(0, 7)
        node = nodes[index]
        return uuid.uuid1(node)