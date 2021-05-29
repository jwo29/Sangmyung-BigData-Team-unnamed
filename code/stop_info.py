import requests
import urllib.parse as urlparse
import json
import pandas as pd
import numpy as np

# URL 만들기 함수
def get_request_query(operation1, operation2, params, serviceKey):
    URL = "http://openapi.tago.go.kr/openapi/service"
    params = urlparse.urlencode(params)
    request_query = URL + '/' + operation1 + '/' + operation2 + '?' + params + '&' + 'ServiceKey' + '=' + serviceKey
    return request_query


# 요청 URL과 오퍼레이션
URL = "http://openapi.tago.go.kr/openapi/service"

OPERATION1 = "BusRouteInfoInqireService"
OPERATION2 = "getRouteAcctoThrghSttnList"  

# 서비스키
SERVICEKEY = "Ee5WLqN4iRCKuFUsxlAF1P9anyOX5vH%2BOFG2%2BYM%2BcEoNQOg9emMEyyKM37eAmmVnl1ZxgTalHHL90VNl1B1zlg%3D%3D"

bus_stop_data = pd.DataFrame(columns = ("routeno", "routeid", "nodenm", "nodeord", "nodeid", "nodeno", "gpslati", "gpslong")) 

stop_name = pd.read_csv("stop_name.csv")

# 파라미터, 노선id는 버스_주요정류소_정보.csv에서 가저온다
cityCode  = 34010
numOfRows = 150
_type = "json"

bus_route_id_idx = 0 #  노선id별 정류소id들을 구하기 위해 사용

for index, routeId in enumerate(stop_name["routeid"]):
   
    bus_nodeord_idx = 2 # stop순서 데이터가 인덱스 3부터 7까지
    stop_num = 1 # stop에 붙는 순서 번호
    
    try:
        PARAMS = {'cityCode':cityCode, 'routeId':routeId, 'numOfRows': numOfRows, '_type': _type}

        # URL만들기
        request_query = get_request_query(OPERATION1, OPERATION2, PARAMS, SERVICEKEY)
        print('request_query:', request_query)

        # #GET
        response = requests.get(url = request_query)

        #상태 확인
        #print('status_code:' + str(response.status_code))

        r_dict = json.loads(response.text)
        r_response = r_dict.get("response")
        r_body = r_response.get("body")
        r_items = r_body.get("items")
        r_item = r_items.get("item")
        
    except:
        print("api 문제")
        
    try:
        for item in r_item: 
            if(bus_nodeord_idx > 6): 
                break
            try:
                if(item.get("nodenm") == stop_name.iloc[index, bus_nodeord_idx]):
                    print(item.get("nodenm"))
                    routeno = stop_name.iloc[index, 0]
                    nodeord = "stop" + str(stop_num)
                    routeid = item.get("routeid")
                    nodeid = item.get("nodeid")
                    nodenm = item.get("nodenm")
                    nodeno = item.get("nodeno")
                    gpslati = item.get("gpslati")
                    gpslong = item.get("gpslong")
                    bus_stop_data.loc[bus_route_id_idx] = [ routeno, routeid, nodenm, nodeord, nodeid, nodeno, gpslong, gpslati ]
                    
                    stop_num += 1
                    bus_route_id_idx += 1
                    bus_nodeord_idx += 1
                    
            except:
                print("error: "+ str(routeNo))
            
    except:
        print("접근문제")



#bus_stop_data.to_csv("stop_info.csv", encoding='utf-8-sig', index=False)
#bus_stop_data.groupby(["nodenm", "nodeid"]).size().to_csv("stop_group.csv", encoding='utf-8-sig')