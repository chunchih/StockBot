
 
from StockData import *
from utils import *
import time
from feed import *

def predict(stockNum, todayDate):
    pre_stat = []
    prevTimestamp = ""

    # interval = int(min_type.split(' ')[0])
    interval = 1
    stock = StockData(stockNum, interval, todayDate)
    stock.loadHistoryTicks()

    while True:
        currentTimestamp = strftime("%H:%M", gmtime())
        validStatus, currentTimeInteger = checkTimeValid(prevTimestamp, currentTimestamp)
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
        pre_stat = feedSystem(stock, prevSignal=pre_stat)  
