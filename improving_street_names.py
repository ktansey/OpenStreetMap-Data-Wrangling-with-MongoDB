__author__ = 'katherinetansey'

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

import os
#Set working directory
os.getcwd()
os.chdir('/Users/katherinetansey/Dropbox/udacity/project3')
OSMFILE = "bridgewater_nj.txt"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Circle", "Crescent", "Drive", "Close", 
            "Court", "Place","Square", "Way", "West", "Lane", "Road", "Trail", 
            "Esplanade", "Grove", "Gardens", "Parkway","Embankment", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Plymouth Pl": "Plymouth Place",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "AVE.": "Avenue",
            "road": "Road",
            "Blvd": "Boulevard",
            "Rd.": "Road",
            "Cir": "Circle",
            "Ct": "Court",
            "LANE": "Lane",
            "PLACE": "Place",
            "Pky": "Parkway",
            "ROAD": "Road",
            "Rd": "Road",
            "ave": "Avenue",
            "LANE WEST": "Lane West",
            #"W. High St.": "West High Street",
            "W. High Street": "West High Street",
            "80 Morristown Road Unit 17": "80 Morristown Road",
            "JFK Blvd.": "JFK Boulevard",
            "Route 206 South": "Route 206",
            "NJ 31 S": "Route 31",
            "US 206": "Route 206",
            "US 22": "Route 22",
            "Rt-31": "Route 31",
            "Mendham Road (Old Rt. 24)": "Mendham Road ",
            "W. Main Street (Old Rt. 24)" : "West Main Street",
            "ROAD 3": "Route 3",
            "Alstede Farms": "Alstede Farms Lane",
            "JOYCE KILMER AVENUE (S/N TWRS)": "Joyce Kilmer Avenue"}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_name(name, mapping):
    for key in mapping:
        if name.endswith(key):
            name = name.replace(key, mapping[key])
            name = name.title()
            if name == "Jfk Boulevard":
                name = "JFK Boulevard"
            else:
                continue
    return name

st_types = audit(OSMFILE)
pprint.pprint(dict(st_types))

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        if name != better_name:
            print name, "=>", better_name