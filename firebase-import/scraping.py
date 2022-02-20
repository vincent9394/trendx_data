# %%
import json
from tokenize import group
import numpy as np
import time
import pandas as pd
# %% read json file
f=open('./mock_stock_data.json', encoding="utf8")
# f=open('./2019_01_02 to 2022_02_13_copy.json', encoding="utf8")
# f=open('./2019_01_02 to 2022_02_13.json', encoding="utf8")
# f=open('./2019_01_02_to_2021_08_12_copy.json', encoding="utf8")

data = json.load(f)
stockDataList =data['trendX_data_v5']

def toPandasDf(array):
    df = pd.DataFrame(data=array)
    return df

df_stocklist=toPandasDf(stockDataList)
df_stocklist
# sorting
df_stocklist.sort_values(by="timestamp",ascending=True)
df_stocklist



# %%

df_stocklist = df_stocklist[["ticker","date","timestamp","chinese_name","sector","signal"]]
df_stocklist

# %%
df_date=df_stocklist['date'].unique().tolist()
df_ticker=[["00001","00004"],"00002","00003"]
df_date.append("123")
print(df_date[0])
dict_date = dict(zip(df_date, df_ticker))
print(dict_date)


# %% spilt to date array
array_by_date=[] 
temp_time =0
temp_array =[]
for index,row in df_stocklist.iterrows():    
    if (temp_time == row["timestamp"]):      # for the first date
        temp_array.append([row])
        if (index == len(df_stocklist)-1):   # for latest date
            array_by_date.append(temp_array)
    if (temp_time != row["timestamp"]):       # for the next date
        if (temp_array !=[] ):
            array_by_date.append(temp_array)
            temp_array = []
            temp_array.append([row])
        else:                 # for the first row of data 
            temp_array.append([row])
        temp_time =row["timestamp"]

# %%
print(array_by_date)




# %%
def find_index(array,ticker):
    for i in range(len(array)):
            if (array[i]["ticker"] == ticker):
               index=i
               print(index, array[i]["ticker"], ticker)
               return index
               
# %% function for up_down_trend
def filter_trend(array_1, array_2):

    for row in array_1:
        # find_index(array_1,row["ticker"])
        for compare_row in array_2:
            # find_index(array_1,row["ticker"])
            if(row["ticker"]==compare_row["ticker"]):
                deleteIndex=find_index(array_1,row["ticker"])
                array_1.pop(deleteIndex)   

# %% calculate the up /down trend
# group = {
#     "upTrendStock":[],
#     "downTrendStock":[]
# }

group = {
    "upTrendStock":[],
    "downTrendStock":[]
}

for i in range(len(array_by_date)):
    for j in range(len(array_by_date[i])):
        for row in array_by_date[i][j]:
            print(row["date"])
            if (row["signal"] == "UP"):
                group["upTrendStock"].append(row)
                if ( len(group["upTrendStock"]) !=0):
                    filter_trend(group["downTrendStock"],group["upTrendStock"])

            if (row["signal"] == "DOWN"):
                group["downTrendStock"].append(row)
                if (len(group["downTrendStock"]) !=0): # filtering opposite trend
                    filter_trend(group["upTrendStock"],group["downTrendStock"])


# %%
print(len(group["upTrendStock"]))  # 16
print(len(group["downTrendStock"])) #24
 
# %% Count the value of continous date for the chart
def countContinousDate(array):
    latestTimestamp=array_by_date[len(array_by_date)-1][0][0]["timestamp"]
    for row in array:
        count_date = 1+(latestTimestamp-row["timestamp"])/86400
        row["count_date"]=count_date

countContinousDate(group["upTrendStock"])
countContinousDate(group["downTrendStock"])

# %% Check Uptrend Results
df_upTrend=pd.DataFrame(data=group["upTrendStock"])
df_upTrend.reset_index()  
# %% Check Downtrend Results
df_downTrend=pd.DataFrame(data=group["downTrendStock"])
df_downTrend.reset_index()

# %% output to json
# for windows
df_upTrend.to_json(r'.\uptrend_data_output.json',  orient='records')
df_downTrend.to_json(r'.\downtrend_data_output.json',  orient='records')

# %%
# for linux
df_upTrend.to_json(r'./uptrend_data_output.json',  orient='records')
df_downTrend.to_json(r'./downtrend_data_output.json',  orient='records')
# %%
