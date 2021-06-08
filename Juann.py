import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#load directory
dir_loc_1 = os.listdir("/Users/kimjuann/Downloads/Sangmyung_BigData_Team_J-AWS-main 2/Stage_1_1")
location = "/Users/kimjuann/Downloads/Sangmyung_BigData_Team_J-AWS-main 2/Stage_1_1/"

dic = {}
for file_name in dir_loc_1:
    file_name = location +  file_name #make a path
    csv_file = pd.read_csv(file_name)

    routeId = csv_file["routeid"]
    arrTime = csv_file["arrtime"]

    for index in range(0, len(routeId), 2):
        if routeId[index] not in dic:
            dic[routeId[index]] = list()
        dic[routeId[index]].append(abs(arrTime[index] - arrTime[index + 1]))

average_by_routeId = {}

for key in dic:
    average_by_routeId[key] = sum(dic[key]) / len(dic[key])

###

mine_dir_loc = os.listdir("/Users/kimjuann/Downloads/Sangmyung_BigData_Team_J-AWS-main 2/mine")
mine_dir_loc.sort()
location = "/Users/kimjuann/Downloads/Sangmyung_BigData_Team_J-AWS-main 2/mine/"

original_average = {}
for file_name in mine_dir_loc:
    file_name = location + file_name
    csv_file = pd.read_csv(file_name)

    average = csv_file["Average"]
    original_average[file_name[-16:-4]] = (average[0] + average[1]) / 2


index = np.arange(len(original_average))
plt.title("Compare (Stage1-1) and (Stage1, 2)")


print(original_average)
plt.bar(index, list(average_by_routeId.values()), 0.2, label="Stage1-1")
plt.bar(index+0.2, list(original_average.values()), 0.2, label="Stage1, 2")
plt.xticks(index, original_average)
plt.yticks(list(average_by_routeId.values()))
plt.ylabel("arrTime")
plt.xlabel("routeId")
plt.show()
plt.savefig("/Users/kimjuann/Library/Mobile Documents/com~apple~CloudDocs/2021-1/빅데이터개론/Project/compare_stage_1_1.png")


'''
#load directory
dir_loc_2 = os.listdir("/Users/kimjuann/Downloads/Sangmyung_BigData_Team_J-AWS-main 2/Stage_2_1")
location = "/Users/kimjuann/Downloads/Sangmyung_BigData_Team_J-AWS-main 2/Stage_2_1/"

dic = {}
for file_name in dir_loc_2:
    file_name = location +  file_name #make a path
    csv_file = pd.read_csv(file_name)

    routeId = csv_file["routeid"]
    arrTime = csv_file["arrtime"]

    for index in range(0, len(routeId), 2):
        if routeId[index] not in dic:
            dic[routeId[index]] = list()
        dic[routeId[index]].append(abs(arrTime[index] - arrTime[index + 1]))

average_by_routeId = {}

for key in dic:
    average_by_routeId[key] = sum(dic[key]) / len(dic[key])
print(average_by_routeId)

plt.bar(average_by_routeId.keys(), average_by_routeId.values())
for i, v in enumerate(average_by_routeId.keys()):
    plt.text(v, average_by_routeId[v], average_by_routeId[v],
    fontsize = 9, color='blue', horizontalalignment='center', verticalalignment='bottom')
plt.show()
'''
