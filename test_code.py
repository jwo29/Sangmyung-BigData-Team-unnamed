import requests
import urllib.parse as urlparse
import json
import pandas as pd
import numpy as np
import csv
import time
import schedule
import datetime
import os

#input#
serviceKey = "7oZHJT4sU22l%2FztC7xaZcrmPYkHuuw2gt%2FVz%2FZtiLdKHvTTGFJj9tZJbi2iA3VP9ThcCy4eOM7MV1L9nBiS1tw%3D%3D"

#url request
def get_request(params):
    url = "http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"
    params = urlparse.urlencode(params)
    url += '?' +"serviceKey=" + serviceKey + "&" + params
    return url

#nodeid and routeid load
routeId_BusStop = pd.read_csv("stop_info.csv") 
nodeId = routeId_BusStop["nodeid"]
routeId = routeId_BusStop["routeid"]

cityCode = 34010 
numOfRows = 10 
_type = "json"

def save_data(data):
    #print(type(data))
    df = pd.DataFrame(data = [data], columns = ("curr_time", "routeno", "routeid", "nodeid", "nodenm", "arrtime", "arrprevstationcnt"))

    if not os.path.exists('test_output.csv'):
        df.to_csv('test_output.csv', index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('test_output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)
    
def get_data():
    for nl, rl in zip(nodeId, routeId):
        params = {'cityCode':cityCode, 'nodeId': nl, 'routeId':rl, '_type': _type}
        try:
            request_query = get_request(params) #call func.
            print('request_query:', request_query)
            response = requests.get(url = request_query)
            curr_time = datetime.datetime.now() 
            r_dict = json.loads(response.text) 
            r_response = r_dict.get("response") 
            r_body = r_response.get("body") 
            r_items = r_body.get("items") 
            r_item = r_items.get("item") 
        except: 
            r_item = []
            r_header = r_response.get("header")
            if(r_header["resultMsg"] == "NORMAL SERVICE."):
                ("")
                print("NO DATA") 
                #save_data(data) #call func.
            else:
                print("API ERROR: " + str(r_header["resultMsg"]))
            #change type
        if type(r_item) is not list:
            temp = []
            temp.append(r_item)
            r_item = temp
        for item in r_item:
            routeno = item.get("routeno")
            routeid = item.get("routeid")
            nodeid = item.get("nodeid")
            nodenm = item.get("nodenm")
            arrtime = item.get("arrtime")
            arrprevstationcnt = item.get("arrprevstationcnt") 

            data= [curr_time, routeno, routeid, nodeid, nodenm, arrtime, arrprevstationcnt]
            save_data(data) #call func.
            print("SAVE DATA")


#main#
if __name__ == "__main__":
    get_data()
#     for _ in range(24): 
#         print("1")
#         schedule.every(5).minutes.do(get_data)

