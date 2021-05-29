import requests
import urllib.parse as urlparse
import json
import pandas as pd

# URL 만들기 함수
def get_request_query(operation1, operation2, params, serviceKey):
    URL = 'http://openapi.tago.go.kr/openapi/service'
    params = urlparse.urlencode(params)
    request_query = URL + '/' + operation1 + '/' + operation2 + '?' + params + '&' + 'ServiceKey' + '=' + serviceKey
    return request_query


# 요청 URL과 오퍼레이션
URL = 'http://openapi.tago.go.kr/openapi/service'

OPERATION1 = 'BusRouteInfoInqireService'
OPERATION2 = 'getRouteNoList' # 

# 서비스키
SERVICEKEY = "Ee5WLqN4iRCKuFUsxlAF1P9anyOX5vH%2BOFG2%2BYM%2BcEoNQOg9emMEyyKM37eAmmVnl1ZxgTalHHL90VNl1B1zlg%3D%3D"

bus_routes_data = pd.DataFrame(columns = ("routeno", "routeid")) 
#버스 노선
Bus_routeNo = [11, 12, 13, 14, 24, 81]

# 파라미터
cityCode  = 34010  # 
_type = "json"
numOfRows = 150
idx = 0

for routeNo in Bus_routeNo:
    try:
        PARAMS = {'cityCode':cityCode, 'routeNo':routeNo, 'numOfRows': numOfRows, '_type': _type}

        # URL만들기
        request_query = get_request_query(OPERATION1, OPERATION2, PARAMS, SERVICEKEY)
        #print('request_query:', request_query)

        # #GET
        response = requests.get(url = request_query)

        #상태 확인
        #print('status_code:' + str(response.status_code))

        r_dict = json.loads(response.text)
        r_response = r_dict.get("response")
        r_body = r_response.get("body")
        r_items = r_body.get("items")
        r_item = r_items.get("item")
        
        for item in r_item: #입력한 노드번호만 가져오기
            #print(item)
            try:
                if(item.get("routeno") == routeNo):
                    routeid = item.get("routeid")
                    routeno = item.get("routeno")
                    bus_routes_data.loc[idx] = [routeno, routeid]
                    #print( bus_routes_data.loc[idx])
                    idx += 1
            except:
                print("노선방면 한개인 노선: "+ str(routeNo))
                       
    except:
        print("api 문제")

#print(bus_routes_data)
#bus_routes_data.to_csv("../csv/route_id.csv", encoding='utf-8-sig')