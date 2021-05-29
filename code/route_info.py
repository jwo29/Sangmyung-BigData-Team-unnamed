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
OPERATION2 = 'getRouteInfoIem' 

# 서비스키
SERVICEKEY = "Ee5WLqN4iRCKuFUsxlAF1P9anyOX5vH%2BOFG2%2BYM%2BcEoNQOg9emMEyyKM37eAmmVnl1ZxgTalHHL90VNl1B1zlg%3D%3D"

bus_routes_data = pd.read_csv("route_id.csv")

bus_routes_schedule_data = pd.DataFrame(columns = ("routeid", "routeno", "startnodenm", "startvehicletime", "endnodenm", "endvehicletime", "intervaltime")) 

# 파라미터
cityCode  = 34010  # 
routeId = bus_routes_data["routeid"]
_type = "json"
numOfRows = 150
idx = 0

for idx in range(len(routeId)):
    
    PARAMS = {'cityCode':cityCode, 'routeId':routeId[idx], 'numOfRows': numOfRows, '_type': _type}

    # URL만들기
    request_query = get_request_query(OPERATION1, OPERATION2, PARAMS, SERVICEKEY)
    print('request_query:', request_query)

    # #GET
    response = requests.get(url = request_query)

    #상태 확인
    print('status_code:' + str(response.status_code))

    r_dict = json.loads(response.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_items = r_body.get("items")
    r_item = r_items.get("item")

    print(r_item)

    routeid = r_item["routeid"]
    routeno = r_item["routeno"]
    startnodenm = r_item["startnodenm"]
    startvehicletime = r_item["startvehicletime"]
    endnodenm = r_item["endnodenm"]
    endvehicletime = r_item["endvehicletime"]
    intervaltime = r_item["intervaltime"]

    bus_routes_schedule_data.loc[idx] = [routeid, routeno, startnodenm, startvehicletime, endnodenm, endvehicletime,intervaltime]

#bus_routes_schedule_data
#bus_routes_schedule_data.to_csv("route_info.csv", encoding='utf-8-sig')