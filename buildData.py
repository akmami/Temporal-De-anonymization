#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lara
"""
import random
import json


timeList =["2018-09-30T18:40:32.142+0100","2020-11-30T18:40:32.142+0100","2022-12-30T18:40:32.142+0100"]
jsonNodes =[]
name_list =[
    "Nylah Walker","Cheyenne Coleman","Tucker Gates","Rylie Barton","Taylor Wells","Ansley Park","Sabrina Bonilla","Paul Hunter",
    "Andres Pittman","Madeleine Hopkins","Omari Fitzgerald","Corey Lambert","Franklin Esparza","Kara Watkins","Brennen Montgomery",
    "Jaquan Hopkins","Bobby George","Angel Woods","Baylee Bolton","Yaretzi Sweeney","Darrell Gonzalez","Clara Hickman","Malachi Juarez"
    "Caitlin Lang","Adeline Peters","Braelyn Bowman","Abby Decker","Sammy Pugh","Gaige Christian","Joanna Moyer","Kailee Lawrence",
    "Lilly Cunningham","Kareem Williamson","Jaelynn Harris","Eva Parrish","Rylee Green"]
social_clup_dic = [
    {"Art":[ "Painting", "Sculpture","Literature","Cinema"]},
    {"Sport":[ "Bowling", "Cycling","Basketball","Hiking"]},
    {"Science":[ "Biology", "Computer","Chemistry","Physics"]},
]
social_club_list =  ["Painting", "Biology", "Computer", "Sculpture", "Bowling", "Cycling", "Basketball", "Hiking", "Literature", "Cinema", "Chemistry", "Physics"]
relationship_status_list  = ["single", "separated", "divorced", "Widow", "roommates", "cohabitants", "de facto", "taken", "relationship", "engaged", "married", "second marriage"]
education_level_list = ["Primary", "Secondary", "High School", "Bachelor", "Master", "PhD"]

jsonNames = {}

user_id = 1

for user in name_list:
    #Properties
    club_list = []
    for x in range(random.randrange(0,4)):
        club = social_club_list[random.randrange(0,len(social_club_list))]
        if club not in club_list: club_list.append(club)
    education_level = education_level_list[random.randrange(0,len(education_level_list))]
    relationship_status = relationship_status_list[random.randrange(0,len(relationship_status_list))]
    
    jsonObj1 ={
        "dbID":1,
        "id": user_id,
        "social_club": club_list,
        "education_level": education_level,
        "relationship_status":relationship_status,
        "snap_shot_time": timeList[0]
    } 
    jsonObj2 ={
        "dbID":2,
        "id": user_id,
        "social_club": club_list,
        "education_level": education_level,
        "relationship_status":relationship_status,
        "snap_shot_time": timeList[1]
    } 
    jsonObj3 ={
        "dbID":3,
        "id": user_id,
        "social_club": club_list,
        "education_level": education_level,
        "relationship_status":relationship_status,
        "snap_shot_time": timeList[2]
    } 
    # Append object for snapshot 1
    jsonNodes.append(jsonObj1) 
    # Append object for snapshot 2
    jsonNodes.append(jsonObj2) 
    # Append object for snapshot 3s
    jsonNodes.append(jsonObj3) 
    # Append user's name and id 
    jsonNames[user] = user_id
    
    user_id = user_id + 1


#with open("sample.json", "w") as outfile:
#    json.dump(jsonNodes, outfile,indent = 4)
    
    
with open("identities.json", "w") as outfile:
    json.dump(jsonNames, outfile,indent = 4)    
