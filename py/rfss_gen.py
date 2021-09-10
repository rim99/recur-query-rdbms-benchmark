import random
import id_gen



class Rfss:
    def __init__(self, type, choice, reference):
        self.id = id_gen.UUID1.get()
        self.rev_id = id_gen.UUID1.get()
        self.type = type
        self.choice = choice
        self.reference = reference
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other):
        return (self.type, self.choice, tuple(self.reference)) == (other.type, other.choice, tuple(other.reference))
    def __hash__(self):
        return hash(("Rfss", self.type, self.choice, tuple(self.reference)))     
    def to_record(self, operator, tags, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": self.id,
            "operator_name": operator,
            "psr_type": 1,
            "revision_id": self.rev_id,
            "name": self.type,
            "description": self.choice,
            "properties": {
                "service": self.type,
                "tech_solution": self.choice
            },            
            "tags": tags
        }
        return rec    

class RfssGen:
    @staticmethod
    def gen(resource_specs):
        # only infra resource spec can be passed in
        agg = dict()
        for r in resource_specs:
            key = (r.subtype, r.choice)
            v = agg.get(key, [])
            v.append(r.id)
            agg[key] = v
        result = []
        for k in agg:
            result.append(Rfss(k[0], k[1], agg[k]))    
        return result
        
        
# import resource_spec_gen
# test_set = resource_spec_gen.ResousceSpecGen.gen("infra")
# res = RfssGen.gen(test_set)
# for i in res:
#     print(i)