'''
    Name: coinbase_get.py

    Purpose: Script to get rest API data from coin base and store in json files

    Version | Author  | Date       | Comment
    V1      | Shivank | 03/25/2021 | Wrote script for all sandbox get requests, will look into websocket next

'''

import json 
import requests
import os
import time
import datetime
import pandas as pd
machine = 1 
base_link = 'https://api-public.sandbox.pro.coinbase.com'
request_link = 'https://api-public.sandbox.pro.coinbase.com/products'
target_lin = '/home/shivank/tech/ref/crypto/shivank_coinbase/Cryptocurrency/'
tartget_win = "C:\\personal\\Programming\\Quant\\Cryptocurrency\\"
#https://api-public.sandbox.pro.coinbase.com

def GetMasterList():
    r = requests.get(request_link)
    g_master = r.json()
    return g_master

def GetIndividualProductInfo(product_id:str):
    request_response = requests.get(f'{request_link}/{product_id}')
    individual_info = request_response.json()
    WriteFile(individual_info, product_id, "")
    #print(individual_info)
    return individual_info

def GetIndividualProductBook(product_id : str, level = 1):
    request_response = requests.get(f'{request_link}/{product_id}/book?level={level}')
    individual_info = request_response.json()
    WriteFile(individual_info, product_id, f"book_L{level}")
    #print(individual_info)
    return individual_info

def GetIndividualProductTicker(product_id : str):
    request_response = requests.get(f'{request_link}/{product_id}/ticker')
    individual_info = request_response.json()
    WriteFile(individual_info, product_id, "ticker")
    #print(individual_info)
    return individual_info

def GetIndividualProductTrades(product_id : str):
    request_response = requests.get(f'{request_link}/{product_id}/trades')
    individual_info = request_response.json()
    WriteFile(individual_info, product_id, "trades")
    #print(individual_info)
    return individual_info

def GetIndividualProductCandles(product_id : str, start = '', end = '', granularity = 60):
    request_response = requests.get(f'{request_link}/{product_id}/candles?{{start={start}}}?{{end={end}}}?{{granularity={granularity}}}')
    individual_info = request_response.json()
    #print(individual_info)
    WriteFile(individual_info, product_id, "candles")
    return individual_info

def GetIndividualProductStats(product_id : str):
    request_response = requests.get(f'{request_link}/{product_id}/stats')
    individual_info = request_response.json()
    WriteFile(individual_info, product_id, "stats")
    #print(individual_info)
    return individual_info

def WriteFile(data, product_id, description):
    target = target_lin
    if(machine == 1):
        target = tartget_win
    if description:
        description = "_"+description
    time = requests.get(f'{base_link}/time').json()
    dt_time =  datetime.datetime.fromtimestamp(time['epoch'])#datetime.datetime.strptime(time['iso'], '%Y-%m-%d %I:%M%p')
    
    description += "_"+dt_time.strftime("%Y%m%d_%H%M%S")
    
    file_name = f'{target}/shivank_restdata/{product_id}/{product_id}{description}.json'
    #file_name = file_name.replace("-","_")
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except:
            raise
    with open(file_name, 'w+') as outfile:
        json.dump(data, outfile)
    

    df = pd.DataFrame([data])
    file_name = f'{target}/shivank_restdata_csv/{product_id}/{product_id}{description}.csv'
    #file_name = file_name.replace("-","_")
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except:
            raise
    export_csv = df.to_csv (file_name, index = None, header=True)

def Run():
    g_master = GetMasterList()
    for i in g_master:
        GetIndividualProductInfo(i['id'])
        for j in range(1,4):
            GetIndividualProductBook(i['id'],j)
            time.sleep(1)
        GetIndividualProductTrades(i['id'])
        GetIndividualProductTicker(i['id'])
        GetIndividualProductCandles(i['id'])
        GetIndividualProductStats(i['id'])
        print(f'finished: {i["id"]}')
Run()
