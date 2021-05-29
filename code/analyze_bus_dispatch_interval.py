# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# In[2]:


df = pd.read_csv("../csv/data_table.csv")
print(df)


# In[3]:


plt.imshow(df)


# In[4]:


# 데이터 칼럼,인덱스 이름 변경
df.index = ["Stage1", "Stage2", "Stage3", "Stage4"]
df.columns = ["11(CAB285000006)","11(CAB285000007)","12(CAB285000008)","12(CAB285000009)","13(CAB285000010)","13(CAB285000011)","14(CAB285000012)","14(CAB285000013)","24(CAB285000024)","24(CAB285000025)","81(CAB285000293)","81(CAB285000294)", "STAGE TOTAL AVERAGE"]
df.columns.names = ["bus_num(routeid)"]


# ## Average of dispatch intervals by time zone

# In[5]:


# total
ax = df.plot(kind="bar", title = "Total Bus Stage Average Interval Time",width=0.5,figsize=(15,6))
plt.ylabel("average Intervaltime")
plt.xticks(rotation=0)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig('../image/bus_average_Interval_time_grap_total.png',dpi=200,transparent=True,bbox_inches='tight') # 그래프 이미지로 저장


# In[6]:


# stages
for stage in df.index:
    #print(stage)
    s = df.loc[[stage],:]
    ax = s.plot(kind="bar", title = stage+" Bus Average Interval Time",width=3.0, figsize=(10,6))
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate("%.1f"%(height), (left+width/2, height*1.01), ha='center')

    plt.ylabel("average Intervaltime")
    plt.xticks(rotation=0)

    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    plt.savefig('../image/bus_average_Interval_time_grap_'+stage+'.png',dpi=100,transparent=True,bbox_inches='tight')


# In[7]:


path =  "../mine"
file_list = os.listdir(path)
print(file_list)


# ## Comparison of dispatch intervals by bus

# In[8]:


route_info = pd.read_csv('../csv/route_info.csv')
interval_times = route_info['intervaltime']


# In[9]:


df = df.drop("STAGE TOTAL AVERAGE", axis =1)


# In[10]:


time_gap_df = pd.DataFrame(columns=["specified time", "actual Time"])


# In[11]:


for i, c in enumerate(df.columns):
    time_gap_df.loc[i] = [interval_times[i], df[c].mean()/60]

time_gap_df.index = ["11(CAB285000006)","11(CAB285000007)","12(CAB285000008)","12(CAB285000009)","13(CAB285000010)","13(CAB285000011)","14(CAB285000012)","14(CAB285000013)","24(CAB285000024)","24(CAB285000025)","81(CAB285000293)","81(CAB285000294)"]
print(time_gap_df)   


# In[12]:


ax = time_gap_df.plot(kind="bar", title = "Compare interval times for all buses",width=0.5,figsize=(15,6))
plt.ylabel("Intervaltime")
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig('../image/Compare_interval_times_for_all_buses.png',dpi=200,transparent=True,bbox_inches='tight')


# In[13]:


# route
for route in time_gap_df.index:
    #print(route)
    s = time_gap_df.loc[[route],:]
    ax = s.plot(kind="bar", title = route+" Bus Average Interval Time",width=0.2, figsize=(6,5))
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate("%.1f"%(height), (left+width/2, height*1.01), ha='center')

    plt.ylabel("average Intervaltime")
    plt.xticks(rotation=0)

    #plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    plt.savefig('../image/Compare_interval_times_for_'+route+'.png',dpi=100,transparent=True,bbox_inches='tight')
    


# ## analysis interval impact stage

# In[14]:


print(interval_times)


# In[15]:


route_info = pd.read_csv('../csv/route_info.csv')
bus_timegap_file_list = os.listdir('../mine')

interval_times = route_info['intervaltime']
for i, file in enumerate(bus_timegap_file_list):
    bus = pd.read_csv('../mine/' + file)
    bus_intervaltime = interval_times[i] # 현재 버스의 배차 간격 추출
    
    bus_interval_comp = list()
    
    for stage in range(4):
        time_gap_str = bus.iloc[stage, 1] # time gap 추출
        time_gap = list(map(int, time_gap_str[1:-1].split(', '))) # str -> int 형 리스트로 변환
        
        for gap in range(len(time_gap)):
            time_gap[gap] -= bus_intervaltime*60
        
        bus_interval_comp.append(time_gap)
       
    plt.subplots(figsize=(5, 5))
    
    plt.hist(bus_interval_comp[0], alpha=0.25)
    plt.hist(bus_interval_comp[1], alpha=0.25)
    plt.hist(bus_interval_comp[2], alpha=0.25)
    plt.hist(bus_interval_comp[3], alpha=0.25)
    
    plt.xticks(np.arange(-1500, 2500, 500))
    
    plt.title(file[:-4])
    
    if i == 0:
        plt.xlabel('Time difference between specifed interval')
        plt.legend(['7:00~9:00', '12:00~14:00', '17:00~19:00', '20:00~22:00']) # 첫번째 그래프에 어느 것이 malignant인지, benign인지 표시
    
    plt.savefig('../image/analysis_interval_impact_'+file[:-4]+'.png') # 그래프 이미지로 저장

