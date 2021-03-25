import json 
import requests
import os
import time
import datetime
base_link = 'https://api-public.sandbox.pro.coinbase.com'
request_link = 'https://api-public.sandbox.pro.coinbase.com/products'

#https://api-public.sandbox.pro.coinbase.com
g_master = 0

def GetMasterList():
    global g_master
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

def WriteFile(data, product_id, description):
    if description:
        description = "_"+description
    time = requests.get(f'{base_link}/time').json()
    dt_time =  datetime.datetime.fromtimestamp(time['epoch'])#datetime.datetime.strptime(time['iso'], '%Y-%m-%d %I:%M%p')
    description += "_"+dt_time.strftime("%Y_%m_%d_%H_%M_%S_%f")+".json"
    file_name = f'./data/{product_id}/{product_id}{description}'
    file_name = file_name.replace("-","_")
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except:
            raise
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

GetMasterList()
for i in g_master:
    GetIndividualProductInfo(i['id'])
    for j in range(1,4):
        GetIndividualProductBook(i['id'],j)
        time.sleep(2)
    GetIndividualProductTrades(i['id'])
    GetIndividualProductTicker(i['id'])
    GetIndividualProductCandles(i['id'])
    