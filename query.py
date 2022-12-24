#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 21:48:01 2022

@author: akmami
"""

from os import listdir
from os.path import isfile, join
import json


domains_dir = 'predefined/domains.json'

onlyfiles = [f for f in listdir('result') if isfile(join('result', f))]

graphs = [f for f in onlyfiles if f[len(f)-5:len(f)] == '.json']
graphs.sort()
domains = json.load(open(domains_dir))

while True:
    i = 1
    for file in graphs:
        print(i, file)
        i = i + 1
    user_input = input('Choose a graph file (q to quit): ')
    if user_input == 'q':
        break
    
    graph_dir = 'result/' + graphs[int(user_input)-1]
    graph = json.load(open(graph_dir))
    
    dbIDs = []
    for item in graph:
        if item['dbID'] not in dbIDs:
            dbIDs.append(item['dbID'])
    dbIDs.sort()
    
    print()
    
    i = 1
    for domain in domains.keys():
        print(i, domain)
        i = i + 1
    
    user_input = int(input('Choose a domain: '))
    domain = ''
    i = 1
    for value in domains.keys():
        if (i == user_input):
            domain = value
            break
        i = i + 1
    
    print()
    
    t1 = input('Please enter attribute at instance t: ')
    t2 = input('Please enter attribute at instance t+1: ')
    
    print()
    
    if not any(node[domain]==t1 for node in graph):
        print('no')
        continue
    if not any(node[domain]==t2 for node in graph):
        print('no')
        continue
    
    attr1 = []
    attr2 = []
    for node in graph:
        if node[domain] == t1 and node['dbID'] == dbIDs[0]:
            attr1.append(node)
    for node in graph:
        if node[domain] == t2 and node['dbID'] == dbIDs[1]:
            for item in attr1:
                if item['id'] == node['id']:
                    attr2.append(node)
                    break
    
    print(attr2)
    print()