def getPositionSize(Capital, Risk, Entry, Stop):
    DistanceToStop = 100 * (abs(Stop - Entry)) / Stop
    return (Capital * (Risk / 100))/DistanceToStop
