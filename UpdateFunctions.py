import urllib
import urllib2
import datetime
import os

currentPath=os.getcwd()
os.chdir(currentPath)

def makeUrl(tickerSymbol,numberOfDays):
    if '.' in tickerSymbol:
        symbolList = tickerSymbol.split('.')
        tickerSymbol = symbolList[0] + '-' + symbolList[1]
    baseUrl = "http://ichart.finance.yahoo.com/table.csv?s="
    today = datetime.datetime.now()
    numberOfDaysDate = datetime.timedelta(days=numberOfDays)
    earlierDay = today - numberOfDaysDate
    todayList = today.strftime("%x").split('/')
    earlierDayList = earlierDay.strftime("%x").split('/')
    dates = '&a=' + str(int(earlierDayList[0])-1) + '&b=' + str(earlierDayList[1]) + '&c=20' + str(earlierDayList[2])
    dates += '&d=' + str(int(todayList[0])-1) + '&e=' + str(todayList[1]) + '&f=20' + str(todayList[2])
    return baseUrl + tickerSymbol + dates

def makeFilename(tickerSymbol, directory="S&P"):
    return directory + "/" + tickerSymbol + ".csv"

def pullHistoricalData(tickerSymbol, numberOfDays, directory="S&P"):
    testFilePath = directory + '/TEST.csv'
    gotData=False
    try:
        urllib.urlretrieve(makeUrl(tickerSymbol,numberOfDays),testFilePath)
    except urllib.ContentTooShortError as e:
        outfile = open(testFilePath, "w")
        outfile.write(e.content)
        outfile.close()
    infile = open(testFilePath)
    fileString = infile.read()
    if not ('DOCTYPE' in fileString or 'doctype' in fileString):
        finalOutfile = open(makeFilename(tickerSymbol,directory),'w')
        finalOutfile.write(fileString)
        finalOutfile.close()
        gotData=True
    infile.close()
    return gotData

def makeLondonUrl(tickerSymbol,numberOfDays):
    if '.' in tickerSymbol:
        symbolList = tickerSymbol.split('.')
        tickerSymbol = symbolList[0] + '-' + symbolList[1]
    baseUrl = "http://ichart.finance.yahoo.com/table.csv?s="
    today = datetime.datetime.now()
    numberOfDaysDate = datetime.timedelta(days=numberOfDays)
    earlierDay = today - numberOfDaysDate
    todayList = today.strftime("%x").split('/')
    earlierDayList = earlierDay.strftime("%x").split('/')
    dates = '&a=' + str(int(earlierDayList[0])-1) + '&b=' + str(earlierDayList[1]) + '&c=20' + str(earlierDayList[2])
    dates += '&d=' + str(int(todayList[0])-1) + '&e=' + str(todayList[1]) + '&f=20' + str(todayList[2])
    return baseUrl + tickerSymbol +'.L'+ dates
 
def pullHistoricalLondonData(tickerSymbol, numberOfDays, directory="London"):
    testFilePath = directory + '/TEST.csv'
    gotData=False
    try:
        urllib.urlretrieve(makeLondonUrl(tickerSymbol,numberOfDays),testFilePath)
    except urllib.ContentTooShortError as e:
        outfile = open(testFilePath, "w")
        outfile.write(e.content)
        outfile.close()
    infile = open(testFilePath)
    fileString = infile.read()
    if not ('DOCTYPE' in fileString or 'doctype' in fileString):
        finalOutfile = open(makeFilename(tickerSymbol,directory),'w')
        finalOutfile.write(fileString)
        finalOutfile.close()
        gotData=True
    infile.close()
    return gotData

def getLastDate(stock,directory='All',daysPrevious=1):
    date=[]
    x = directory+'/' + stock + '.csv'
    if os.path.isfile(x):
        f = open(x)
        for n in range(daysPrevious):
            f.readline()
        line=f.readline()
        while len(date)<3:
            date += [line.split(',')[0]]
            line=f.readline()
            if line == '':
                date[0]='1900-01-01'
                break
        return date[0]
    else:
        return '1900-01-01'

