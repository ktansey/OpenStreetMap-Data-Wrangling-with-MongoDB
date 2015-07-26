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

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "node":
            uid = element.attrib.get("uid")
            #print uid
            if uid not in users:
                users.add(uid)
            else:
                pass
        if element.tag == "way":
            uid = element.attrib.get("uid")
            #print uid
            if uid not in users:
                users.add(uid)
            else:
                pass
        if element.tag == "relation":
            uid = element.attrib.get("uid")
            #print uid
            if uid not in users:
                users.add(uid)
            else:
                pass
    return users


users = process_map('bridgewater_nj.txt')
pprint.pprint(users)



