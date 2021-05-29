import numpy as np
import pandas as pd

bus_route_data = pd.read_csv("route_id.csv")

bus_route_no = bus_route_data["routeno"]
bus_route_id = bus_route_data["routeid"]

bus_nodeord = np.array([["늘푸른극동아파트","천안역 서부광장", "동남구청", "단국대학교", "두정우남아파트"], #11
                        ["주공8단지아파트", "단국대 삼거리", "남산축협", "성정초등학교", "두정한성아파트"],#11
                        ["방아다리공원", "5단지시장입구", "삼룡교", "부영아파트", "NULL"], #12
                        ["부영아파트", "삼룡교", "주공5단지아파트", "방아다리공원", "NULL"], #12
                        ["종합터미널", "충무병원정문", "천안아산역", "NULL", "NULL"], #13
                        ["두레현대1단지아파트", "중앙도서관", "단대병원", "NULL", "NULL"], #13
                        ["천안시청 서북구보건소", "두정중학교", "신부청광아파트", "백석대학교(운동장)", "NULL"], #14
                        ["신부청광아파트", "두정도서관", "주공그린빌3차아파트", "방아다리공원", "NULL"], #14
                        ["종합터미널", "삼룡교", "동우아파트", "NULL", "NULL"], #24
                        ["천안동중학교", "복자여자중고등학교", "각원사", "NULL", "NULL"], #24
                        ["동아태조아파트", "계룡리슈빌", "차암2통", "NULL", "NULL"],#81
                        ["백석푸르지오아파트", "역말오거리", "각원사", "NULL", "NULL"]]) #81


data = pd.DataFrame(columns = ("routeno", "routeid", "stop1",  "stop2",  "stop3",  "stop4",  "stop5")) 
idx = 0
for _ in range(len(bus_route_no)):
    routeno = bus_route_no[idx]
    routeid = bus_route_id[idx]
    stop1 = bus_nodeord[idx, 0]
    stop2 = bus_nodeord[idx, 1]
    stop3 = bus_nodeord[idx, 2]
    stop4 = bus_nodeord[idx, 3]
    stop5 = bus_nodeord[idx, 4]
    data.loc[idx] = [ routeno, routeid, stop1, stop2, stop3, stop4, stop5 ]
    idx += 1
data.to_csv("stop_name.csv", encoding='utf-8-sig', index=False)