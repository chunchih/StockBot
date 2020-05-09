# -- coding: UTF-8 --
# from utils import *
from analysis_utils import *
import numpy as np
def boolChannel(price, stock_name, t): 
    m5_price = get_ticks_with_interval(price, 5)
    mu = get_MA(m5_price[:,3], 20)
    std = np.array([np.std(m5_price[i-19:i+1, 3]) for i in range(19, len(m5_price)+1)])

    new_list = []
    if m5_price[-3][3] <= mu[-3] + std[-3]*2 and m5_price[-2][3] >= mu[-2] + std[-2]*2 and m5_price[-2][1] <= m5_price[-1][3]:
        s = "【布林向上突破】 股票代號: %s 突破點: %.2d:%.2d"%(stock_name, t//60, t%60)
        new_list.append(s)
    elif m5_price[-3][3] >= mu[-3] - std[-3]*2 and m5_price[-2][3] <= mu[-2] - std[-2]*2 and m5_price[-2][2] >= m5_price[-1][3]:
        s = "【布林向下突破】 股票代號: %s 突破點: %.2d:%.2d"%(stock_name, t//60, t%60)
        new_list.append(s)
    return new_list 