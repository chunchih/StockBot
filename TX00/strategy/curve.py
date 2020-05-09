# -*- coding: UTF-8 -*-
from analysis_utils import *

def curve(price, interval, stock_no, t):
    delta = len(price) % interval
    price = get_ticks_with_interval(price, interval)
    short_time_ma = get_MA(price[:,3], 3)
    long_time_ma_low = get_MA(price[:,2], 5)
    long_time_ma_high = get_MA(price[:,1], 5)

    new_list = []
    for i in range(-1, -len(price)-1, -1):
        new_t = t+(interval-delta)%interval+(i+1)*interval
        # print(new_t, i, t, len(price), len(short_time_ma), len(long_time_ma_low))
        if 8*60+45 < new_t <= 13*60+45:
            pass
        else:
            break
        is_red = price[i][0] <= price[i][3]
        if -(i-4) > len(long_time_ma_high):
            break
        if is_red:
            is_gc = short_time_ma[i] >= long_time_ma_low[i] and short_time_ma[i-1] <= long_time_ma_low[i-1]
            is_short_up = short_time_ma[i] >= short_time_ma[i-1]
            is_long_down = long_time_ma_low[i] <= long_time_ma_low[i-1]
            is_below_continue1 = price[i-1][3] <= long_time_ma_low[i-1] and price[i-2][3] <= long_time_ma_low[i-2] and price[i-3][3] <= long_time_ma_low[i-3]  
            is_below_continue2 = price[i-2][3] <= long_time_ma_low[i-2] and price[i-3][3] <= long_time_ma_low[i-3] and price[i-4][3] <= long_time_ma_low[i-4]  
            if is_gc and is_short_up and is_long_down and (is_below_continue1 or is_below_continue2):
                s = "【彎道向上-%d分K】 股票代號: %s %.2d:%.2d"%(interval, stock_no, new_t//60, new_t%60)
                new_list.append(s)

        else:
            is_dc = short_time_ma[i] <= long_time_ma_high[i] and short_time_ma[i-1] >= long_time_ma_high[i-1]
            is_short_down = short_time_ma[i] <= short_time_ma[i-1]
            is_long_up = long_time_ma_high[i] >= long_time_ma_high[i-1]
            is_above_continue1 = price[i-1][3] >= long_time_ma_high[i-1] and price[i-2][3] >= long_time_ma_high[i-2] and price[i-3][3] >= long_time_ma_high[i-3]  
            is_above_continue2 = price[i-2][3] >= long_time_ma_high[i-2] and price[i-3][3] >= long_time_ma_high[i-3] and price[i-4][3] >= long_time_ma_high[i-4]  
            if is_dc and is_short_down and is_long_up and (is_above_continue1 or is_above_continue2):
                s = "【彎道向下-%d分K】 股票代號: %s %.2d:%.2d"%(interval, stock_no, new_t//60, new_t%60)
                new_list.append(s)

    new_list = new_list[::-1]
    return new_list
