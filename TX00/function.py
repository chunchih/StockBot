
 
from StockData import *
from utils import *
import time
from feed import *

def predict(stockNum, todayDate):
    pre_stat = []
    prevTimestamp = ""

    interval = 1
    stock = StockData(stockNum, interval, todayDate)
    stock.loadHistoryTicks()
    lastTickRepeatedTimes = 0
    prevLastTick = ""

    while True:
        currentTimestamp = strftime("%H:%M", gmtime())
        validStatus, _= checkTimeValid(prevTimestamp, currentTimestamp)
        if validStatus == "Leave":
            break   
        elif validStatus == "Wait":
            time.sleep(30)
            continue        
        else:
            pass

        prevTimestamp = currentTimestamp
        stock.loadCurrentTicks()
        if stock.getCurrentTicks().getNum() == 0:
            time.sleep(30)
            continue    

        currentLastTick = stock.getCurrentTicks().getTickByIdx(-1)
        if currentLastTick == prevLastTick:
            lastTickRepeatedTimes += 1
            time.sleep(10)
            continue
        else:
            lastTickRepeatedTimes = 0

        prevLastTick = currentLastTick

        if lastTickRepeatedTimes > 5:
            time.sleep(5)
            break

        pre_stat = feedSystem(stock, prevSignal=pre_stat)  
