import csv
import uuid
import random
from datetime import datetime
import threading
import os

product_spec_number_estimated = 200
app_product_spec_number_estimated = 20
product_offer_number_estimated = 4000

START = datetime.fromisoformat('2020-01-01T12:00:00')
START_TIMESTAMP = START.timestamp()
END = datetime.fromisoformat('2020-11-30T23:00:00')
END_TIMESTAMP = END.timestamp()
insert_to_mysql = os.environ['INSERT_TO_MYSQL'] == 'true'
insert_to_mariadb = os.environ['INSERT_TO_MARIADB'] == 'true'
insert_to_postgres = os.environ['INSERT_TO_PG'] == 'true'

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
    "AT&T", 
    "Verizon", 
    "Nippon",
    "Deutsche Telekom", 
    "T-Mobile",
    "Vodafone", 
    "Telefonica", 
    "America Movil",
    "KDDI", 
    "Orange", 
    "Digi", 
    "China Mobile", 
    "LG", 
    "Japan Telecom", 
    "Samsung", 
    "Jio", 
    "Bharti Airtel"
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
add_spec_relation = ("INSERT INTO spec_relationship "
                     "(operator_name, parent_entity_id, child_entity_id) "
                     "VALUES (%(operator_name)s, %(parent_entity_id)s, %(child_entity_id)s)")                         

def start(mysql_cnx_pool, pg_cnx, mariadb_cnx_pool):
    try:
        worker_group = []
        for operator in operators:
            w = Worker(operator, mysql_cnx_pool.get_connection(), pg_cnx, mariadb_cnx_pool.get_connection())
            w.start()
            worker_group.append(w)
        for w in worker_group:
            w.join()
    finally:
        # mysql_cnx_pool.close()
        pg_cnx.close()


class Worker(threading.Thread):
    def __init__(self, operator, mysql_cnx, pg_cnx, mariadb_cnx):
       threading.Thread.__init__(self)
       self.operator = operator
       self.mysql_cnx = mysql_cnx
       self.pg_cnx = pg_cnx
       self.mariadb_cnx = mariadb_cnx
    def run(self):
        my_cursor = self.mysql_cnx.cursor()
        pg_cursor = self.pg_cnx.cursor()
        ma_cursor = self.mariadb_cnx.cursor()
        try:
            self.insert_record(my_cursor, pg_cursor, ma_cursor, self.operator, random.randrange(300, 600))
        finally:
            self.mysql_cnx.commit()
            my_cursor.close() 
            self.mysql_cnx.close()
            self.pg_cnx.commit()
            pg_cursor.close()
            self.mariadb_cnx.commit()
            ma_cursor.close()
            self.mariadb_cnx.close()


    def insert_record(self, mysql_cursor, pg_cursor, mariadb_cursor, operator, step):
        import tag_gen
        tags = tag_gen.TagGen.gen()
        tag_l = len(tags)
        for t in tags:
            if insert_to_mysql:
                mysql_cursor.execute(add_tag, t.to_mysql_record(operator))  
            if insert_to_mariadb:
                mariadb_cursor.execute(add_tag, t.to_mysql_record(operator))  
            if insert_to_postgres:        
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

        counter = 0
        for psr_models in (infra_res_set, rfss_l, resource_set, cfss_set, po_spec, po_spec2, po):
            for entity in psr_models:
                counter += 1
                if counter % step == 0:
                    print("inserting")
                start_time, end_time = random_time()
                tag_ref = random_tag_ref()
                if insert_to_mysql:
                    m_rec = entity.to_mysql_record(operator, start_time, end_time)
                    try:
                        mysql_cursor.execute(add_spec, m_rec)
                        for t_id in tag_ref:
                            mysql_cursor.execute(add_spec_tag_relation, {
                                "operator_name": operator,
                                "entity_id": entity.id.bytes,
                                "revision_id": entity.rev_id.bytes,
                                "tag_id": t_id.bytes
                            })  
                        for c_id in entity.get_ref_list():
                            mysql_cursor.execute(add_spec_relation, {
                                "operator_name": operator,
                                "parent_entity_id": entity.id.bytes,
                                "child_entity_id": c_id.bytes
                            })
                    except Exception as e:
                        print("MySQL fail to save")
                        print(m_rec)
                        raise e
                if insert_to_mariadb:
                    m_rec = entity.to_mysql_record(operator, start_time, end_time)
                    try:
                        mariadb_cursor.execute(add_spec, m_rec)
                        for t_id in tag_ref:
                            mariadb_cursor.execute(add_spec_tag_relation, {
                                "operator_name": operator,
                                "entity_id": entity.id.bytes,
                                "revision_id": entity.rev_id.bytes,
                                "tag_id": t_id.bytes
                            })  
                        for c_id in entity.get_ref_list():
                            mariadb_cursor.execute(add_spec_relation, {
                                "operator_name": operator,
                                "parent_entity_id": entity.id.bytes,
                                "child_entity_id": c_id.bytes
                            })
                    except Exception as e:
                        print("MariaDB fail to save")
                        print(m_rec)
                        raise e        
                if insert_to_postgres:    
                    pg_rec = entity.to_pg_record(operator, start_time, end_time)    
                    try:
                        pg_cursor.execute(add_spec, pg_rec) 
                        for t_id in tag_ref:
                            pg_cursor.execute(add_spec_tag_relation, {
                                "operator_name": operator,
                                "entity_id": str(entity.id),
                                "revision_id": str(entity.rev_id),
                                "tag_id": str(t_id)
                            })  
                        for c_id in entity.get_ref_list():
                            pg_cursor.execute(add_spec_relation, {
                                "operator_name": operator,
                                "parent_entity_id": str(entity.id),
                                "child_entity_id": str(c_id)
                            })    
                    except Exception as e:
                        print("PG fail to save")
                        print(pg_rec)
                        raise e    
