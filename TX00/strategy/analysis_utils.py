import numpy as np
def continous_peak_bottom(high_price, low_price, close_price):
    c = -1
    peak_n = []
    while c > -len(high_price):
        if c != -1 and high_price[c+1] >= high_price[c]: 
            c -= 1
            continue
        fg = False
        for j in range(1, 10):
            if high_price[max(c-j,-len(high_price))] != high_price[c]:
                fg = True
                break     
        if fg and high_price[max(c-j,-len(high_price))] < high_price[c]:
            peak_n += [int(c+len(high_price))]  
            
        c = c-1 if fg else c-1          
               
            
    bottom_n = []
    c = -1
    while c > -len(high_price):
        if c != -1 and low_price[c+1] <= low_price[c]: 
            c -= 1
            continue
        fg = False
        for j in range(1, 10):
            if low_price[max(c-j, -len(high_price))] != low_price[c]:
                fg = True
                break                
        if fg and low_price[max(c-j,-len(high_price))] > low_price[c]:
            bottom_n += [int(c+len(high_price))]
            
        c = c-1 if fg else c-1
            
    return peak_n, bottom_n

def getPeakBottom(close_price, high_price, low_price, open_price):
    price = []
    for i in range(len(high_price)):
        price += [[open_price[i], high_price[i], low_price[i], close_price[i]]]
    price = np.array(price)
    
    peak = np.array([int(idx) for idx in range(1, len(high_price)-1) if high_price[idx-1] < high_price[idx] and high_price[idx] > high_price[idx+1]])
    bottom = np.array([int(idx) for idx in range(1, len(low_price)-1) if low_price[idx-1] > low_price[idx] and low_price[idx] < low_price[idx+1]])
    peak_n, bottom_n = continous_peak_bottom(high_price, low_price, close_price)
    
    if len(peak_n) != 0:
        peak = np.concatenate((peak, np.array(peak_n)), axis=0) # peak.extend(peak_n) # += peak_n
        peak = [int(p) for e, p in enumerate(np.sort(peak)) if p not in np.sort(peak)[:e] and int(p) != len(close_price)-1] 
    if len(bottom_n) != 0:
        bottom = np.concatenate((bottom, np.array(bottom_n)), axis=0) # += bottom_n
        bottom = [int(b) for e, b in enumerate(np.sort(bottom)) if b not in np.sort(bottom)[:e] and int(b) != len(close_price)-1]  
    
    return peak, bottom

def get_ticks_with_interval(price, interval):
    if interval == 1:
        return price
    results = []
    for i in range(len(price)):
        if i % interval == 0:
            o, h, l = price[i][0], price[i][1], price[i][2]
        else:
            h, l = max(h, price[i][1]), min(l, price[i][2])
        c = price[i][3]
        if i % interval == interval -1 or i == len(price) -1:
            results.append([o,h,l,c])
    return np.array(results)

def get_MA(price, interval):
    return np.array([np.mean(price[i-(interval):i]) for i in range(interval, len(price)+1) if len(price[i-(interval):i]) == interval])

def getRSI(close_price):
    up, down = [], []
    for i in range(1, len(close_price)):
        up += [max(close_price[i]-close_price[i-1], 0)]
        down += [max(close_price[i-1]-close_price[i], 0)]
    up_t, down_t = [np.mean(up[:5])], [np.mean(down[:5])]
    for i in range(5, len(up)):
        up_t += [up_t[i-5] + (1./5)*(up[i]-up_t[i-5])]
        down_t += [down_t[i-5] + (1./5)*(down[i]-down_t[i-5])]
    up_t, down_t = np.array(up_t), np.array(down_t)
    rsi = up_t / (up_t+down_t)    
    return rsi[-1]


def getKD(stock_name, price, parameter=[9,3,3]):    

    fpt = price
    RSV = np.ones((len(fpt)))*0.5
    fpt = np.array(fpt)
    for i in range(parameter[0]-1, len(fpt)):
        try:
            RSV[i] = (fpt[i][3] - min(fpt[i-(parameter[0]-1):i+1,2]))/(max(fpt[i-(parameter[0]-1):i+1,1]) - min(fpt[i-(parameter[0]-1):i+1,2]))
        except:
            RSV[i] = 1
    K, D = np.zeros((len(fpt))), np.zeros((len(fpt)))
    
    for i in range(1, len(RSV)):
        K[i] = (1.-1./(parameter[1])) * K[i-1] + 1./(parameter[1]) * RSV[i]
        D[i] = (1.-1./(parameter[2])) * D[i-1] + 1./(parameter[2]) * K[i]
    
    return K, D
