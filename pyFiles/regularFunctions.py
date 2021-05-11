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


def plotLineData(X, Y, new_X, new_Y, Y_upper, Y_lower, newPredictedPointY):
    fig = plt.figure(facecolor='w')  # Plot the data on three separate curves for S(t), I(t) and R(t)
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.plot(X, Y, 'k', label='Actual Y-coordinates', linestyle='--', marker='o')
    ax.plot(new_X, new_Y, 'r', label='Linear regression')
    ax.scatter(new_X[-1], newPredictedPointY, color='y')
    ax.scatter(new_X[-1], Y_upper, color='b')
    ax.scatter(new_X[-1], Y_lower, color='b')
    ax.text(new_X[-1], newPredictedPointY, '({}, {})'.format(new_X[-1], round(newPredictedPointY, 3)))
    ax.text(new_X[-1], Y_upper, '({}, {})'.format(new_X[-1], round(Y_upper, 3)))
    ax.text(new_X[-1], Y_lower, '({}, {})'.format(new_X[-1], round(Y_lower, 3)))
    ax.set_xlabel('X')
    ax.set_ylabel('f(X)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    img_path = os.path.join("C:/Users/psyon/Desktop/work/", "graph.jpg")
    plt.savefig(img_path, bbox_inches="tight")

def getHighest(dataList):
    highest = dataList[0]
    for i in dataList:
        if i > highest:
            highest = i
    return highest

def getLowest(dataList):
    Lowest = dataList[0]
    for i in dataList:
        if i < Lowest:
            Lowest = i
    return Lowest

def getCutList(dataList, pointsTaken):
    pointsTaken = pointsTaken * -1
    return dataList[pointsTaken:]

def getAvg(dataList):
    sum = 0
    for i in dataList:
        sum = sum + i
    return sum/len(dataList)