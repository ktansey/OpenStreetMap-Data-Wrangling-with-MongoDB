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


expected = ["08807", "07065", "07080", "07059", "07060", "07069", "07920", "07921", "07924", "07928", "07930", "07932",
            "07933", "07959", "07977", "07980", "08809", "08812", "08821", "07093", "07853", "07922", "07927", "07945",
            "08822", "08826", "08835", "08844", "08846", "08854", "08855", "07939", "07940", "07950", "07960", "07962",
            "08867", "08873", "08876", "07981"]


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_name(name):
    if '-' in name:
        sep = '-'
        name = name.split(sep, 1)[0]
    return name

st_types = audit(OSMFILE)
#pprint.pprint(dict(st_types))

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name)
        if name != better_name:
            print name, "=>", better_name