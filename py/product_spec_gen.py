import random
import id_gen
import json


avaliable_countries = [
    "US", 
    "Japan", 
    "UK",
    "China Hongkong", 
    "China Mainland", 
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Ecuador",
    "Egypt",
    "Bulgaria",
    "Fiji",
    "Finland",
    "France",
    "Burkina Faso",
    "Burundi",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Pakistan",
    "Palau",
    "Palestine",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Venezuela",
    "Vietnam",
    "Timor-Leste",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Zambia",
    "Zimbabwe",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Yemen",
    "Romania",
    "Russia",
    "Rwanda",
    "Qatar"
]
ac_len = len(avaliable_countries)

class ProductSpec:
    def __init__(self, child_id_tuple, supported_countries = ()):
        self.id = id_gen.UUID1.get()
        self.rev_id = id_gen.UUID1.get()
        self.child_id_tuple = child_id_tuple
        self.supported_countries = supported_countries
    def __str__(self):
        return str(self.__dict__)
    def __eq__(self, other):
        return (self.child_id_tuple, self.supported_countries)== (other.child_id_tuple, other.supported_countries)
    def __hash__(self):
        return hash(("ProductSpec", self.child_id_tuple, self.supported_countries))     
    def to_mysql_record(self, operator, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": self.id.bytes,
            "operator_name": operator,
            "psr_type": 3,
            "revision_id": self.rev_id.bytes,
            "name": "product_spec",
            "description": str(self.supported_countries),
            "properties": json.dumps({
                "supported_countries": self.supported_countries
            })            
        }
        return rec     
    def to_pg_record(self, operator, start_time, end_time):
        rec = {
            "start_time": start_time,
            "end_time": end_time,
            "entity_id": str(self.id),
            "operator_name": operator,
            "psr_type": 3,
            "revision_id": str(self.rev_id),
            "name": "product_spec",
            "description": str(self.supported_countries),
            "properties": json.dumps({
                "supported_countries": self.supported_countries
            })            
        }
        return rec         

def random_supported_countries():
    ac_indices = set()
    for i in range(5, 50):
        i = random.randrange(ac_len)
        ac_indices.add(i)
    ac = [avaliable_countries[i] for i in ac_indices]
    ac.sort
    return tuple(ac)


class ProductSpecGen:
    @staticmethod
    def genFromCfss(cfss_set, number = 200):
        result = set()
        cfss_l = [x for x in cfss_set]
        length_l = len(cfss_l)
        indices = [random.randrange(length_l) for i in range(3, 18)]
        indices.sort()
        for i in range(number):
            ref = tuple([cfss_l[j].id for j in indices])
            ac = random_supported_countries() 
            result.add(ProductSpec(ref, ac))
        return tuple(result)

    @staticmethod
    def genFromAppResource(resource_set, number = 20):
        result = set()
        for r in resource_set:
            ac = random_supported_countries()
            result.add(ProductSpec((r.id), ac))
        return tuple(result)    


# import resource_spec_gen
# test_set = resource_spec_gen.ResousceSpecGen.gen("infra")
# import rfss_gen
# rfss_l = rfss_gen.RfssGen.gen(test_set)
# import cfss_gen
# cfss_set = cfss_gen.CfssGen.gen(rfss_l)

# po_spec = ProductSpecGen.genFromCfss(cfss_set, number = 10)

# resource_set = resource_spec_gen.ResousceSpecGen.gen("app")
# po_spec2 = ProductSpecGen.genFromAppResource(resource_set, number = 10)
# for x in po_spec2:
#     print(x)


