import time
import os
import numpy as np
from numpy import genfromtxt
import operator

from selenium import webdriver
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from time import gmtime, strftime, sleep


def expand_shadow_element(driver, element):
  
  return shadow_root

def get5mStock(stock_list):

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=option)
    

    stock_info = dict()
    if os.path.isdir('5m') is False:
        os.makedirs('5m')

    pass_files = []
    for s in stock_list:
        if os.path.isfile(os.path.join('5m', str(s)+'.txt')) is True:
            whole_file = open(os.path.join('5m', str(s)+'.txt'), 'r').read().splitlines()
            last_line = whole_file[-1]
        else:
            whole_file = []
            last_line = '-1'
        stock_file = []
        # driver.implicitly_wait(5) 
        driver.get('https://tw.stock.yahoo.com/q/ta?s=%s'%(s))
        time.sleep(10)

       

        driver.switch_to.frame(driver.find_element_by_xpath("/html/body/center/table[1]/tbody/tr/td[1]/table[2]/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td/iframe"))
        # soup = BeautifulSoup(r.text, "html.parser")
        element = driver.find_element_by_id('TAChartPeriod')
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == "5m":
                option.click()
      
        # blank = driver.find_element_by_xpath('//font[contains(@size, "-1")][text()= "股票代號查詢"]')
        value = driver.find_element_by_id('TAChartLabel1')
        year = strftime("%Y", gmtime())
        stock_data = []
        start_t = -1
        for i in range(0, 550, 5):
            for j in range(2):
                if i != 0 and j == 1:
                    continue
                try:
                    ActionChains(driver).move_to_element_with_offset(value, i, 40).perform()
                    data = value.text.split('\n')[0].split(' ')
                    d, t = year+'/'+data[0], data[1]
                    o, h, l, c, v = data[3].split(':')[1],data[5].split(':')[1], data[7].split(':')[1], data[9].split(':')[1] , data[11].split(':')[1]
                    current_t = (int(data[0].split('/')[0])*31+int(data[0].split('/')[1]))*60*24+int(data[1].split(':')[0])*60+int(data[1].split(':')[1])
                    # print(current_t)
                    if start_t == -1:
                        start_t = current_t
                        stock_data = [', '.join([d, t, o, h, l, c, v])]
                        # print('first', stock_data)
                    elif start_t > current_t: 
                        stock_data = [', '.join([d, t, o, h, l, c, v])]
                        start_t = current_t
                        # print('first_second', stock_data)
                    else:
                        new_data = ', '.join([d, t, o, h, l, c, v])
                        if new_data not in stock_data:
                            stock_data.append(new_data)
                            # print('second', stock_data)
                except:
                    pass_files.append(s)
                    pass
        open(os.path.join('5m', str(s)+'.txt'), 'w').write('\n'.join(stock_data))
    return pass_files
def getVol(top_num):

    f = genfromtxt("vol.txt", delimiter=' ')[::-1,:]
    stock = dict()
    for comp in f:
        stock_name = str(int(comp[0]))
        if stock_name not in stock:
            stock[stock_name] = int(comp[1])

    sorted_x = sorted(stock.items(), key=operator.itemgetter(1))[::-1][:top_num]
    stock_name = [xx[0] for xx in sorted_x][:top_num]
    stock_ignore_list = []
    if os.path.isfile('system_ignore_list.txt') is True:
        stock_ignore_list += genfromtxt('system_ignore_list.txt', delimiter=',')
    if os.path.isfile('manual_ignore_list.txt') is True:
        stock_ignore_list += genfromtxt('manual_ignore_list.txt', delimiter=',')
    stock_name = [str(s) for s in stock_name if int(s) not in stock_ignore_list]
    return stock_name

def getHistoryData(stock_name, today_date, interval, duration):
    date = dict()
    for i,j,k in os.walk('data'):
        if len(i.split('\\')) != 2: continue
        folder_date = i.split('\\')[1]
        if folder_date != today_date:
            date[folder_date] = int(folder_date.split('-')[0])*(12*31)+int(folder_date.split('-')[1])*(31)+int(folder_date.split('-')[2])
    import operator
    sorted_date = sorted(date.items(), key=operator.itemgetter(1))
    history_data = []
    if stock_name == 'TX00': start_time, end_time = 8*60+45, 13*60+45
    else: start_time, end_time = 9*60, 13*60+30

    for d in sorted_date:
        d = d[0]
        try:
            data = open(os.path.join('data', d, stock_name+'.txt'), 'r').read().splitlines()
            new_data = []
            for t in data:
                comp = t.split(', ')
                if start_time <= int(comp[1].split(':')[0])*60+int(comp[1].split(':')[1]) <= end_time:
                    tmp = [int(comp[2])*0.01, int(comp[3])*0.01, int(comp[4])*0.01, int(comp[5])*0.01, int(comp[6])]
                    if tmp not in history_data:
                        new_data += [tmp]
            history_data += new_data
        except:
            pass
    history_data = np.array(history_data)
    output = np.array([[history_data[i][0], max(history_data[i:i+interval,1]), min(history_data[i:i+interval,2]), history_data[i+interval-1][3], sum(history_data[i:i+interval,4])] for i in range(0, len(history_data), interval)])[-duration:]
    return output

def getCurrentData(stock_name, today_date, interval):
    if stock_name == 'TX00':
        if os.path.isfile(os.path.join('data', today_date, '1m', stock_name+'.txt')) is False:
            return None, []
        today_data = open(os.path.join('data', today_date, '1m', stock_name+'.txt'), 'r').read().splitlines()
        if len(today_data) == 0:
        	return None, []
        for i in range(len(today_data)):
            if today_data[0].split(',')[1].strip() == '08:46':
                is_first = True
            else:
                is_first = False
                h, m = today_data[0].split(',')[1].strip().split(':')                
                if (int(h)*60+int(m)) % interval == 1 or interval == 1:
                    today_data = today_data[i:]
                    break

        price = np.array([[float(int(dd)*0.01) for dd in d.split(',')[2:]] for d in today_data])
        price = get_ticks_with_interval(price, interval)

    else:
        if os.path.isfile(os.path.join('data', today_date, '5m', stock_name+'.txt')) is False:
            return None, []
        today_data = open(os.path.join('data', today_date, '5m', stock_name+'.txt'), 'r').read().splitlines()   
        for i in range(len(today_data)):
            if today_data[0].split(',')[1].strip() == '08:50':
                is_first = True
            else:
                is_first = False
                h, m = today_data[0].split(',')[1].strip().split(':')
                if (((int(h)*60+int(m)+16*60+45)%24*60)//5) % (interval//5) == 1 or interval == 5:
                    today_data = today_data[i:]
                    break
        price = np.array([[float(int(dd)*0.01) for dd in d[2:]] for d in today_data])
        price = get_ticks_with_interval(price, interval//5)
    return is_first, price

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