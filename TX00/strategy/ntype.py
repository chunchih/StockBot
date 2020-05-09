# -- coding: UTF-8 --
import numpy as np
#from Analyze import *
from analysis_utils import *

def nTypeL1Up(close_price, high_price, low_price, open_price, peak, bottom, stock_no=None, lower_bound=0, t=0):
    point0, point1, point2, point3, closed_price = [], [], [], [], []
    t = t-len(close_price)+1
    for e1, b1 in enumerate(bottom):
        if low_price[b1] <= lower_bound: continue
        if e1 == len(bottom)-1: break
        fg = False
        for e2, p1 in enumerate(peak):
            if p1 > b1 and e2 != len(close_price)-1:
                fg = True
                break
        if fg == False: continue

        b_idx1, b_idx2 = b1, bottom[e1+1]
        p_idx1 = p1      
        
        if (b_idx1 < p_idx1 < b_idx2) == False: continue            
        if (low_price[b_idx2] <= low_price[b_idx1]): continue
        
        fg = False
        for p2 in range(p_idx1+1, b_idx2): 
            if high_price[p2] - low_price[b_idx1] >= 20:
                fg = True
                break  
        if fg == True: continue

        fg = False
        for p2 in range(b_idx2, len(close_price)):
            if low_price[p2] < low_price[b_idx2]:
                fg = False
                break
            if close_price[p2] > high_price[p_idx1]:
                fg = 10 <= close_price[p2] - low_price[b_idx1] <= 20
                break
        if fg == False: continue
        if close_price[p2] - open_price[p2] > 12: continue
        point3 += [p2]
        point0 += [b_idx1]
        point1 += [p_idx1]
        point2 += [b_idx2]
        closed_price += [close_price[p2]]
    
    point0 = np.array(point0)
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3)
    closed_price = np.array(closed_price)
    if len(point3) == 0: return []
    
    if stock_no == 'TX00': start_time = 8*60+45
    elif stock_no == None:  start_time = 1000000
    else: start_time = 9*60

    stat = []
    for p2 in range(len(point3)): #zip(n_buy2, n_buy):
        b0 = point0[p2]
        if t+b0 <= start_time:
            continue
        b1 = point1[p2]
        b2 = point2[p2]
        b3 = point3[p2]
        c = closed_price[p2]
        #s = unicode("[N型上升]", encoding="utf-8")+" 0: %.2d:%.2d 1: %.2d:%.2d 2: %.2d:%.2d 3: %.2d:%.2d Buy Price:%d" %((t+b0+8*60+45+1)//60, (t+b0+8*60+45+1)%60, (t+b1+8*60+45+1)//60, (t+b1+8*60+45+1)%60, (t+b2+8*60+45+1)//60, (t+b2+8*60+45+1)%60, (t+b3+8*60+45+1)//60, (t+b3+8*60+45+1)%60, c)
        s = "【N型上升】 [0] %.2d:%.2d [1] %.2d:%.2d [2] %.2d:%.2d [3] %.2d:%.2d [Buy Price] %d !" %((t+b0)//60, (t+b0)%60, (t+b1)//60, (t+b1)%60, (t+b2)//60, (t+b2)%60, (t+b3)//60, (t+b3)%60, c)
        stat.append(s)
    return stat

def nTypeL1Down(close_price, high_price, low_price, open_price, peak, bottom, stock_no=None, upper_bound=0, t=0):
    point0, point1, point2, point3, closed_price = [], [], [], [], []
    t = t-len(close_price)+1
    for e1, b1 in enumerate(peak):
        if high_price[b1] >= upper_bound: continue
        if e1 == len(peak)-1: break
        fg = False
        for e2, p1 in enumerate(bottom):
            if p1 > b1 and e2 != len(close_price)-1:
                fg = True
                break
        if fg == False: continue
        p_idx1, p_idx2 = b1, peak[e1+1]
        b_idx1 = p1
        
        if (p_idx1 < b_idx1 < p_idx2) == False: continue            
        if (high_price[p_idx1] <= high_price[p_idx2]): continue
        fg = False
        for p2 in range(b_idx1+1, p_idx2): 
            if high_price[p_idx1] - low_price[p2] >= 20:
                fg = True
                break  
        if fg == True: continue
        fg = False
        for p2 in range(p_idx2, len(close_price)):
            if high_price[p2] > high_price[p_idx2]:
                fg = False
                break
                
            if close_price[p2] < low_price[b_idx1]:
                fg = -10 >= close_price[p2] - high_price[p_idx1] >= -20
                break
        if fg == False: continue
        if close_price[p2] - open_price[p2] < -12: continue
        point3 += [p2]
        point0 += [p_idx1]
        point1 += [b_idx1]
        point2 += [p_idx2]
        closed_price += [close_price[p2]]
    
    point0 = np.array(point0)
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3)
    closed_price = np.array(closed_price)
    if len(point3) == 0: return []
    
    if stock_no == 'TX00': start_time = 8*60+45
    elif stock_no == None:  start_time = 1000000
    else: start_time = 9*60
    stat = []
    for p2 in range(len(point3)): #zip(n_buy2, n_buy):
        b0 = point0[p2]
        if t+b0 <= start_time:
            continue
        b1 = point1[p2]
        b2 = point2[p2]
        b3 = point3[p2]
        c = closed_price[p2]
        s = "【N型下降】 [0] %.2d:%.2d [1] %.2d:%.2d [2] %.2d:%.2d [3] %.2d:%.2d [Buy Price] %d !" %((t+b0)//60, (t+b0)%60, (t+b1)//60, (t+b1)%60, (t+b2)//60, (t+b2)%60, (t+b3)//60, (t+b3)%60, c)
        stat.append(s)
    return stat

def nTypeL1(close_price, high_price, low_price, open_price, peak, bottom, bound, t=0, stock_no=None):

    statUp = nTypeL1Up(close_price, high_price, low_price, open_price, peak, bottom, lower_bound=bound, t=t, stock_no=stock_no)
    #statUp = []
    statDown = nTypeL1Down(close_price, high_price, low_price, open_price, peak, bottom, upper_bound=bound, t=t, stock_no=stock_no)
    return statUp, statDown

def nType(price, stock_no=None, bound=0, t=0): 
    peak, bottom = getPeakBottom(price[:,3], price[:,1], price[:,2], price[:,0])  
    statUp, statDown = nTypeL1(price[:,3], price[:,1], price[:,2], price[:,0], peak, bottom, bound=bound, t=t, stock_no=stock_no)  
    return statUp, statDown   



