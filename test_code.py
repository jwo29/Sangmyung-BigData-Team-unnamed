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

# load file
serviceKey_file = pd.read_csv("key.csv")

# input#
# 키 한번에 묶어서 트래픽 다쓰면 바꿀수 있게 만들기

# 트래픽을 저장
def set_traffic():
    serviceKey_file = pd.read_csv("key.csv")
#     mask = serviceKey_file['serviceKey'] == serviceKey
    serviceKey_file.loc[serviceKey_idx, "traffic"] = traffic  # 수정, 경고에서 이렇게 고치가로 함!, 아래 30번이란 다른점이 애는 파일에 붙여넣기고 아래는 값만 가져와 반환
    serviceKey_file.to_csv("key.csv", index=False, mode='w',
                           encoding='utf-8-sig')  # index=False, 행 (인덱스) 이름 쓰기 여부 (기본값 True)


def init_serviceKey():
    for value in serviceKey_file['traffic']:
        if value < 990 and value >= 0:
            temp = list(serviceKey_file['traffic'])
            index = temp.index(value)
    #             return serviceKey_file['serviceKey'][index], value
            print(index, value)
            return index, value
        else:
            print("다음 서비스키로~")
    #             set_traffic(serviceKey, value)

    # 9개의 serviceKey를 모두 소진한 경우
    print("Error: there arn't usable traffic")
    return None, None
    
# 키 바꾸는 함수
def get_serviceKey():
    if serviceKey_idx >= 9:
        # 9개의 serviceKey를 모두 소진한 경우
        print("Error: there arn't usable traffic")
        return None, None
    else:
        return serviceKey_idx+1, 0


serviceKey_idx, traffic = init_serviceKey()


# url request
def get_request(params):
#     global serviceKey
    serviceKey = serviceKey_file.loc[serviceKey_idx, "serviceKey"]
    url = "http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"
    params = urlparse.urlencode(params)
    url += '?' + "serviceKey=" + serviceKey + "&" + params
    return url


# nodeid and routeid load
routeId_BusStop = pd.read_csv("stop_info.csv")
nodeId = routeId_BusStop["nodeid"]
routeId = routeId_BusStop["routeid"]

file_name = datetime.datetime.now().strftime('%Y_%m_%d') + "_test_output.csv"

cityCode = 34010
numOfRows = 10
_type = "json"


def save_data(data):
    df = pd.DataFrame(data=[data], columns=(
    "curr_date", "curr_time", "routeno", "routeid", "nodeid", "nodenm", "arrtime", "arrprevstationcnt"))
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv(file_name, index=False, mode='a', encoding='utf-8-sig', header=False)


def get_data():
#     global serviceKey, traffic
    for nl, rl in zip(nodeId, routeId):
        params = {'cityCode': cityCode, 'nodeId': nl, 'routeId': rl, '_type': _type}
        try:
            date_time = datetime.datetime.now()
            curr_date = date_time.strftime('%Y-%m-%d')
            curr_time = date_time.strftime('%H:%M:%S')

#             serviceKey, traffic = get_serviceKey()
#             if serviceKey == None and traffic == None:
#                 serviceKey, traffic = get_serviceKey()
#                 print("get_serviceKey")

            request_query = get_request(params)  # get url
            print('request_query:', request_query)
            response = requests.get(url=request_query)  # get data

            traffic += 1
            if traffic >= 990:
                set_traffic()  # 트래픽 저장
                serviceKey_idx, value = get_serviceKey()

            r_dict = json.loads(response.text)
            r_response = r_dict.get("response")
            r_body = r_response.get("body")
            r_items = r_body.get("items")
            r_item = r_items.get("item")
        except:
            r_item = []
            r_header = r_response.get("header")
            if (r_header["resultMsg"] == "NORMAL SERVICE."):
                print("NO DATA")
            else:
                print("API ERROR: " + str(r_header["resultMsg"]))
            # change type
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

            data = [curr_date, curr_time, routeno, routeid, nodeid, nodenm, arrtime, arrprevstationcnt]
            save_data(data)  # call func.
            print("SAVE DATA")


# 코드 돌리기 전에 key.csv 손으로 0 초기화
# 내일 할거
# 서비스키를 save하고 get하는 함수 호출부분 최적화

# 스케줄 함수 구현
# 파일 날짜별로 저장하기
##########################################
# traffic은 매 4분마다. (하루 총 8064번)
# 코드 최적화  // 트래픽 인덱스 전역 변수
# 스케줄 함수 구현
# traffic 파일은 꼭 시간대 종료 후에 다음 사람과 확인할 것
# 정류장 정리해서 보내줄 것

# main#
if __name__ == "__main__":
    get_data()
    set_traffic()
