import time
import numpy as np
import os
from comtypes.client import GetModule, CreateObject, GetEvents
from tkinter import *
import datetime

GetModule(r'SKCOM.dll')
import comtypes.gen.SKCOMLib as sk
if 'skC' not in globals(): skC=CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
if 'skQ' not in globals(): skQ=CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
if 'skR' not in globals(): skR=CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)
# Configuration

class EntryWithPlaceholder(Entry):
    def __init__(self, master, placeholder, textvariable, color='grey'):
    	# super(StockDataFromCSV, self).__init__(data_root)
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

class skQ_events:
    def OnConnection(self, nKind, nCode):
        if nCode == 0 :
            if nKind == 3001 :  print("連線中, nkind= ", nKind)
            elif nKind == 3003: print("連線成功, nkind= ", nKind)
class skR_events:
    def OnReplyMessage(self, bstrUserID, bstrMessage, sConfirmCode=0xFFFF):
        print('OnReplyMessage', bstrUserID, bstrMessage)
        return sConfirmCode       


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

    def OnNotifyKLineData(self, bstrStockNo, bstrData):
        global note_data, last_date, fg
        # print(note_data)
        if bstrData[12:17] == '13:45' and fg == False:            
            if bstrData[6:10]+'-'+bstrData[:2]+'-'+bstrData[3:5] == last_date:
                fg = True
        elif fg == True:
            note_data.append(bstrData[6:10]+'/'+bstrData[:2]+'/'+bstrData[3:5]+bstrData[10:]) 
            

def requestKL():
    global note_data, today_date, last_date, fg

    today_date = today_string.get()

    if os.path.isdir(os.path.join('data', today_date)) is False:
    	os.makedirs(os.path.join('data', today_date))	     

    f = ['TX00']
    for e, s in enumerate(f):		
        print(e, s)
        last_date = ''
        last_num = -1
        for i,j,k in os.walk('data'):
            i = i.split('\\')
            print(i)
            if len(i) != 2:
            	continue
            i = i[1]
            comp = i.split('-')
            num = int(comp[0])*(12*31) + int(comp[1])*31 + int(comp[2])
            if num > last_num and i != today_date and os.path.isfile(os.path.join('data', i, s+'.txt')):
            	last_num, last_date = num, i   

        note_data, fg = [], last_date == ''
        m_nCode = skQ.SKQuoteLib_RequestKLineAM(s, 0, 0, 0)
        if len(note_data) == 0:		
        	continue
        note = open(os.path.join('data', today_date, s+'.txt'), 'w')   
        note.write('\n'.join(note_data))
        time.sleep(1)

if __name__ == '__main__':
    EventQ = SKQuoteLibEvents()
    # EventQ2 = skQ_events()
    EventR=skR_events()
    ConnQ = GetEvents(skQ, EventQ)
    ConnR = GetEvents(skR, EventR)    
    # ConnQ2 = GetEvents(skQ, EventQ2)

    f = open('ID.txt', 'r').readlines()
    ID = f[0].rstrip('\n').strip(' ')
    PW = f[1].rstrip('\n').strip(' ')
    print("Login:", skC.SKCenterLib_GetReturnCodeMessage(skC.SKCenterLib_Login(ID, PW)))
    print("Connect:", skC.SKCenterLib_GetReturnCodeMessage(skQ.SKQuoteLib_EnterMonitor()))

    root = Tk()
    root.title('紀錄當天股票')
    root.geometry('300x30')  

    today_date_label = Label(root, text = "Today Date")
    today_string = StringVar()

    entry_today = EntryWithPlaceholder(root, '2000-01-01', textvariable=today_string)
    resultButton = Button(root, text = u"送出", command=requestKL)

    today_date_label.grid(column=0, row=0, sticky=W)
    entry_today.grid(column=1, row=0, padx=10)
    resultButton.grid(column=2, row=0, sticky=W)

    root.mainloop()