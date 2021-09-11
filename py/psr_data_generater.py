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

add_tag = ("INSERT INTO tag "
           "(tag_id, operator_name, name) "
           "VALUES (%(tag_id)s, %(operator_name)s, %(name)s)")
add_spec = ("INSERT INTO specification "
            "(start_time, end_time, entity_id, revision_id, operator_name, psr_type, name, description, properties) "
            "VALUES (%(start_time)s, %(end_time)s, %(entity_id)s, %(revision_id)s, "
            "%(operator_name)s, %(psr_type)s, %(name)s, %(description)s, %(properties)s)")
add_spec_tag_relation = ("INSERT INTO spec_tag "
                         "(operator_name, entity_id, revision_id, tag_id) "
                         "VALUES (%(operator_name)s, %(entity_id)s, %(revision_id)s, %(tag_id)s)")

def start(mysql_cnx, pg_cnx):
    my_cursor = mysql_cnx.cursor()
    pg_cursor = pg_cnx.cursor()
    try:
        insert_record(my_cursor, pg_cursor)
    finally:
        mysql_cnx.commit()
        my_cursor.close() 
        pg_cnx.commit()
        pg_cursor.close()
        pg_cnx.close()   

def insert_record(mysql_cursor, pg_cursor):
    for operator in operators:
        import tag_gen
        tags = tag_gen.TagGen.gen()
        tag_l = len(tags)
        for t in tags:
            mysql_cursor.execute(add_tag, t.to_mysql_record(operator))  
            pg_cursor.execute(add_tag, t.to_pg_record(operator)) 


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

        for psr_models in (infra_res_set,resource_set, cfss_set, po_spec, po_spec2, po):
            for entity in psr_models:
                start_time, end_time = random_time()
                tag_ref = random_tag_ref()
                m_rec = entity.to_mysql_record(operator, start_time, end_time)
                pg_rec = entity.to_pg_record(operator, start_time, end_time)
                try:
                    mysql_cursor.execute(add_spec, m_rec)  
                except Exception as e:
                    print("MySQL fail to save")
                    print(m_rec)
                    raise e
                try:
                    pg_cursor.execute(add_spec, pg_rec) 
                except Exception as e:
                    print("PG fail to save")
                    print(pg_rec)
                    raise e    
                



















