import time
import numpy as np
import os
from tkinter import *
import datetime
from feed import *
import threading
from utils import *
from tkinter import ttk
from time import gmtime, strftime, sleep

import comtypes.client

comtypes.client.GetModule(r'SKCOM.dll')
import comtypes.gen.SKCOMLib as sk
# global skQt
skC = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)
skOOQ = comtypes.client.CreateObject(sk.SKOOQuoteLib,interface=sk.ISKOOQuoteLib)
skO = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib)
skOSQ = comtypes.client.CreateObject(sk.SKOSQuoteLib,interface=sk.ISKOSQuoteLib)
skQ = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib)
skR = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib)

class skR_events:
    def OnReplyMessage(self, bstrUserID, bstrMessage, sConfirmCode=0xFFFF):
        print('OnReplyMessage', bstrUserID, bstrMessage)
        return sConfirmCode   

#Event sink, 事件實體  
EventR=skR_events()
#make connection to event sink
ConnR = comtypes.client.GetEvents(skR, EventR)
def takeSecond(elem):
    return elem.split(',')[1]

class SKQuoteLibEvents:     
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
    def OnNotifyTicks(self,sMarketNo, sStockIdx, nPtr, lDate, lTimehms, lTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        global today_date, stock_no, note_data, all_data

        # note = open(os.path.join('data', today_date, '1m', stock_no+'.txt'), 'a')
        if note_data['time'] == lTimehms//100:
            note_data['high'] = max(nClose, note_data['high'])
            note_data['low'] = max(nClose, note_data['low'])
            note_data['close'] = nClose
            note_data['volume'] += nQty

        else:
            if note_data['time'] != -1:
                if 8*60+46 <= (lTimehms//10000)*60+((lTimehms%10000)//100):
                    all_data.sort(key=takeSecond)
                    all_data.append(', '.join(["%.4d/%.2d/%.2d"%(lDate//10000, (lDate%10000)//100, lDate%100), "%.2d:%.2d"%(lTimehms//10000, ((lTimehms%10000)//100)), str(note_data['open']), 
                    str(note_data['high']), str(note_data['low']), str(note_data['close']), str(note_data['volume'])]))
                    open(os.path.join('data', today_date, '1m', stock_no+'.txt'), 'w').write('\n'.join(all_data))
            note_data['time'] = lTimehms//100
            note_data['open'] = nClose
            note_data['high'] = nClose
            note_data['low'] = nClose
            note_data['close'] = nClose
            note_data['volume'] = nQty

SKQuoteEvent=SKQuoteLibEvents()
SKQuoteLibEventHandler = comtypes.client.GetEvents(skQ, SKQuoteEvent)


class EntryWithPlaceholder(Entry):
    def __init__(self, master, placeholder, textvariable, color='grey'):
        super(EntryWithPlaceholder, self).__init__(master, textvariable=textvariable)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def run():
	while True:
		global today_date, stock_no, min_type, note_data, tickNum
		today_date = today_string.get()
		stock_no = stock_string.get()
		min_type = comboExample.get()

		if os.path.isdir(os.path.join('data', today_date, '1m')) is False:
			os.makedirs(os.path.join('data', today_date, '1m'))

		if os.path.isfile(os.path.join(stock_no+"-report.txt")) is True:
			os.remove(os.path.join(stock_no+"-report.txt"))
		_ = open(os.path.join(stock_no+"-report.txt"), 'w')

		if os.path.isfile("new_add.txt") is True:
			os.remove("new_add.txt")

		thread1 = threading.Thread(target=tick)
		thread2 = threading.Thread(target=predict)
		thread1.start()
		thread2.start()
		tickNum = []
def tick():
    global stock_no, note_data, all_data
    note_data = {'time':-1, 'open':-1, 'high':-1, 'low':-1, 'close':-1, 'volume':0}
    all_data = []
    m_nCode = skQ.SKQuoteLib_RequestLiveTick(0, stock_no)


def predict():
    global stock_no, today_date, all_data, tickNum
    pre_stat = []
    pre_t = 0
    history_data = getHistoryData(stock_no, today_date, interval=int(min_type.split(' ')[0]), duration=3000)
    while True:
        current_time = strftime("%H:%M", gmtime()).split(':')
        # t = 8*60+45+len(today_data)
        # t = 13*60+45
        t = (int(current_time[0])*60 + int(current_time[1]) + 8*60) % (24*60)
        if t>13*60+46:
        	break
        if pre_t == t or t <= 8*60+45:
            time.sleep(30)
            continue

        # if os.path.isfile('new_add.txt') is True:
        #     for ff in open('new_add.txt', 'r').readlines():
        #         if ff.rstrip('\n') not in all_data:
        #             all_data.append(ff.rstrip('\n'))

        is_first, today_data = getCurrentData(stock_no, today_date, interval=int(min_type.split(' ')[0]))
        if len(today_data) == 0 or is_first is None:
            time.sleep(20)
            continue
        if is_first:
            data = np.concatenate([history_data, today_data], 0)
        else:
            data = today_data
        print('data', len(data))

        tickNum.append(len(data))
        if(len(tickNum) >= 3 and tickNum[-1]==tickNum[-2] and tickNum[-2]==tickNum[-3]): break

        # print(data)
        pre_t = t
        ntype_info = {'price': data, 'bound':history_data[-1,3], 't':t, 'stock_no':stock_no}
        # thrInRow_info = {'close_price':c, 'high_price':h, 'low_price':l, 'open_price':o, 'last_close':last_close, 'this_open':this_open, 't':t}
        curve_info_1 = {'price': data, 't':t, 'stock_no':stock_no, 'interval': 1}
        curve_info_5 = {'price': data, 't':t, 'stock_no':stock_no, 'interval': 5}
        infos = {'ntype':ntype_info, 'curve': [curve_info_1, curve_info_5]}
        pre_stat = feed_stream(infos, pre_stat=pre_stat, stock_name=stock_no)  	

if __name__ == '__main__':    
    # EventQ = SKQuoteLibEvents()
    # EventR=skR_events()
    # ConnQ = GetEvents(skQ, EventQ)
    # ConnR = GetEvents(skR, EventR)    
    f = open('ID.txt', 'r').readlines()
    ID = f[0].rstrip('\n').strip(' ')
    PW = f[1].rstrip('\n').strip(' ')
    print("Login:", skC.SKCenterLib_GetReturnCodeMessage(skC.SKCenterLib_Login(ID, PW)))
    print("Connect:", skC.SKCenterLib_GetReturnCodeMessage(skQ.SKQuoteLib_EnterMonitor()))

    root = Tk()
    root.title('策略預估')
    root.geometry('300x50')  

    today_date_label = Label(root, text = "Today Date")
    stock_label = Label(root, text = "Stock No.")
    today_string = StringVar()
    stock_string = StringVar()
    tickNum = []

    entry_today = EntryWithPlaceholder(root, '2019-08-03', textvariable=today_string)
    entry_stock = EntryWithPlaceholder(root, 'TX00', textvariable=stock_string)

    comboExample = ttk.Combobox(root, values=[ "1 min", "5 min"], width=5)
    resultButton = Button(root, text = u"開始", command=run, width=5)

    today_date_label.grid(column=0, row=1, sticky=W)
    entry_today.grid(column=1, row=1, padx=10)
    stock_label.grid(column=0, row=0, sticky=W)
    entry_stock.grid(column=1, row=0, padx=10)
    comboExample.grid(column=2, row=0)
    comboExample.current(0)
    resultButton.grid(column=2, row=1, sticky=W)

    root.mainloop()