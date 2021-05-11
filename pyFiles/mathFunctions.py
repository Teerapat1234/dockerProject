def getValueDifference(coordinate):
    Xdiff, Ydiff, Xpoint, Ypoint = [], [], 0, 0
    for i in range(1, len(coordinate)):
        Xdiff.append(coordinate[i].X - coordinate[i-1].X)
        Ydiff.append(coordinate[i].Y - coordinate[i-1].Y)
    return Xdiff, Ydiff

def getRegression(coordinate):
    n, SUMxy, SUMx, SUMx2, SUMy = len(coordinate), 0, 0, 0, 0
    for i in coordinate:
        x, y = i.X, i.Y
        SUMx, SUMy, SUMx2, SUMxy = SUMx + x, SUMy + y, SUMx2 + (x * x), SUMxy + (x * y)
    try:
        b = (n * SUMxy) - (SUMx * SUMy)
        b = b / ((n * SUMx2) - (SUMx * SUMx))
    except:
        b = 1.0
    #f(x) = a + bx
    Meanx, Meany = SUMx/n, SUMy/n
    a = Meany - b * Meanx
    return a, b

def getRSI(difference):
    up, down, rsi, loopNum = 0, 0, [], int(len(difference)/14)
    loop, i, cut = 14, 0, difference[0] #cut will change to the first value of every 14 blocks, and will be used to subract the sum when the next block arrives.
    while i < 14:      #This will run throuhg the first 14 elements in the first block
        if difference[i] < 0:
            up = up + difference[i]
        elif difference[i] > 0:
            down = down + difference[i]
        i += 1
    rsi.append(100 - 100/(1 + (up / (-1 * down))))
    if cut > 0:     #this essentially take the first value of each block away for the next block calculation  [cut(1)[rest(13)]]
        up = up - cut
    elif cut < 0:
        down = down - cut

    while loop < len(difference):   #this will run the rest by going 1 step each
        cut = difference[loop - 13]
        if difference[loop] > 0:
            up = up + difference[loop]
        elif difference[loop] < 0:
            down = down + difference[loop]
        rsi.append(100 - 100/(1 + (up / (-1 * down))))
        if cut > 0:     #this essentially take the first value of each block away for the next block calculation  [cut(1)[rest(13)]]
            up = up - cut
        elif cut < 0:
            down = down - cut
        loop += 1
    return rsi

def getLinearFuncGraph(a, b, dataList):
    linear = []
    for data in dataList:
        linear.append(a + (b * data))
    return linear

def getMargin(Ydiff):
    up, down = 0, 0
    for i in range(len(Ydiff)):
        if Ydiff[i] > 0:
            up = up + Ydiff[i]
        elif Ydiff[i] < 0:
            down = down + Ydiff[i]
    return up/len(Ydiff), abs(down)/len(Ydiff)

def getAffectedPointPrediction(rsi, predictedPoint, upperQuartile, lowerQuartile):
    rsi = rsi - 50
    if rsi > 0:
        rsi = rsi * 2
        margin = upperQuartile * (rsi/100)
        predictedPoint = predictedPoint + margin
    elif rsi < 0:
        rsi = rsi * -2
        margin = lowerQuartile * (rsi/100)
        predictedPoint = predictedPoint - margin
    return predictedPoint