__author__ = 'Katherine'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re

import os
#Set the proper current working directory
os.getcwd()
os.chdir('/Users/katherinetansey/Dropbox/udacity/project3')

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib.get("k")
        if re.search(lower, key):
            keys['lower'] += 1
        elif re.search(lower_colon, key):
            keys['lower_colon'] += 1
        elif re.search(problemchars, key):
            keys['problemchars'] += 1
        else:
            keys["other"] = keys["other"] + 1
        pass

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


keys = process_map('bridgewater_nj.txt')
pprint.pprint(keys)
