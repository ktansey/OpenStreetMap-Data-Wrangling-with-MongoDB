__author__ = 'katherinetansey'


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

import os
#Set the proper current working directory
os.getcwd()
os.chdir('/Users/katherinetansey/Dropbox/udacity/project3')


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# UPDATE THIS VARIABLE
mapping_street = { "St": "Street",
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
            "W. High Street": "West High Street",
            "80 Morristown Road Unit 17": "80 Morristown Road",
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



CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POSITION = ["lat", "lon"]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        id = element.attrib.get("id")
        node['id'] = id
        node['visible'] = element.attrib.get("visible")
        for key in element.attrib.keys():
            #print key
            val = element.attrib[key]
            node["type"] = element.tag
            #values =  element.attrib.values()
            #print keys, values
            if key in CREATED:
                #print key
                #print val
                if not "created" in node.keys():
                    node["created"] = {}
                node["created"][key] = val
            if key in POSITION:
                #print key
                #print val
                if not "pos" in node.keys():
                    node["pos"] = ['0.0', '0.0']
                if node["pos"][1] == '0.0':
                    node["pos"][1] = val
                else:
                    node["pos"][0] = val
            else:
                pass
            for tag in element.iter("tag"):
                if not "address" in node.keys():
                    node['address'] = {}
                #print tag
                key = tag.attrib.get("k")
                #print key
                val = tag.attrib.get("v")
                if problemchars.match(key):
                    pass
                #print val
                elif key == "addr:housenumber":
                    #print val
                    node['address']['housenumber'] = val
                elif key == "addr:postcode":
                    if '-' in val:
                        sep = '-'
                        zip = val.split(sep, 1)[0]
                        #print zip
                        node['address']['postcode'] = zip
                    else:
                         node['address']['postcode'] = val
                elif key == "addr:street":
                    street = val
                    for key in mapping_street:
                        if street.endswith(key):
                            street = street.replace(key, mapping_street[key])
                            street = street.title()
                            node['address']['street'] = street
                        else:
                            continue
                    node['address']['street'] = street
                    #print street
                elif key == "amenity" :
                    node['amenity'] = val
                elif key == "cuisine":
                    node['cuisine'] = val
                elif key == "name" :
                    node['name'] = val
                elif key == "phone" :
                    node['phone'] = val
                    #print node
                elif key == "religion":
                    node['religion'] = val
                elif key == 'denomination':
                    node['denomination'] = val
                else:
                    pass
            for items in element.iter("nd"):
                ref = items.attrib.get("ref")
                node['node_refs'] = ref

        #print node
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():

    data = process_map('bridgewater_nj.txt', True)
    #pprint.pprint(data)

if __name__ == "__main__":
    test()