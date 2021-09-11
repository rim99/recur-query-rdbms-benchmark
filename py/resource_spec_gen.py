import random
import id_gen
import json

companies = {
    "infra": [
        "huawei", "nokia", "sismens", "ericsson"
    ],
    "app": [
         "netflix", "HBO max", "tubi", "hulu", "syfy"
    ]
}

infra_type = [
   "data", "wifi", "sms", "voice" 
]

choices = {
    "data": [
        "5G", "4G"
    ],
    "wifi": [
        "150Mbps", "300Mbps", "450Mbps", "800Mbps"
    ],
    "sms": [
        "5G", "4G"
    ],
    "voice": [
        "volte", "nr", "csfb"
    ]
}

def random_choose_from(list):
    return list[random.randrange(len(list))]

class ResourceSpec:
    def __init__(self, type, company, subtype = None, choice = None):
        self.id = id_gen.UUID1.get()
        self.rev_id = id_gen.UUID1.get()
        self.type = type
        self.company = company
        self.subtype = subtype
        self.choice = choice
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other):
        return self.__dict__ == other.__dict__   
    def __hash__(self):
        return hash(("ResourceSpec", self.type, self.company, self.subtype, self.choice))     
    def to_mysql_record(self, operator, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": self.id.bytes,
            "operator_name": operator,
            "psr_type": 0,
            "revision_id": self.rev_id.bytes,
            "name": self.subtype,
            "description": self.choice,
            "properties": json.dumps({
                "company": self.company,
                "service": self.subtype,
                "tech_solution": self.choice
            })            
        }
        return rec
    def to_pg_record(self, operator, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": str(self.id),
            "operator_name": operator,
            "psr_type": 0,
            "revision_id": str(self.rev_id),
            "name": self.subtype,
            "description": self.choice,
            "properties": json.dumps({
                "company": self.company,
                "service": self.subtype,
                "tech_solution": self.choice
            })            
        }
        return rec    

class ResousceSpecGen:
    @staticmethod
    def gen(type):
        result = set()
        company = random_choose_from(companies[type])
        if type == "infra":
            for subtype in infra_type:
                for i in range(random.randrange(2, 4)):
                    choice = random_choose_from(choices[subtype])
                    result.add(ResourceSpec(type, company, subtype, choice))
        else:
            for i in range(random.randrange(3, 4)):
                result.add(ResourceSpec(type, company, "app", "online service"))
        return result


