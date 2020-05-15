# from analysis_utils import *
# import numpy as np
from talib import BBANDS, SMA, RSI, STOCH, MINUS_DI, PLUS_DI
from utils import *
from numpy import array, double
from StockData import TickInfoEnum

# def boolChannel(price, stock_name, t): 
#     priceIn5m = getTicksWithInterval(price, 5)
#     highPriceIn5m = [p[1] for p in priceIn5m]
#     lowPriceIn5m = [p[2] for p in priceIn5m]
#     closePriceIn5m = [p[3] for p in priceIn5m]
#     upperBand, middleBand, lowerBand = BBANDS(array(closePriceIn5m, dtype=double), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    
#     if len(closePriceIn5m) < 3 or isNaN(upperBand[-3]):
#         return []

#     signal = []
#     if closePriceIn5m[-3] <= upperBand[-3] and closePriceIn5m[-2] >= upperBand[-2] and highPriceIn5m[-2] <= closePriceIn5m[-1]:
#         s = "【布林向上突破】 股票代號: %s 突破點: %.2d:%.2d"%(stock_name, t//60, t%60)
#         signal.append(s)
#     elif closePriceIn5m[-3] >= lowerBand[-3] and closePriceIn5m[-2] <= lowerBand[-2] and lowPriceIn5m[-2] >= closePriceIn5m[-1]:
#         s = "【布林向下突破】 股票代號: %s 突破點: %.2d:%.2d"%(stock_name, t//60, t%60)
#         signal.append(s)
#     return signal 

# def doubPeriod(ticks, shortTermInterval, longTermInterval, shortTermMAPeriod, longTermMAPeriod, stockNum): 
#     shortTermTicks = getTicksWithInterval(ticks, shortTermInterval)
#     longTermTicks = getTicksWithInterval(ticks, longTermInterval)

#     shortTermClose = [p[PriceInfoEnum.Close] for p in shortTermTicks]
    
#     rsi = RSI(array(shortTermClose, dtype=double), timeperiod=9)
#     if len(rsi) == 0 or isNaN(rsi[-1]):
#         return []

#     if longTermMAPeriod > len(longTermTicks):
#         return []

#     isLongTermTicksGC = sum(longTermTicks[-shortTermMAPeriod:]) >= sum(longTermTicks[-longTermMAPeriod:])
#     isShortTermTicksGC = sum(shortTermTicks[-shortTermMAPeriod:]) >= sum(shortTermTicks[-longTermMAPeriod:])

#     signal = []  
#     if rsi[-1] > 0.5and isShortTermTicksGC and isLongTermTicksGC:
#         timestamp = ticks[-1][PriceInfoEnum.Time].strip()
#         s = "【雙週期上升】 股票代號 : %s %s"%(stockNum, timestamp)
#         signal.append(s)
#     elif rsi[-1] < 0.5 and (not isShortTermTicksGC) and (not isLongTermTicksGC):
#         timestamp = ticks[-1][PriceInfoEnum.Time].strip()
#         s = "【雙週期下降】 股票代號: %s %s"%(stockNum, timestamp)
#         signal.append(s)

#     return signal 

INVALID_PRICE = -1
def MADirection(price, period):
    addedIdx = -1
    removedIdx = -1-period
    
    if len(price) < -removedIdx or price[removedIdx] == INVALID_PRICE:
        return "Invalid"

    if price[removedIdx] < price[addedIdx]:
        return "Up"

    if price[removedIdx] >= price[addedIdx]:
        return "Down"

