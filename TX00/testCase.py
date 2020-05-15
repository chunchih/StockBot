from utils import *
from feed import *
from StockData import StockData, TickInfoEnum

stock = StockData('TX00', 1, '2020-05-14', mode='test')
### Test Stock DataLoading
stock.loadHistoryTicks()
print("---------------------------------")
print("Get History Data: ", stock.getHistoryTicks().getNum())
print("---------------------------------")
print("Get Total Data: ", stock.getTotalTicks().getNum())
print("---------------------------------")
print("Get 5K Data: ", stock.getTotalTicks().getTicksWithInterval(5).getNum())
print("---------------------------------")
### Test Enum
print("Enum Time: ", TickInfoEnum.Time)
print("---------------------------------")

### Test Prediction
def test1():
    print("Simulate: Perfectly Run A day!")
    print("---------------------------------")

    pre_stat = []
    testData = open(os.path.join('data', '2020-05-14', 'TX00_test.txt'), 'r').read().splitlines()
    for i in range(1, 301, 1):
        open(os.path.join('data', '2020-05-14', 'TX00.txt'), 'w').write('\n'.join(testData[:i]))
        stock.loadCurrentTicks()
        
        new_stat = feedSystem(stock, prevSignal=pre_stat)
        if len(new_stat) != pre_stat and i == 300:
            pre_stat = new_stat
            print("Last Tick:", stock.getCurrentTicks().getTickByIdx(-1))
            print("Signals:", pre_stat)
            print('-----------------------------------')
            open('test1.txt', 'w').write('\n'.join(pre_stat))

### Not Run At First
def test2():
    print("Simulate: Not Run At First!")
    print("---------------------------------")

    pre_stat = []
    testData = open(os.path.join('data', '2020-05-14', 'TX00_test.txt'), 'r').read().splitlines()
    psuedoTicks = [', '.join(['2020/05/14', convertIntegerToTimestamp(ts), "-1", "-1", "-1", "-1", "-1"]) for ts in range(8*60+46, 9*60+46)]
    for i in range(60, 301, 1):
        open(os.path.join('data', '2020-05-14', 'TX00.txt'), 'w').write('\n'.join(psuedoTicks+testData[60:i]))
        stock.loadCurrentTicks()
        
        new_stat = feedSystem(stock, prevSignal=pre_stat)
        if len(new_stat) != pre_stat and i == 300:
            pre_stat = new_stat
            print("Last Tick:", stock.getCurrentTicks().getTickByIdx(-1))
            print("Signals:", pre_stat)
            print('-----------------------------------')
            open('test1.txt', 'w').write('\n'.join(pre_stat))

test1()
test2()