def getLastDateBig(stock,daysPrevious=1):
    date=[]
    x = 'big/' + stock + '.csv'
    if os.path.isfile(x):
        f = open(x)
        for n in range(daysPrevious):
            f.readline()
        line=f.readline()
        while len(date)<3:
            date += [line.split(',')[0]]
            line=f.readline()
            if line == '':
                date[0]='1900-01-01'
                break
        return date[0]
    else:
        return '1900-01-01'

def UpdateTickerListSP500():
    tempList=[]
    response =urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    SP500Html = response.read()
    outfile = open('ListOfSP500html.txt','w+')
    for line in SP500Html:
        outfile.write(line)
    outfile.close()
    infile = open('ListOfSP500html.txt')
    for line in infile:
        if 'nyse.com' in line:
            subline = line[line.find('nyse.com'):]
            stock = subline[subline.find('>')+1:subline.find('<')]
            tempList = tempList + [stock]
        if 'nasdaq.com' in line:
            subline = line[line.find('nasdaq.com'):]
            stock = subline[subline.find('>')+1:subline.find('<')]
            tempList = tempList + [stock]
    infile.close()
    newoutfile = open('ListOfSP500.txt','w')
    tempListStr = ','.join(tempList)
    newoutfile.write(tempListStr)
    newoutfile.close()
    os.remove('ListOfSP500html.txt')
    return tempList

def updateDowJones(path='All',number=200):
    # fix date
    date=getLastDate('A',path)
    dateList=date.split('-')
    tempData=[]
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    urlStart='https://www.google.com/finance/historical?q=INDEXDJX%3A.DJI&startdate='+\
        months[int(dateList[1])-1]+'+'+dateList[2]+'%2C+'+str(int(dateList[0])-3)+'&enddate='+\
        months[int(dateList[1])-1]+'+'+dateList[2]+'%2C+'+str(int(dateList[0]))+'&start='
    urlEndList=['0&num=200','200&num=400','400&num=600','600&num=800']
    for i in range(4):
        tempUrl=urlStart+urlEndList[i]
        response =urllib2.urlopen(tempUrl)
        dowJonesHtml = response.read()
        outfile = open('DOWJONES.txt','w+')
        for line in dowJonesHtml:
            outfile.write(line)
        outfile.close()
        infile = open('DOWJONES.txt')
        for line in infile:
            if '<td class="lm">' in line:
                tempValue=line.split('>')[1][:-1]
                tempValue=''.join(tempValue.split(','))
                tempValue=tempValue.split(' ')
                tempData=tempData+[tempValue[2]+'-'+str(months.index(tempValue[0])+1)+'-'+tempValue[1]]
            if '<td class="rgt">' in line:
                tempValue=line.split('>')[1]
                tempValue=''.join(tempValue.split(','))
                tempData[-1]=tempData[-1]+','+tempValue[:-1]
            if '<td class="rgt rm">' in line:
                tempValue=line.split('>')[1]
                tempValue=''.join(tempValue.split(','))
                tempData[-1]=tempData[-1]+','+tempValue
        infile.close()
    os.remove('DOWJONES.txt')
    outfile=open(path+'/DOWJONES.csv','w')
    outfile.write('Date,Open,High,Low,Close,Volume,Adj Close\n')
    for line in tempData:
        outfile.write(line)
    outfile.close()