def MASync(stock, interval): 
    currentTicks = stock.currentTicks.getTicksWithInterval(interval)
    totalTicks = stock.totalTicks.getTicksWithInterval(interval)
    stockNum = stock.stockNum

    if totalTicks.getNum() == 0 or currentTicks.getNum() == 0:
        return []
    
    # MA60 = SMA(array(totalTicks.closes, dtype=double), 60)
    # MA20 = SMA(array(totalTicks.closes, dtype=double), 20)
    # MA10 = SMA(array(totalTicks.closes, dtype=double), 10)

    RSI_PERIOD = 9
    if len(totalTicks.closes) < RSI_PERIOD*2+1 or INVALID_PRICE in totalTicks.closes[-RSI_PERIOD*2-1:]:
        return []

    RSICloses = []
    for idx in range(len(totalTicks.closes)-1,-1,-1):
        if totalTicks.closes[idx] != -1:
            RSICloses.append(totalTicks.closes[idx])
        else:
            lastClose = RSICloses[-1]
            for i in range(20):
                RSICloses.append(lastClose+(i%2==1))
            break

    RSICloses = RSICloses[::-1]

    rsi = RSI(array(RSICloses, dtype=double), timeperiod=RSI_PERIOD)
    

    signal = []  

    MA60Direction = MADirection(totalTicks.closes, 60)
    MA20Direction = MADirection(totalTicks.closes, 20)
    MA10Direction = MADirection(totalTicks.closes, 10)

    if MA60Direction == "Up" and MA20Direction == "Up" and MA10Direction == "Up" and rsi[-2] < 50 and rsi[-1] > 50:
        timestamp = currentTicks.times[-1].strip()
        s = "【均線多頭排列】 股票代號 : %s %s"%(stockNum, timestamp)
        signal.append(s)

    if MA60Direction == "Down" and MA20Direction == "Down" and MA10Direction == "Down" and rsi[-2] > 50 and rsi[-1] < 50:
        timestamp = currentTicks.times[-1].strip()
        s = "【均線空頭排列】 股票代號 : %s %s"%(stockNum, timestamp)
        signal.append(s)

    return signal 

def curve(stock, interval):
    stockNum = stock.stockNum
    ticks = stock.currentTicks

    ticks = ticks.getTicksWithInterval(interval)
    if ticks.getNum() == 0:
        return []
    
    smallPeriod = 3
    bigPeriod = 5

    shortTermCloseMA = SMA(array(ticks.closes, dtype=double), smallPeriod)
    longTermLowMA = SMA(array(ticks.lows, dtype=double), bigPeriod)
    longTermHighMA = SMA(array(ticks.highs, dtype=double), bigPeriod)

    if len(longTermHighMA) < 3*bigPeriod or INVALID_PRICE in ticks.closes[-3*bigPeriod:]:
        return []

    signal = []

    isMAGC = shortTermCloseMA[-1] >= longTermLowMA[-1] and shortTermCloseMA[-2] <= longTermLowMA[-2]
    isMADC = shortTermCloseMA[-1] <= longTermHighMA[-1] and shortTermCloseMA[-2] >= longTermHighMA[-2]

    isShortTermMAUp = shortTermCloseMA[-2] <= shortTermCloseMA[-1]
    isShortTermMADown = shortTermCloseMA[-2] >= shortTermCloseMA[-1]
    isLongTermHighMAUp = longTermHighMA[-2] <= longTermHighMA[-1]
    isLongTermLowMADown = longTermLowMA[-2] >= longTermLowMA[-1]

    if ticks.opens[-1] <= ticks.closes[-1]:      
        isBelowInRow = ticks.closes[-2] <= longTermLowMA[-2] and ticks.closes[-3] <= longTermLowMA[-3]
        if isMAGC and isShortTermMAUp and isLongTermLowMADown and isBelowInRow:
            timestamp = ticks.times[-1].strip()
            s = "【彎道向上-%d分K】 股票代號: %s %s"%(interval, stockNum, timestamp)
            signal.append(s)

    else:           
        isAboveInRow = ticks.closes[-2] >= longTermHighMA[-2] and ticks.closes[-3] >= longTermHighMA[-3]
        if isMADC and isShortTermMADown and isLongTermHighMAUp and isAboveInRow:
            timestamp = ticks.times[-1].strip()
            s = "【彎道向下-%d分K】 股票代號: %s %s"%(interval, stockNum, timestamp)
            signal.append(s)

    return signal

