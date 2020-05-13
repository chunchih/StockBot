from utils import *
from feed import *
from StockData import StockData, TickInfoEnum

stock = StockData('TX00', 1, '2020-05-11')
### Test Stock DataLoading
stock.loadHistoryTicks()
stock.loadCurrentTicks()
print("---------------------------------")
print("Get Total Data: ", stock.getTotalTicks().getNum())
print("---------------------------------")
print("Get 5K Data: ", stock.getTotalTicks().getTicksWithInterval(5).getNum())
print("---------------------------------")
### Test Enum
print("Enum Time: ", TickInfoEnum.Time)

### Test Prediction
def test1():
    pre_stat = []
    testData = open(os.path.join('data', '2020-05-11', 'TX00_test.txt'), 'r').read().splitlines()
    for i in range(1, 301, 1):
        open(os.path.join('data', '2020-05-11', 'TX00.txt'), 'w').write('\n'.join(testData[:i]))
        stock.loadCurrentTicks()
        
        new_stat = feedSystem(stock, prevSignal=pre_stat)
        if len(new_stat) != pre_stat:
            pre_stat = new_stat
            print(stock.getCurrentTicks().getTickByIdx(-1))
            print(pre_stat)
            print('-----------------------------------')
            open('curve.txt', 'w').write('\n'.join(pre_stat))

test1()