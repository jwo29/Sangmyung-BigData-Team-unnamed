import requests
import urllib.parse as urlparse
import json
import pandas as pd
import numpy as np
import csv
import time
import schedule
import datetime

#input#
serviceKey = "7oZHJT4sU22l%2FztC7xaZcrmPYkHuuw2gt%2FVz%2FZtiLdKHvTTGFJj9tZJbi2iA3VP9ThcCy4eOM7MV1L9nBiS1tw%3D%3D"

#url 요청
def get_request(params):
    url = "http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"
    params = urlparse.urlencode(params)
    url += '/' + params + '&' + serviceKey
    return url

#노선id 와 정류소id load
routeId_BusStop = pd.read_csv("버스_정류소아이디_정보.csv") # <-파일 위치 삽입
nodeId = routeId_BusStop.name["nodeId"]
routeId = routeId_BusStop.name["routId"]

cityCode = 34010 #천안시 도시 번호
numOfRows = 10 #최대 10개씩 보기
_type = "json" #json형태로 받기

#save natural data
#date.time() live로

def save_data(data):
    with open('file_name.csv', mode='a') as file_name: #file 열기
        writer = csv.writer(file_name)
        writer.writerow(data)
        file_name.close() #file 닫기

def get_data():
    for nl, rl in zip(nodeId, routeId):
        params = {'cityCode':cityCode, 'routeId':rl, 'nodeId': nl, 'numOfRows': numOfRows, '_type': _type}
        try:
            request_query = get_request(params) #call func.
        
            response = requests.get(url = request_query)
            curr_time = datetime.datetime.now() #request 한 시간
            r_dict = json.loads(response.text) #change to json
            r_response = r_dict.get("response") #
            r_body = r_response.get("body") #
            r_items = r_body.get("items") #
            r_item = r_items.get("item") #

            #change type
            if type(r_item) is not list:
                temp = []
                temp.append(r_item)
                r_item = temp

        except: #예외 처리
            pass
        
        for item in r_item:
            routeno = item.get("routeno")
            routeid = item.get("routeid")
            nodeid = item.get("nodeid")
            nodenm = item.get("nodenm")
            arrtime = item.get("arrtime")
            arrprevstationcnt = item.get("arrprevstationcnt") 

            data= [curr_time, routeno, routeid, nodeid, nodenm, arrtime, arrprevstationcnt]
            save_data(data) #call func.

#main#
if __name__ == "__main__":
    get_data()