def nType(stock): 
    stockNum = stock.stockNum
    times = stock.currentTicks.times
    bound = stock.getHistoryTicks().getTickByIdx(-1)[TickInfoEnum.Close]
    currentTicks = stock.currentTicks
    totalTicks = stock.totalTicks

    peakIdx, bottomIdx = getPeakBottom(currentTicks)  

    if len(totalTicks.lows) < 14 or INVALID_PRICE in totalTicks.closes[-14:]:
        return []
    K, _ = STOCH(array(totalTicks.highs, dtype=double), array(totalTicks.lows, dtype=double), array(totalTicks.closes, dtype=double))
    DI_MINUS = MINUS_DI(array(totalTicks.highs, dtype=double), array(totalTicks.lows, dtype=double), array(totalTicks.closes, dtype=double))
    DI_PLUS = PLUS_DI(array(totalTicks.highs, dtype=double), array(totalTicks.lows, dtype=double), array(totalTicks.closes, dtype=double))

    signal = [] 
    if (K[-1] < 20) and (DI_PLUS[-1] >= DI_MINUS[-1]):
        signalUp = nTypeL1Up(times, currentTicks, peakIdx, bottomIdx, stockNum=stockNum, lowerBound=bound)
        signal += signalUp
    if (K[-1] > 80) and (DI_PLUS[-1] <= DI_MINUS[-1]):
        signalDown = nTypeL1Down(times, currentTicks, peakIdx, bottomIdx, stockNum=stockNum, upperBound=bound)
        signal += signalDown
    return signal

def getPeakBottom(ticks):

    peakIdx, bottomIdx = [], []
    for idx in range(1, len(ticks.highs)-1):
        if ticks.closes[idx] == INVALID_PRICE:
            peakIdx, bottomIdx = [], []
        elif isBiggerThanNeigbor(ticks.highs, idx, "left") and isBiggerThanNeigbor(ticks.highs, idx, "right"):
            peakIdx.append(idx)
        elif isSmallerThanNeigbor(ticks.lows, idx, "left") and isSmallerThanNeigbor(ticks.lows, idx, "right"):
            bottomIdx.append(idx)    
    return peakIdx, bottomIdx

def isBiggerThanNeigbor(price, currentIdx, side):
    currentPrice = price[currentIdx]
    idxRange = range(currentIdx, -1, -1) if side == "left" else range(currentIdx, len(price), 1)

    for idx in idxRange:
        if price[idx] == INVALID_PRICE:
            break
        if price[idx] > currentPrice:
            return False
        if price[idx] < currentPrice:
            return True
    return False

def isSmallerThanNeigbor(price, currentIdx, side):
    currentPrice = price[currentIdx]
    idxRange = range(currentIdx, -1, -1) if side == "left" else range(currentIdx, len(price), 1)

    for idx in idxRange:
        if price[idx] == INVALID_PRICE:
            break
        if price[idx] < currentPrice:
            return False
        if price[idx] > currentPrice:
            return True
    return False

def nTypeL1Up(time, ticks, peakIdx, bottomIdx, stockNum=None, lowerBound=0):

    idxList = []
    PERIOD_OVERBOUGHT = 20

    for bIdx1 in bottomIdx:
        # print("bIdx1:", time[bIdx1],)
        if ticks.lows[bIdx1] <= lowerBound: continue

        pIdx1 = findNextIdx(peakIdx, bIdx1)
        if pIdx1 is None: continue
        if isRangeOverBound(ticks.lows[bIdx1+1:pIdx1], lowerBound=ticks.lows[bIdx1]): continue

        bIdx2 = findNextIdx(bottomIdx, pIdx1)     
        if bIdx2 is None: continue
        if ticks.lows[bIdx1] >= ticks.lows[bIdx2]: continue
        if isRangeOverBound(ticks.highs[pIdx1+1:bIdx2+1], upperBound=ticks.lows[bIdx1]+PERIOD_OVERBOUGHT): continue

        pIdx2 = findUpPIdx2(bIdx1, bIdx2, pIdx1, ticks)
        if pIdx2 is None: continue

        idxList.append([bIdx1, pIdx1, bIdx2, pIdx2])
    
    signal = []
    for idxs in idxList:
        s = "【N型上升】 %s [0] %s [1] %s [2] %s [3] %s [Buy Price] %d !" %(stockNum, time[idxs[0]], time[idxs[1]], time[idxs[2]], time[idxs[3]], ticks.closes[idxs[3]])
        signal.append(s)
    return signal

