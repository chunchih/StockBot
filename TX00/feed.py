# import sys
# sys.path.append('strategy')
# from strategy.ntype import nType
# from strategy.curve import curve
from strategy import nType, curve, MASync
# from strategy.three_in_row import three_in_row
# from strategy.doubPeriod import doubPeriod
from StockData import TickInfoEnum

def putSignal(prevSignal, newSignal, stockNum):
    for signal in newSignal:
        if signal not in prevSignal:
            f = open(stockNum+'-report.txt', 'a')
            f.write(signal+'\n')
            f.close()
            prevSignal.append(signal)
    return prevSignal
    
def feedSystem(stock, prevSignal):
    ntypeInfo = {'stock': stock}
    # thrInRow_info = {'close_price':c, 'high_price':h, 'low_price':l, 'open_price':o, 'last_close':last_close, 'this_open':this_open, 'currentTimeInteger':t}
    curve1KInfo = {'stock': stock, 'interval': 1}
    curve5KInfo = {'stock': stock, 'interval': 5}
    MASyncInfo = {'stock': stock, 'interval': 5}
    infos = {'ntype':ntypeInfo, 'curve': [curve1KInfo, curve5KInfo], 'MASync': MASyncInfo}

    if 'ntype' in infos:
        ntypeSignal = nType(**infos['ntype'])
        prevSignal = putSignal(prevSignal, ntypeSignal, stock.stockNum)    
    
    if 'curve' in infos:
        for curveInfo in infos['curve']:
            curveSignal = curve(**curveInfo)
            prevSignal = putSignal(prevSignal, curveSignal, stock.stockNum)
    
    if 'MASync' in infos:
        MASyncSignal = MASync(**infos['MASync'])
        prevSignal = putSignal(prevSignal, MASyncSignal, stock.stockNum) 

    # if 'thrInRow' in infos:
    #     thr_statUp, thr_statDown = three_in_row(**infos['thrInRow'])
    #     pre_stat = put_in_stat(pre_stat, thr_statUp, stock_name)
    #     pre_stat = put_in_stat(pre_stat, thr_statDown, stock_name)  



    return prevSignal
    
