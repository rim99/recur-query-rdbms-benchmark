import csv
import uuid
import random
from datetime import datetime

product_spec_number_estimated = 200
app_product_spec_number_estimated = 20
product_offer_number_estimated = 4000

START = datetime.fromisoformat('2020-01-01T12:00:00')
START_TIMESTAMP = START.timestamp()
END = datetime.fromisoformat('2020-11-30T23:00:00')
END_TIMESTAMP = END.timestamp()

def random_time():
    t1 = random.randrange(START_TIMESTAMP, END_TIMESTAMP)
    t2 = random.randrange(START_TIMESTAMP, END_TIMESTAMP)
    start_time, end_time = (t1, t2) if t1 < t2 else (t2, t1)
    return datetime.utcfromtimestamp(start_time), datetime.utcfromtimestamp(end_time)

entity_fields = [
    'start_time',
    'end_time',
    'entity_id',
    'operator_name',
    'psr_type',
    'revision_id',
    'name',
    'description',
    'properties',
    'tags'
]

relationship_field = [
    'parent_entity_id',
    'child_entity_id'
]

operators = [
    "AT&T", "Verizon", "Nippon",
    "Deutsche Telekom", "T-Mobile",
    "Vodafone", "Telefonica", "America Movil",
    "KDDI", "Orange", "Digi", 
    "China Mobile", "LG", "NTT", 
    "Samsung", "Jio", "Bharti Airtel"
]

def start():
    for operator in operators:

        import tag_gen
        tags = tag_gen.TagGen.gen()
        tag_l = len(tags)

        def random_tag_ref():
            n = random.randrange(3, 8)
            ids = set()
            for i in range(n):
                id = random.randrange(tag_l) 
                ids.add(id)
            ref = [tags[i].id for i in ids]
            return ref
            
        import resource_spec_gen
        import rfss_gen
        import cfss_gen
        import product_spec_gen
        import product_offer_gen

        infra_res_set = resource_spec_gen.ResousceSpecGen.gen("infra")
        rfss_l = rfss_gen.RfssGen.gen(infra_res_set)
        cfss_set = cfss_gen.CfssGen.gen(rfss_l)
        po_spec = product_spec_gen.ProductSpecGen.genFromCfss(cfss_set, number = product_spec_number_estimated)
        resource_set = resource_spec_gen.ResousceSpecGen.gen("app")
        po_spec2 = product_spec_gen.ProductSpecGen.genFromAppResource(resource_set, number = app_product_spec_number_estimated)
        ps = {
            "infra": tuple(po_spec),
            "app": tuple(po_spec2)
        }
        po = product_offer_gen.ProductOfferGen.gen(ps, product_offer_number_estimated)

        for x in infra_res_set:
            start_time, end_time = random_time()
            record = x.to_record(operator, random_tag_ref(), start_time, end_time)
            print(record)



















