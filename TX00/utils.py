import os
from time import gmtime, strftime, sleep

def findLastDateByStock(filename, todayDatestamp):
    maxInteger, lastDate = -1, ''
    for dir, _, _ in os.walk('data'):
        if isFileExistInDir(dir, filename):
            datestamp = extractDatestampByLastDir(dir)
            datestampToInteger = convertDatestampToInteger(datestamp)
            if datestampToInteger > maxInteger and datestamp != todayDatestamp:
                maxInteger, lastDate = datestampToInteger, datestamp
    return lastDate

def isFileExistInDir(path, filename):
    return os.path.isfile(os.path.join(path, filename))

def extractDatestampByLastDir(path):
    return path.split('\\')[-1]

def convertDatestampToInteger(datestamp):
    dateYear, dateMonth, dateDay = datestamp.split('-')
    return int(dateYear)*(12*31) + int(dateMonth)*31 + int(dateDay)

def convertTimestampToInteger(timestamp):
    return int(timestamp.split(':')[0])*60+int(timestamp.split(':')[1])

def convertIntegerToTimestamp(integer):
    return "%.2d:%.2d"%(integer//60, integer%60)

def removeDataUntilLastDate(data, lastDate):
    newData = []
    for datum in data:
        comp = datum.split(',')
        date = comp[0].strip().replace('/', '-')
        if lastDate != '' and date <= lastDate:
            continue

        timestamp = comp[1].strip()
        timeToInteger = convertTimestampToInteger(timestamp)
        if 13*60+46<=timeToInteger<=15*60:
            continue
        else:
            newData.append(datum)
    return newData

def writeFileWithContent(filename, content):
    createParentFolderIfNotExist(filename)
    open(filename, 'w').write(content)   

def createParentFolderIfNotExist(path):
    parentFolder = '\\'.join(path.split('\\')[:-1])
    if os.path.isdir(parentFolder) is False:
        os.makedirs(parentFolder)

def intListToStrList(numList):
    return [str(n) for n in numList]

def priceMultiplyOnePercent(price):
    newPrice = []
    for p in price:
        if p.strip()[-2:] == "00":
            newPrice.append(int(p.strip()[:-2]))
        else:
            newPrice.append(round(int(p.strip())*0.01, 2))
    return newPrice

def getPastFolderDate():
    folderDate = []
    for dir, _, _ in os.walk('data'):
        if len(dir.split('\\')) != 2:
            continue
        folderDate.append(extractDatestampByLastDir(dir))
    folderDate.sort()
    return folderDate

def clearFile(filename):
    if os.path.isfile(filename) is True:
        os.remove(filename)
    _ = open(filename, 'w')

def isNaN(data):
    return data != data

def checkTimeValid(prevTimestamp, currentTimestamp):
    currentTimeInteger = (convertTimestampToInteger(currentTimestamp) + 8*60) % (24*60)

    if prevTimestamp != currentTimestamp and (8*60+45 <= currentTimeInteger <= 13*60+45 or 15*60 <= currentTimeInteger or currentTimeInteger <= 5*60):
        return "Valid", currentTimeInteger
    else:
        return "Wait", currentTimeInteger
    

