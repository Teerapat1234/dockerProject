import requests                    # for "get" request to API
import pandas as pd                # working with data frames
import datetime as dt              # working with dates
import matplotlib.pyplot as plt    # plot data
import qgrid                       # display dataframe in notebooks
import urllib.request, json , time, os, difflib, itertools
from multiprocessing.dummy import Pool
import re
import csv
from io import StringIO
from bs4 import BeautifulSoup
# from PIL import Image
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

def get_binance_bars(symbol, interval, startTime, endTime):
    url = "https://api.binance.com/api/v3/klines"
    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'
    req_params = {"symbol": symbol, 'interval': interval, 'startTime': startTime, 'endTime': endTime, 'limit': limit}
    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))
    if (len(df.index) == 0):
        return None
    df = df.iloc[:, 0:6]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.open = df.open.astype("float")
    df.high = df.high.astype("float")
    df.low = df.low.astype("float")
    df.close = df.close.astype("float")
    df.volume = df.volume.astype("float")

    df['adj_close'] = df['close']

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]

    return df

def jsonSave(symbol, interval, startTime, endTime):
    df = get_binance_bars(symbol, interval, startTime, endTime)
    #df = get_binance_bars('BTCUSDT', '1h', dt.datetime(2021, 5, 9), dt.datetime(2021, 5, 10))
    js = str(df.to_json(orient = 'records'))
    data = js[1:-2]
    data = data.split("},")

    DataArr = []
    for i in data:
        box = i.split(",")
        x = {"Open": box[1][7:], "High": box[2][7:], "Low": box[3][6:], "Close": box[4][8:], "Volume": box[5][9:], "Adj_close": box[6][12:]}
        DataArr.append(x)

    log_file = "data" + '.json'
    with open(log_file, "w") as file:
        json.dump(DataArr, file, indent=4)
    return None

def jsonRead(filename):
    with open(filename + '.json') as file:
        data = json.load(file)
    data = json.dumps(data)
    data = data[1:-2]
    data = data.split("}, ")

    class row:
        Open, High, Low, Close, Volume, Adj_close = 0, 0, 0, 0, 0, 0

    rowList, CloseList = [], []
    for i in data:
        x, element = row(), i.split(",")
        x.Open, x.High, x.Low, x.Close, x.Volume, x.Adj_close = float(element[0][10:-1]), float(element[1][10:-1]), float(element[2][9:-1]), float(element[3][11:-1]), float(element[4][12:-1]), float(element[5][15:-1])
        CloseList.append(float(element[3][11:-1]))
        rowList.append(x)

    # print(CloseList, rowList)
    return rowList, CloseList