def updateTickerFromTable(ticker,path='big'):
    date=getLastDate('A')
    dateList=date.split('-')
    tempDataFinal=[]
    urlStart='https://finance.yahoo.com/q/hp?s='+ticker+'&a='+dateList[1]+'&b='+dateList[2]+'&c='+str(int(dateList[0])-2)+'&d='+dateList[1]+'&e='+dateList[2]+'&f='+dateList[0]+'&g=d'
    urlEndList=['','&z=66&y=66','&z=66&y=132','&z=66&y=198','&z=66&y=264','&z=66&y=330']
    for i in range(5):
        tempData=[]
        tempUrl=urlStart+urlEndList[i]
        response =urllib2.urlopen(tempUrl)
        dowJonesHtml = response.read()
        outfile = open('tempTicker.txt','w')
        for line in dowJonesHtml:
            outfile.write(line)
        outfile.close()
        infile = open('tempTicker.txt','r')
        for line in infile:
            if 'tabledata1' in line:
                tempData=line.split('</td>')
        for line in tempData:
            if 'Dividend' in line:
                del tempData[tempData.index(line)-1]
                tempData.remove(line)
            elif 'Split' in line:
                tempData.remove(line)
        for n in range(len(tempData)):
            tempData[n] = tempData[n][tempData[n].rfind('>')+1:]
            if n%7 == 0:
                tempData[n] = tempData[n][:tempData[n].find(',')]+'-'+tempData[n][1+tempData[n].find(','):]
            else:
                while ',' in tempData[n]:
                    tempData[n]=tempData[n][:tempData[n].find(',')]+tempData[n][tempData[n].find(',')+1:]
        infile.close()
        tempDataFinal+=tempData[0:-1]
    newoutfile=open(path+'/'+ticker+'.csv','w')
    newoutfile.write('Date,Open,High,Low,Close,Volume,AdjClose'+' \n')
    for n in range(len(tempDataFinal)):
        if (n+1)%7 == 0:
            newoutfile.write(tempDataFinal[n]+'\n')
        else:
            newoutfile.write(tempDataFinal[n]+',')
    newoutfile.close()

def getTickerListSP500():
    infile = open('ListOfSP500.txt')
    stockListString =''
    stockList=[]
    for line in infile:
        stockListString = stockListString + line
    stockList = stockListString.split(',')
    return stockList
    infile.close()

def getTickerList(n=0):
    infile = open('listOfStocks.txt')
    stockListString =''
    stockListString=infile.read()
    tempStockList= stockListString.split(',')
    stockList=[]
    m = len(tempStockList)/2
    for k in range(m):
        stockList += [(tempStockList[2*k][2:-1],tempStockList[2*k+1][2:-2])]
    if  n == 0 or n==1:
        finalStockList=[]
        for stockTuple in stockList:
            finalStockList += [stockTuple[n]]
        return finalStockList
    infile.close()
    return stockList

def getLondonTickerList(n=0):
    infile = open('listOfLondonStocks.txt')
    stockListString =''
    stockListString=infile.read()
    tempStockList= stockListString.split(',')
    stockList=[]
    m = len(tempStockList)/2
    for k in range(m):
        stockList += [(tempStockList[2*k][2:-1],tempStockList[2*k+1][2:-2])]
    if  n == 0 or n==1:
        finalStockList=[]
        for stockTuple in stockList:
            finalStockList += [stockTuple[n]]
        return finalStockList
    infile.close()
    return stockList

def getValues(stock,numberOfDays,directory='All'):
    #returns a list of stock prices for a number of pervious days
    # n=0 Date, n=1 Open, n=2 High, n=3 Low, n=4 Close
    # n=5 Volume, n=6 Adj Close
    values = []
    x = directory+'/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(values) < numberOfDays:
        tempLine = f.readline()[:-1]
        if tempLine == '':
            break
        tempValues = tempLine.split(',')
        for n in range(1,5):
            tempValues[n]=''.join(tempValues[n].split(','))
            tempValues[n]=float(tempValues[n])
        values += [tempValues]
    return values

def getClosingValue(numberOfDays,stock):
    #returns a list of stock prices for a number of pervious days
    closingValue = []
    x = 'All/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(closingValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[4]
        tempValue=''.join(tempValue.split(','))
        closingValue += [float(tempValue)]
    return closingValue

def getLowValue(numberOfDays,stock):
    lowValue = []
    x = 'All/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(lowValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[3]
        tempValue=''.join(tempValue.split(','))
        lowValue += [float(tempValue)]
    return lowValue

def getHighValue(numberOfDays,stock):
    highValue = []
    x = 'All/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(highValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[2]
        tempValue=''.join(tempValue.split(','))
        highValue += [float(tempValue)]
    return highValue

def getValue(numberOfDays,stock,n):
    # n=0 Date, n=1 Open, n=2 High, n=3 Low, n=4 Close
    # n=5 Volume, n=6 Adj Close
    value = []
    x = 'All/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(highValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        value += [float(tempLine.split(',')[n])]
    return value

def getDate(stock,daysAgo=1):
    date=[]
    x = 'All/' + stock + '.csv'
    f = open(x)
    f.readline()
    line=f.readline()
    while line != '':
        shortDate = line.split(',')[0]
        shortDate = shortDate.split('-')[1:3]
        shortDate = '-'.join(shortDate)
        date = [shortDate]+date
        line=f.readline()
    return date
    
