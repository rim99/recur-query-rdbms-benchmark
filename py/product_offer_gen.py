import random
import id_gen


class ProductOffer:
    def __init__(self, product_spec_ids):
        self.id = id_gen.UUID1.get()
        self.rev_id = id_gen.UUID1.get()
        self.product_spec_ids = product_spec_ids
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other):
        return self.product_spec_ids == other.product_spec_ids
    def __hash__(self):
        return hash(("ProductOffer", self.product_spec_ids))     
    def to_mysql_record(self, operator, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": self.id.bytes,
            "operator_name": operator,
            "psr_type": 4,
            "revision_id": self.rev_id.bytes,
            "name": "product_offering",
            "description": "for test",
            "properties": "{}"            
        }
        return rec         
    def to_pg_record(self, operator, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": str(self.id),
            "operator_name": operator,
            "psr_type": 4,
            "revision_id": str(self.rev_id),
            "name": "product_offering",
            "description": "for test",
            "properties": "{}"            
        }
        return rec    

def random_ps(pl_tuple, minN = 5, maxN = 50):
    pl_l = len(pl_tuple)
    indices = set()
    for i in range(minN, maxN):
        j = random.randrange(pl_l)
        indices.add(j)
    r = [pl_tuple[i].id for i in indices]
    r.sort
    return r

class ProductOfferGen:
    @staticmethod
    def gen(product_spec_l, number = 2000):
        result_set = set()
        for i in range(number):
            self_ps = random_ps(product_spec_l["infra"]) 
            apps = random_ps(product_spec_l["app"], 0, 4)
            self_ps += apps
            po = ProductOffer(tuple(self_ps))
            result_set.add(po) 
        return result_set
            


# import resource_spec_gen
# test_set = resource_spec_gen.ResousceSpecGen.gen("infra")
# import rfss_gen
# rfss_l = rfss_gen.RfssGen.gen(test_set)
# import cfss_gen
# cfss_set = cfss_gen.CfssGen.gen(rfss_l)
# import product_spec_gen
# po_spec = product_spec_gen.ProductSpecGen.genFromCfss(cfss_set, number = 10)

# resource_set = resource_spec_gen.ResousceSpecGen.gen("app")
# po_spec2 = product_spec_gen.ProductSpecGen.genFromAppResource(resource_set, number = 10)

# ps = {
#     "infra": tuple(po_spec),
#     "app": tuple(po_spec2)
# }
# r = ProductOfferGen.gen(ps, 20)

