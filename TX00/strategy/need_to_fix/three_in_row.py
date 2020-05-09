# -*- coding: UTF-8 -*-
from analysis_utils import *

def thrL1Red(close_price, high_price, low_price, open_price, bottom, last_close, this_open, t):
    statUp = []
    for e1 in bottom:
        if e1+2 > len(close_price) -1: continue
        if close_price[e1] < open_price[e1] or close_price[e1+1] < open_price[e1+1] or close_price[e1+2] < open_price[e1+2]: continue
        if close_price[e1+1] <= close_price[e1] or close_price[e1+2] <= close_price[e1+1]: continue
        if max(high_price[e1:e1+3]) - min(low_price[e1:e1+3]) < 10: continue
        if abs(last_close-low_price[e1]) <= 30 and abs(this_open-low_price[e1]) <= 30 : continue
        b0 = e1 #len(close_price)-3
        b1 = e1+1 #len(close_price)-2
        b2 = e1+2 #len(close_price)-1
        c = close_price[e1+2]
        s = "【紅三兵】 [1] %.2d:%.2d [2] %.2d:%.2d [3] %.2d:%.2d [Buy Price] %d !" %((t+b0)//60, (t+b0)%60, (t+b1)//60, (t+b1)%60, (t+b2)//60, (t+b2)%60, c)
        statUp += [s]
    return statUp

def thrL1Black(close_price, high_price, low_price, open_price, peak, last_close, this_open, t):
    statDown = []
    print len(close_price)
    for e1 in peak:
        if e1+2 > len(close_price) -1: continue
        if close_price[e1] > open_price[e1] or close_price[e1+1] > open_price[e1+1] or close_price[e1+2] > open_price[e1+2]: continue
        if close_price[e1+1] >= close_price[e1] or close_price[e1+2] >= close_price[e1+1]: continue
        if max(high_price[e1:e1+3]) - min(low_price[e1:e1+3]) < 10: continue
        if abs(last_close-high_price[e1]) <= 30 and abs(this_open-high_price[e1]) <= 30 : continue
        b0 = e1
        b1 = e1+1
        b2 = e1+2
        c = close_price[e1+2]
        s = "【黑三兵】 [1] %.2d:%.2d [2] %.2d:%.2d [3] %.2d:%.2d [Buy Price] %d !" %((t+b0)//60, (t+b0)%60, (t+b1)//60, (t+b1)%60, (t+b2)//60, (t+b2)%60, c)
        statDown += [s]
    return statDown

def thrL1(close_price, high_price, low_price, open_price, peak, bottom, last_close, this_open, t):
    statUp = thrL1Red(close_price, high_price, low_price, open_price, bottom, last_close, this_open, t=t)
    statDown = thrL1Black(close_price, high_price, low_price, open_price, peak, last_close, this_open, t=t)    
    return statUp, statDown
    
def three_in_row(close_price, high_price, low_price, open_price, last_close, this_open, t=0): 
    peak, bottom = getPeakBottom(close_price, high_price, low_price, open_price)  
    statUp, statDown = thrL1(close_price, high_price, low_price, open_price, peak, bottom, last_close, this_open, t=t)   
    return statUp, statDown 