def findNextIdx(idxList, currentIdx):
    for idx in idxList:
        if idx > currentIdx:
            return idx
    return None

def isRangeOverBound(rangeList, upperBound=100000, lowerBound=-1):
    for r in rangeList:
        if r > upperBound or r < lowerBound:
            return True
    return False

def nTypeL1Down(time, ticks, peakIdx, bottomIdx, stockNum=None, upperBound=0):
    idxList = []
    PERIOD_OVERSOLD = 20

    for pIdx1 in peakIdx:

        # print("pIdx1:", time[pIdx1],)
        if ticks.highs[pIdx1] >= upperBound: continue

        bIdx1 = findNextIdx(bottomIdx, pIdx1)
        if bIdx1 is None: continue
        if isRangeOverBound(ticks.highs[pIdx1+1:bIdx1], upperBound=ticks.highs[pIdx1]): continue
        # print("bIdx1:", time[bIdx1],)

        pIdx2 = findNextIdx(peakIdx, bIdx1)
        if pIdx2 is None: continue
        if ticks.highs[pIdx1] <= ticks.highs[pIdx2]: continue
        if isRangeOverBound(ticks.lows[bIdx1+1:pIdx2+1], lowerBound=ticks.highs[bIdx1]-PERIOD_OVERSOLD): continue
        # print("pIdx2:", time[pIdx2],)

        bIdx2 = findDownBIdx2(pIdx1, pIdx2, bIdx1, ticks)
        if bIdx2 is None: continue
        # print("bIdx2:", time[bIdx2])

        idxList.append([pIdx1, bIdx1, pIdx2, bIdx2])
    
    signal = []
    for idxs in idxList:
        s = "【N型下降】 %s [0] %s [1] %s [2] %s [3] %s [Buy Price] %d !" %(stockNum, time[idxs[0]], time[idxs[1]], time[idxs[2]], time[idxs[3]], ticks.closes[idxs[3]])
        signal.append(s)
    return signal

def findUpPIdx2(bIdx1, bIdx2, pIdx1, ticks):
    upperBound, lowerBound1, lowerBound2 = ticks.highs[pIdx1], ticks.lows[bIdx1], ticks.lows[bIdx2]
    PERIOD_OVERBOUGHT = 20
    SINGLE_OVERBOUGHT = 12
    SINGLE_GROW = 10

    for idx in range(bIdx2+1, len(ticks.opens)):
        if lowerBound2 > ticks.lows[idx]:
            return None
        if upperBound < ticks.closes[idx]:
            idxUpperBound = min(ticks.opens[idx]+SINGLE_OVERBOUGHT, lowerBound1+PERIOD_OVERBOUGHT )
            if isRangeOverBound([ticks.closes[idx]], upperBound=idxUpperBound, lowerBound=lowerBound1+SINGLE_GROW):
                return idx
            else:
                return None
    return None

def findDownBIdx2(pIdx1, pIdx2, bIdx1, ticks):
    lowerBound, upperBound1, upperBound2 = ticks.lows[bIdx1], ticks.highs[pIdx1], ticks.highs[pIdx2]
    PERIOD_OVERSOLD = 20
    SINGLE_OVERSOLD = 12
    SINGLE_DOWN = 10

    for idx in range(pIdx2+1, len(ticks.opens)):
        if upperBound2 < ticks.highs[idx]:
            return None
        if lowerBound > ticks.closes[idx]:
            idxLowerBound = max(ticks.opens[idx]-SINGLE_OVERSOLD, upperBound1-PERIOD_OVERSOLD)
            if isRangeOverBound([ticks.closes[idx]], upperBound=upperBound1-SINGLE_DOWN, lowerBound=idxLowerBound):
                return idx
            else:
                return None
    return None

