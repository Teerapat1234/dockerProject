from urllib import request
from flask import Flask
from mathFunctions import getRegression, getValueDifference, getRSI, getMargin, getAffectedPointPrediction, getLinearFuncGraph
from finance import getPositionSize
from dataRetriever import get_binance_bars, jsonSave, jsonRead
from regularFunctions import getLowest, getHighest, plotLineData, getCutList, getAvg

import re, json, os, csv
from io import StringIO
from bs4 import BeautifulSoup
import requests                    # for "get" request to API
import pandas as pd                # working with data frames
import datetime as dt              # working with dates
import matplotlib.pyplot as plt    # plot data
import qgrid                       # display dataframe in notebooks
import urllib.request, time, difflib, itertools
from multiprocessing.dummy import Pool

app = Flask(__name__)

@app.route("/")
def index():
    return "It works"

@app.route("/predict/coin/")
def CoinData():
    query_string = request.query_string
    # jsonSave(CoinName)
    return "it works"

@app.route("/predict/")
def prediction():

    class coordinateElement:
        X, Y = 0, 0

    coordinate = []
    fullList, YcoordinateList = jsonRead("data") ######################### (list[class], list[float])
    XcoordinateList = []
    for i in range(len(YcoordinateList)):
        XcoordinateList.append(i+1)

    for i in range(len(YcoordinateList)):
        each = coordinateElement()
        each.X, each.Y = XcoordinateList[i], YcoordinateList[i] #Change this when the time comes
        coordinate.append(each)

    #######FUNCTIONS NOT-SUBJECTED TO CHANGE IN THE INPUT#############################
    # a_alldata, b_alldata = getRegression(coordinate) ######################### (float, float)
    Xdiff, Ydiff = getValueDifference(coordinate)  ######################### (list[int], list[int])
    rsi = getRSI(Ydiff)  ######################### (list[percentage])
    ##################################################################################

    ##################################################################################
    new_coordinate = getCutList(coordinate, 14) ######################### (list)
    a_recentdata, b_recentdata = getRegression(new_coordinate) ######################### (float, float)
    new_X = []
    for i in new_coordinate:
        new_X.append(i.X)
    # Append the new last x-coordinate, ready for the calculation of the next predicted point.
    new_X.append(int(new_X[-1] + getAvg(Xdiff))) ######################### (float) X-axis
    new_Y = getLinearFuncGraph(a_recentdata, b_recentdata, new_X) ######################### (list[float]) Y-axis
    upperQuartile, lowerQuartile = getMargin(Ydiff) ######################### (float, float) Y-axis
    newPredictedPointY = getAffectedPointPrediction(rsi[-1], new_Y[-1], upperQuartile, lowerQuartile) ######################### (float) Y-axis
    ##################################################################################

    ##################################################################################
    capital = 100 #ARBITRARILY SELECTED
    risk = rsi[len(rsi) - 1] - 50
    if risk > 0: #The rsi direction is in the upper margin.
        # This essentially means that only maximum of 50% "risk" is possible.
        Position_Size = getPositionSize(capital, risk, new_Y[-1], upperQuartile) ######################### (float) value
    else:   #The rsi direction is in the lower margin.
        risk = abs(risk)
        # This essentially means that only maximum of 50% "risk" is possible.
        Position_Size = getPositionSize(capital, risk, new_Y[-1], lowerQuartile) ######################### (float) value
    ##################################################################################

    plotLineData(XcoordinateList, YcoordinateList, new_X, new_Y, new_Y[-1] + upperQuartile, new_Y[-1] - lowerQuartile, newPredictedPointY) ######################### plot
    print("a,b", a_recentdata, b_recentdata)
    print("xdiff, ydiff", Xdiff[-5:], Ydiff[-5:])
    print("rsi", rsi[-5:])
    print("predict X, Y", new_X[-1], new_Y[-1])
    print("Quartile upper lower", upperQuartile, lowerQuartile)
    print("new predicted point", newPredictedPointY)
    print("position size", Position_Size)

    return "It works"

@app.route("/prediction/cardano")
def prediction_Finance():
    CARDANO_US_Stats = "https: // finance.yahoo.com / quote / ADA - USD?p = ADA - USD"
    CARDANO_US_HistoricalData = "https: // finance.yahoo.com / quote / ADA - USD?p = ADA - USD &.tsrc = fin - srch"


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')

    text = prediction()