import random
import id_gen

limit_enums = {
    "data": [
        "5GB", "8GB", "10GB", "15GB", "unlimited"
    ],
    "wifi": [
        "30h", "50h", "100h", "200h", "unlimited"
    ],
    "sms": [
        "100", "300", "500", "800"
    ],
    "voice": [
        "10h", "18h", "24h", "48h", "unlimited"
    ]
}

def random_choose_from(list):
    return list[random.randrange(len(list))]

class Cfss:
    def __init__(self, limit, reference_id):
        self.id = id_gen.UUID1.get()
        self.rev_id = id_gen.UUID1.get()
        self.limit = limit
        self.reference_id = reference_id
    def __str__(self):
        return str(self.__dict__)
    def __hash__(self):
        return hash(("Cfss", self.limit, self.reference_id)) 
    def to_record(self, operator, tags, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": self.id,
            "operator_name": operator,
            "psr_type": 2,
            "revision_id": self.rev_id,
            "name": "cfss",
            "description": self.limit,
            "properties": {
                "limit": self.limit
            },            
            "tags": tags
        }
        return rec     

class CfssGen:
    @staticmethod
    def gen(rfss_list):
        result = set()
        for rfss in rfss_list:
            for i in range(random.randrange(2, 4)):
                limit = random_choose_from(limit_enums[rfss.type])
                result.add(Cfss(limit, rfss.id))
        return result

# import resource_spec_gen
# test_set = resource_spec_gen.ResousceSpecGen.gen("infra")
# import rfss_gen
# rfss_l = rfss_gen.RfssGen.gen(test_set)

# cfss_set = CfssGen.gen(rfss_l)
# for i in cfss_set:
#     print(i)
        