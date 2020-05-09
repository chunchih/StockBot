# -- coding: UTF-8 --
from analysis_utils import *
import numpy as np
def doubPeriod(price, short_time_interval, long_time_interval, short_ma, long_ma, stock_name, t): 
    short_time_ticks = get_ticks_with_interval(price, short_time_interval)
    long_time_ticks = get_ticks_with_interval(price, long_time_interval)
    
    rsi = getRSI(short_price)
    KL, DL = getKD(stock_name, long_time_ticks, parameter=[9,3,3])

    is_long_time_gc = np.mean(long_time_ticks[-short_ma:]) >= np.mean(long_time_ticks[-long_ma:])
    is_short_time_gc = np.mean(short_time_ticks[-short_ma:]) >= np.mean(short_time_ticks[-long_ma:])

    new_list = []
    if rsi > 0.5 and is_short_time_gc and is_long_time_gc:
        s = "【雙週期上升】 股票代號 : %s %.2d:%.2d"%(stock_name, t//60, t%60)
        new_list.append(a)
    elif rsi < 0.5 and (not is_short_time_gc) and (not is_long_time_gc):
        s = "【雙週期下降】 股票代號: %s %.2d:%.2d"%(stock_name, t//60, t%60)
        new_list.append(a)

    return new_list 