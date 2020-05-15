from utils import *

class TickInfoEnum:
    Date = 0
    Time = 1
    Open = 2
    High = 3
    Low = 4
    Close = 5
    Volume = 6

class Ticks:
    def __init__(self):
        self.dates = []
        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        
    def addTick(self, tick):
        self.dates.append(tick[TickInfoEnum.Date])
        self.times.append(tick[TickInfoEnum.Time])
        self.opens.append(tick[TickInfoEnum.Open])
        self.highs.append(tick[TickInfoEnum.High])
        self.lows.append(tick[TickInfoEnum.Low])
        self.closes.append(tick[TickInfoEnum.Close])
        self.volumes.append(tick[TickInfoEnum.Volume])
    
    def addTicks(self, ticks):
        for tick in ticks:
            self.addTick(tick)

    def getNum(self):
        return len(self.closes)

    def getTickByIdx(self, idx):
        return [self.dates[idx], self.times[idx], self.opens[idx], self.highs[idx], self.lows[idx], self.closes[idx], self.volumes[idx]]

    def mergeTicks(self, ticksA, ticksB):
        newTicks = Ticks()
        for idx in range(ticksA.getNum()):
            tick = ticksA.getTickByIdx(idx)
            newTicks.addTick(tick)
        
        for idx in range(ticksB.getNum()):
            tick = ticksB.getTickByIdx(idx)
            newTicks.addTick(tick)

        return newTicks

    def getTicksWithInterval(self, interval):
        INVALID_PRICE = -1

        if len(self.times) == 0:
            return self

        if interval == 1:
            return self

        newTicks = Ticks()
        remain = convertTimestampToInteger(self.times[0]) % interval 
        startIdx = (interval-remain+1)%interval

        for i in range(startIdx, self.getNum(), interval):
            if i+interval-1 < self.getNum():
                firstIdx = i
                lastIdx = i+interval-1
                d, t, o, h, l, c, v = self.dates[lastIdx], self.times[lastIdx], self.opens[firstIdx], max(self.highs[i:i+interval]), min(self.lows[i:i+interval]), self.closes[lastIdx], sum(self.volumes[i:i+interval])
                if l == INVALID_PRICE:
                    newTicks.addTick([d, t, -1, -1, -1, -1, -1])
                else:
                    newTicks.addTick([d, t, o, h, l, c, v])
        return newTicks

class StockData:
    def __init__(self, stockNum, interval, todayDate, mode='normal'):
        self.stockNum = stockNum
        self.interval = interval
        self.todayDate = todayDate
        # self.historyTicks = []
        # self.currentTicks = []
        # self.isCurrentStartAtBeginning = False
        self.startTimeInteger = 8*60+45 if stockNum == "TX00" else 9*60
        self.endTimeInteger = 13*60+45 if stockNum == "TX00" else 13*60+30
        self.historyTicks = Ticks()
        self.currentTicks = Ticks()
        self.totalTicks = Ticks()
        self.mode = mode

    def loadHistoryTicks(self):
        ticks = []
        folderDate = getPastFolderDate()
        for date in folderDate:
            if date != self.todayDate:
                dateTicks = self.handleTicksByDateFolder(date)
                ticks += dateTicks
        
        maxDuration = 3000
        self.historyTicks.addTicks(ticks[-maxDuration:])
        if self.mode == 'normal':
            print("History Ticks: ", self.historyTicks.getNum())
        self.totalTicks = self.historyTicks
        

    def handleTicksByDateFolder(self, date):
        dateTicks = []
        fileInDate = os.path.join('data', date, self.stockNum+'.txt')

        if os.path.isfile(fileInDate) is True:
            content = open(fileInDate, 'r').read().splitlines()
            for kl in content:
                comp = kl.split(', ')
                timestamp = comp[TickInfoEnum.Time]
                dateTicks = self.addTickWithoutDuplicate(timestamp, comp, dateTicks)
        return dateTicks
    
    def addTickWithoutDuplicate(self, timestamp, newKLine, dataTicks):
        for i in range(TickInfoEnum.Open, TickInfoEnum.Close+1):
            newKLine[i] = float(newKLine[i])
        newKLine[TickInfoEnum.Volume] = int(newKLine[TickInfoEnum.Volume])
        if newKLine not in dataTicks:
            dataTicks.append(newKLine)
        return dataTicks

    def loadCurrentTicks(self):
        self.currentTicks = Ticks()
        ticks = self.handleTicksByDateFolder(self.todayDate)
        if len(ticks) != 0:
            for tick in ticks:
                self.currentTicks.addTick(tick)       
            if self.mode == 'normal':
                print("Current Ticks: ", self.currentTicks.getNum())
            self.mergeHistoryAndCurrentTicks()

    def mergeHistoryAndCurrentTicks(self):
        # if self.isCurrentStartAtBeginning:
        self.totalTicks = Ticks().mergeTicks(self.historyTicks, self.currentTicks)
        # else:
        #     self.totalTicks = self.currentTicks
        if self.mode == 'normal':
            print("Total Ticks: ", self.totalTicks.getNum())
    
    def getHistoryTicks(self): return self.historyTicks
    def getCurrentTicks(self): return self.currentTicks
    def getTotalTicks(self): return self.totalTicks
    
    