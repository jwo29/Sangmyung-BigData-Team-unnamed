
# In[1]:


import os
import pandas as pd
import math
import numpy as np


# In[2]:


routeid_list = ["CAB285000006",
                "CAB285000007",
                "CAB285000008",
                "CAB285000009",
                "CAB285000010",
                "CAB285000011",
                "CAB285000012",
                "CAB285000013",
                "CAB285000024",
                "CAB285000025",
                "CAB285000293",
                "CAB285000294"]

dir_list = ["../Stage_1", "../Stage_2", "../Stage_3", "../Stage_4"]

for r_id in routeid_list:
    bus_dic = {}
    bus_df = pd.DataFrame(columns=['Stage', 'Time gap', 'Average'])
    
    for idx, directory in enumerate(dir_list):
        path =  directory 
        file_list = os.listdir(path)

        bus_dic[directory] = []
        
        for file in file_list:

            df = pd.read_csv(path+"/"+file)
            curr_bus = df[df["routeid"] == r_id]
            
            for i in range(0, len(curr_bus), 2):
                gap = curr_bus.iloc[i+1, 6] - curr_bus.iloc[i, 6]
                bus_dic[directory].append(abs(gap))

        bus_df.at[idx, "Stage"] = idx + 1
        bus_df.at[idx, "Time gap"] = bus_dic[directory]
        bus_df.at[idx, "Average"] = np.mean(bus_dic[directory])

    file_name = "../mine/"+r_id +".csv"
    bus_df.to_csv(file_name, index=False, mode='w', encoding='utf-8-sig')


# In[20]:


total_averages = pd.DataFrame(columns=["CAB285000006","CAB285000007","CAB285000008","CAB285000009","CAB285000010","CAB285000011","CAB285000012","CAB285000013","CAB285000024","CAB285000025","CAB285000293","CAB285000294"],index=["Stage1","Stage2","Stage3","Stage4"])


# In[22]:


path =  "../mine"
file_list = os.listdir(path)


# In[23]:


for i in range(1,len(file_list)):
    temp = pd.read_csv("../mine/"+file_list[i])
    r_id = file_list[i][:-4]

    total_averages[r_id][0] = (temp["Average"][0])
    total_averages[r_id][1] = (temp["Average"][1])
    total_averages[r_id][2] = (temp["Average"][2])
    total_averages[r_id][3] = (temp["Average"][3])

total_averages["total_average"] = total_averages.mean(axis=1)
total_averages.to_csv("../csv/data_table.csv", index=False, mode='w', encoding='utf-8-sig')
#     aver_col = temp['Average']
#     temp_df = pd.DataFrame(aver_col, columns=[r_id])
    


# %%
