import comtypes.client
from comtypes.client import GetModule, CreateObject, GetEvents
GetModule(r'SKCOM.dll')

import comtypes.gen.SKCOMLib as sk
from utils import *
import threading
from function import predict


if 'skC' not in globals(): skC=CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
if 'skQ' not in globals(): skQ=CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
if 'skR' not in globals(): skR=CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)

class skR_events:
    def OnReplyMessage(self, bstrUserID, bstrMessage, sConfirmCode=0xFFFF):
        print('OnReplyMessage', bstrUserID, bstrMessage)
        return sConfirmCode       

class SKQuoteLibEvents:     
    def __init__(self):
        self.data = []

    def setTick(self, tickData):
        self.tickData = tickData

    def setStockNum(self, stockNum):
        self.stockNum = stockNum

    def setTodayDate(self, todayDate):
        self.todayDate = todayDate

    def clearData(self):
        self.data = []

    def OnConnection(self, nKind, nCode):
        if (nKind == 3001):
            strMsg = "Connected!"
        elif (nKind == 3002):
            strMsg = "DisConnected!"
        elif (nKind == 3003):
            strMsg = "Stocks ready!"
        elif (nKind == 3021):
            strMsg = "Connect Error!"
        print(strMsg)

    def OnNotifyKLineData(self, bstrStockNo, bstrData):
        KLYear, KLMonth, KLDay = bstrData[6:10], bstrData[:2], bstrData[3:5]
        dateStamp = "%s/%s/%s"%(KLYear, KLMonth, KLDay)
        comp = bstrData.split(',')
        timeStamp = comp[1].strip()
        price = ', '.join(intListToStrList(priceMultiplyOnePercent(comp[2:6])))
        volume = comp[6].strip()
        self.data.append(', '.join([dateStamp, timeStamp, price, volume]))

    def OnNotifyTicks(self,sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        if self.tickData['time'] == lTimehms//100:
            self.tickData['high'] = max(nClose, self.tickData['high'])
            self.tickData['low'] = min(nClose, self.tickData['low'])
            self.tickData['close'] = nClose
            self.tickData['volume'] += nQty

        else:
            if self.tickData['time'] != -1:
                if 8*60+46 <= (lTimehms//10000)*60+((lTimehms%10000)//100):
                    tickYear = "%.4d/%.2d/%.2d"%(lDate//10000, (lDate%10000)//100, lDate%100)
                    tickTime = "%.2d:%.2d"%(lTimehms//10000, ((lTimehms%10000)//100))
                    tickPrice = "%d, %d, %d, %d"%(self.tickData['open'], self.tickData['high'], self.tickData['low'], self.tickData['close'])
                    self.data.append(', '.join([tickYear, tickTime, tickPrice, str(self.tickData['volume'])]))
                    createParentFolderIfNotExist(os.path.join('data', self.todayDate, self.stockNum+'.txt'))
                    open(os.path.join('data', self.todayDate, self.stockNum+'.txt'), 'w').write('\n'.join(self.data))

            self.tickData['time'] = lTimehms//100
            self.tickData['open'] = nClose
            self.tickData['high'] = nClose
            self.tickData['low'] = nClose
            self.tickData['close'] = nClose
            self.tickData['volume'] = nQty

    def getData(self):
        return self.data

EventQ = SKQuoteLibEvents()
EventR = skR_events()
ConnQ = GetEvents(skQ, EventQ)
ConnR = GetEvents(skR, EventR)  

def loginCapitalAccount():
    content = open('ID.txt', 'r').read().splitlines()
    ID = content[0].strip(' ')
    PW = content[1].strip(' ')

    print("Login:", skC.SKCenterLib_GetReturnCodeMessage(skC.SKCenterLib_Login(ID, PW)))
    print("Connect:", skC.SKCenterLib_GetReturnCodeMessage(skQ.SKQuoteLib_EnterMonitor()))
        
def requestKL(todayString):
    todayDatestamp = todayString.get()
    lastDate = findLastDateByStock('TX00.txt', todayDatestamp)

    m_nCode = skQ.SKQuoteLib_RequestKLineAM('TX00', 0, 0, 0)
    if m_nCode != 0:
        print("RequestKL Error: "+m_nCode)

    savingData = removeDataUntilLastDate(EventQ.getData(), lastDate)
    savingFolder = os.path.join('data', todayDatestamp)
    writeFileWithContent(os.path.join(savingFolder, 'TX00.txt'), '\n'.join(savingData))
    EventQ.clearData()

def requestTick(todayString):
    todayDatestamp = todayString.get()
    lastDate = findLastDateByStock('TX00.txt', todayDatestamp)

    m_nCode = skQ.SKQuoteLib_RequestKLineAM('TX00', 0, 0, 0)
    if m_nCode != 0:
        print("RequestKL Error: "+str(m_nCode))

    savingData = removeDataUntilLastDate(EventQ.getData(), lastDate)
    savingFolder = os.path.join('data', todayDatestamp)
    writeFileWithContent(os.path.join(savingFolder, 'TX00.txt'), '\n'.join(savingData))
    EventQ.clearData()

def runTX00(todayString):
    ### TO-DO: handle thread1 Exception
    todayDate = todayString.get()
    createParentFolderIfNotExist(os.path.join('data', todayDate))
    clearFile("TX00-report.txt")
    thread1 = threading.Thread(target=getTick, args=('TX00', todayDate))
    thread2 = threading.Thread(target=predict, args=('TX00', todayDate))
    thread1.start()
    thread2.start()	

def getTick(stockNum, todayDate):
    tickData = {'time':-1, 'open':-1, 'high':-1, 'low':-1, 'close':-1, 'volume':0}
    EventQ.setTick(tickData)
    EventQ.setStockNum(stockNum)
    EventQ.setTodayDate(todayDate)
    m_nCode = skQ.SKQuoteLib_RequestLiveTick(0, stockNum)
    if m_nCode != [0, 0]:
        print("GetTick Error: "+str(m_nCode))