def getFileLines(stock,path='All'):
    x = path+'/'+stock+'.csv'
    if os.path.isfile(x):
        f = open(x)
        n=0
        line = f.readline()
        while line != '':
            n+=1
            line = f.readline()
        return n
    else:
        return 0

def getClosingValueBig(numberOfDays,stock):
    #returns a list of NYSE stock prices for a number of pervious days
    closingValue = []
    x = 'big/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(closingValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[4]
        tempValue=''.join(tempValue.split(','))
        closingValue += [float(tempValue)]
    return closingValue

def getOpeningValueBig(numberOfDays,stock):
    #returns a list of NYSE stock prices for a number of pervious days
    closingValue = []
    x = 'big/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(closingValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[1]
        tempValue=''.join(tempValue.split(','))
        closingValue += [float(tempValue)]
    return closingValue

def getLowValueBig(numberOfDays,stock):
    lowValue = []
    x = 'big/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(lowValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[3]
        tempValue=''.join(tempValue.split(','))
        lowValue += [float(tempValue)]
    return lowValue

def getHighValueBig(numberOfDays,stock):
    highValue = []
    x = 'big/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(highValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        tempValue = tempLine.split(',')[2]
        tempValue=''.join(tempValue.split(','))
        highValue += [float(tempValue)]
    return highValue

def getValueBig(numberOfDays,stock,n):
    # n=0 Date, n=1 Open, n=2 High, n=3 Low, n=4 Close
    # n=5 Volume, n=6 Adj Close
    value = []
    x = 'big/' + stock + '.csv'
    f = open(x)
    f.readline()
    while len(highValue) < numberOfDays:
        tempLine = f.readline()
        if tempLine == '':
            break
        value += [float(tempLine.split(',')[n])]
    return value

def getDateBig(stock):
    date=[]
    x = 'big/' + stock + '.csv'
    f = open(x)
    f.readline()
    line=f.readline()
    while line != '':
        shortDate = line.split(',')[0]
        date = date+[shortDate]
        line=f.readline()
    return date
    
def getFileLinesBig(stock):
    x = 'big/'+stock+'.csv'
    if os.path.isfile(x):
        f = open(x)
        n=0
        line = f.readline()
        while line != '':
            n+=1
            line = f.readline()
        return n
    else:
        return 0
    
def getDataSP500():
    tempTickerList=getTickerListSP500()
    for ticker in tempTickerList:
        print ticker
        pullHistoricalData(ticker,20,'All')

def updateFromGoogle(ticker,market,path='AllGoogle'):
    urlString='http://www.google.com/finance/historical?q='+market+'%3A'+ticker+'&output=csv'
    response=urllib2.urlopen(urlString)
    tempFileString=response.read()
    tempFile=open(path+'/'+ticker+'.csv','a')
    tempFile.seek(0)
    tempFile.truncate()
    tempFile.write(tempFileString)
    tempFile.close()
    response.close()

def updateAllStocksGoogle():
    tickerList=getTickerList()[:5]
    market='NYSE'
    redo=[]
    for ticker in tickerList:
        print ticker+' Google'
        try:
            updateFromGoogle(ticker,market)
        except urllib2.HTTPError as e:
            path='AllGoogle/'+ticker+'.csv'
            outfile = open(path, "w")
            outfile.write('HTTPError')
            outfile.close() 
            redo=redo+[(ticker,str(market))]
        if ticker=='ZX':
            market='NASDAQ'
        
    for ticker in redo:
        print ticker[0]+' Google Redo'
        try:
            updateFromGoogle(ticker[0],ticker[1])
        except urllib2.HTTPError as e:
            path='AllGoogle/'+ticker[0]+'.csv'
            outfile = open(path, "w")
            outfile.write('HTTPError')
            outfile.close() 

def getGoogleDayData(ticker,date):
    tempFile=open('AllGoogle/'+ticker+'.csv','r')
    for line in tempFile:
        if ',' in line:
            tempLineList=line.split(',')
            if tempLineList[0]==date:
                return line
    return ''

