#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 00:47:48 2022

@author: akmami
"""

import json
import math
import random
import copy
import numpy as np


def euclideanDistance(attr1, attr2, domain):
    list1 = domain[attr1]
    list2 = domain[attr2]
    if len(list1) != len(list2):
        return float('inf')
    distance = 0
    for i in range(len(list1)):
        distance = distance + pow(list1[i]-list2[i], 2)
    return math.sqrt(distance)


def vClosest(attribute, domain, v):
    distances = []
    for item in domain.keys():
        distance = euclideanDistance(attribute, item, domain)
        if abs(distance) <= v:
            distances.append((distance, item))
    return distances


def anonymizeTemporalData(identities, nodes_t1, nodes_t2, domains, distances, snapshot1, snapshot2, console):
    anonymized_graph = []
    total_distance = 0
    for node in nodes_t2:
        node2 = copy.deepcopy(node)
        if any(node2['name']==node1['name'] for node1 in nodes_t1):
            anonymized_node = {}
            anonymized_node['id'] = identities[node2['name']]
            isPrinted = False
            for attribute in node2:
                if attribute not in distances.keys():
                    if attribute == 'name':                             # name
                        anonymized_node['id'] = identities[node2['name']]
                    else:                                               # dbID
                        anonymized_node[attribute] = node2[attribute]
                elif type(node2[attribute]) is list:
                    node1 = next(item for item in nodes_t1 if item['name'] == node2['name'])
                    new_attributes = []
                    for item2 in node2[attribute]:                       # if new attribute is added to list
                        if item2 not in node1[attribute]:
                            closestSubstitutes = vClosest(item2, domains[attribute], distances[attribute])
                            new_attribute = random.choice(closestSubstitutes)
                            if np.random.binomial(1, .5, 1) == 1:       # anonymize temporal data
                                new_attributes.append(new_attribute[1])
                                total_distance = total_distance + euclideanDistance(item2, new_attribute[1], domains[attribute])
                                if console:
                                    if not isPrinted:
                                        isPrinted = True
                                        print('node id:', anonymized_node['id'])
                                    print('temporal', 'added', item2, 'closestSubstitutes', closestSubstitutes)
                            else:
                                total_distance = total_distance + euclideanDistance(item2, 'None', domains[attribute])
                                if console:
                                    if not isPrinted:
                                        isPrinted = True
                                        print('node id:', anonymized_node['id'])
                                    print('temporal', item2, 'not added by binomial')
                        else:
                            new_attributes.append(item2)
                    for item1 in node1[attribute]:                       # if attribute is removed from list
                        if item1 not in node2[attribute]:
                            closestSubstitutes = vClosest('None', domains[attribute], distances[attribute])
                            new_attribute = random.choice(closestSubstitutes)
                            if np.random.binomial(1, .5, 1) == 1:        # anonymize temporal data
                                new_attributes.append(new_attribute[1])
                                total_distance = total_distance + euclideanDistance(item1, new_attribute[1], domains[attribute])
                                if console:
                                    if not isPrinted:
                                        isPrinted = True
                                        print('node id:', anonymized_node['id'])
                                    print('temporal', 'removed', item1, 'closestSubstitutes', closestSubstitutes)
                            else:
                                total_distance = total_distance + euclideanDistance(item1, 'None', domains[attribute])
                                if console:
                                    if not isPrinted:
                                        isPrinted = True
                                        print('node id:', anonymized_node['id'])
                                    print('temporal', item1, 'not removed by binomial')
                    anonymized_node[attribute] = new_attributes
                    
                elif type(node2[attribute]) is str:
                    node1 = next(item for item in nodes_t1 if item['name'] == node2['name'])
                    distance = euclideanDistance(node1[attribute], node2[attribute], domains[attribute])
                    
                    if distance > distances[attribute]:                # if data is temporal
                        closestSubstitutes = vClosest(node2[attribute], domains[attribute], distances[attribute])
                        new_attribute = random.choice(closestSubstitutes)
                        if np.random.binomial(1, .5, 1) == 0:           # do not change temporal data
                            anonymized_node[attribute] = node1[attribute]
                            total_distance = total_distance + euclideanDistance(node2[attribute], node1[attribute], domains[attribute])
                            if console:
                                if not isPrinted:
                                    isPrinted = True
                                    print('node id:', anonymized_node['id'])
                                print('temporal', snapshot1+':', node1[attribute], ',', snapshot2+':', anonymized_node[attribute], ', not added by binomial')
                        else:                                           # anonymize temporal data
                            anonymized_node[attribute] = new_attribute[1]
                            total_distance = total_distance + euclideanDistance(node2[attribute], new_attribute[1], domains[attribute])
                            if console:
                                if not isPrinted:
                                    isPrinted = True
                                    print('node id:', anonymized_node['id'])
                                print('temporal', snapshot1+':', node1[attribute], ',', snapshot2+':', anonymized_node[attribute], ', new_value:', new_attribute[1], ', closestSubstitutes:', closestSubstitutes)
                    else:
                        anonymized_node[attribute] = node2[attribute]   # if data is not temporal
                        if distance > 0:
                            if console:
                                if not isPrinted:
                                    isPrinted = True
                                    print('node id:', anonymized_node['id'])
                                print('normal', snapshot1+':', node1[attribute], ',', snapshot2+':', anonymized_node[attribute])
                        #else:
                        #    print('distance:', distance, node1[attribute], node2[attribute])
                else:
                    anonymized_node[attribute] = node2[attribute]
            temp = next(item for item in nodes_t1 if item['name'] == node2['name'])
            node1 = copy.deepcopy(temp)
            temp = {'id': identities[node1['name']]}
            temp.update(node1)
            node1 = temp
            anonymized_graph.append(node1)
            anonymized_graph.append(anonymized_node)
            if isPrinted and console:
                print()
    for item in anonymized_graph:
        if 'name' in item:
            del item['name']
    return anonymized_graph, total_distance


base_dir = '/Users/akmami/Desktop/DP/'
sample_dir = base_dir + 'sample.json'
domains_dir = base_dir + 'domains.json'
distances_dir = base_dir + 'distances.json'
identities_dir = base_dir + 'identities.json'
anonymized_graph_t1t2_dir = base_dir + 'anonymized_graph_t2.json'
anonymized_graph_t2t3_dir = base_dir + 'anonymized_graph_t3.json'
  
# Opening JSON file
f1 = open(sample_dir)
f2 = open(domains_dir)
f3 = open(distances_dir)
f4 = open(identities_dir)
  
# returns JSON object as a dictionary
graphs = json.load(f1)
domains = json.load(f2)
distances = json.load(f3)
identities= json.load(f4)


nodes_t1 = [x for x in graphs if x['dbID'] == 1]
nodes_t2 = [x for x in graphs if x['dbID'] == 2]
nodes_t3 = [x for x in graphs if x['dbID'] == 3]

n = 100

total1 = 0
for i in range(n):
    if n-1 == i:
        anonymized_graph_t1t2, total_distance = anonymizeTemporalData(identities, nodes_t1, nodes_t2, domains, distances, 't1', 't2', True)
        total1 = total1 + total_distance
        with open(anonymized_graph_t1t2_dir, "w") as output:
            json.dump(anonymized_graph_t1t2, output, indent = 4)
    else:
        anonymized_graph_t1t2, total_distance = anonymizeTemporalData(identities, nodes_t1, nodes_t2, domains, distances, 't1', 't2', False)
        total1 = total1 + total_distance
    
total1 = total1 / n


total2 = 0
for i in range(n):
    if n-1 == i:
        anonymized_graph_t2t3, total_distance = anonymizeTemporalData(identities, nodes_t2, nodes_t3, domains, distances, 't2', 't3', True)
        total2 = total2 + total_distance
        with open(anonymized_graph_t2t3_dir, "w") as output:
            json.dump(anonymized_graph_t2t3, output, indent = 4)
    else:
        anonymized_graph_t2t3, total_distance = anonymizeTemporalData(identities, nodes_t2, nodes_t3, domains, distances, 't2', 't3', False)
        total2 = total2 + total_distance
        
total2 = total2 / n

print('average distance anonymized_graph_t1t2', total1)

print('average distance anonymized_graph_t2t3', total2)