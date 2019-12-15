import urllib
import urllib
import os
from UpdateFunctions import*

override=True

currentPath=os.getcwd()
os.chdir(currentPath)

def updateTickerList():
    tempList=[]
    marketList=['NYSE','NASDAQ']
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    dateResponse=urllib2.urlopen('http://www.eoddata.com')
    defaultStockHtml=dateResponse.read()
    intermediateDate = defaultStockHtml.split('New York Stock Exchange</td><td>')
    date = intermediateDate[-1].split(' ')[0]
    dateList=date.split('/')
    dateData= '20' + dateList[2] + '-' + dateList[0] + '-' + dateList[1]
    print dateData
    for market in marketList:
        for letter in alphabet:
            print market + ' ' + letter
            response=urllib2.urlopen('http://www.eoddata.com/stocklist/'+market+'/'+letter+'.htm')
            stockHtml = response.read()
            outfile = open('listOfStocksHtml/'+market+letter+'.txt','w')
            for line in stockHtml:
                outfile.write(line)
            outfile.close()

            infile = open('listOfStocksHtml/'+market+letter+'.txt')
            for line in infile:
                if 'Display Quote' in line:
                    a=line.split('<')
                    stockTicker = a[3].split('>')[-1]
                    stockName = a[6].split('>')[-1]
                    tempList += [str((stockTicker,stockName))]
    newoutfile = open('listOfStocks.txt','w')
    tempListStr = ','.join(tempList)
    newoutfile.write(tempListStr)
    newoutfile.close()
    return tempList

def updateLondonTickerList():
    tempList=[]
    marketList=['LSE']
    alphabet = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    dateResponse=urllib2.urlopen('http://www.eoddata.com')
    defaultStockHtml=dateResponse.read()
    intermediateDate = defaultStockHtml.split('London Stock Exchange</td><td>')
    date = intermediateDate[-1].split(' ')[0]
    dateList=date.split('/')
    dateData= '20' + dateList[2] + '-' + dateList[0] + '-' + dateList[1]
    print dateData
    for market in marketList:
        for letter in alphabet:
            print market + ' ' + letter
            response=urllib2.urlopen('http://www.eoddata.com/stocklist/'+market+'/'+letter+'.htm')
            stockHtml = response.read()
            outfile = open('listOfLondonStocksHtml/'+market+letter+'.txt','w')
            for line in stockHtml:
                outfile.write(line)
            outfile.close()

            infile = open('listOfLondonStocksHtml/'+market+letter+'.txt')
            for line in infile:
                if 'Display Quote' in line:
                    a=line.split('<')
                    stockTicker = a[3].split('>')[-1]
                    stockName = a[6].split('>')[-1]
                    tempList += [str((stockTicker,stockName))]
    newoutfile = open('listOfLondonStocks.txt','w')
    tempListStr = ','.join(tempList)
    newoutfile.write(tempListStr)
    newoutfile.close()
    return tempList
	
def updateDataAll(overRide):
    marketList=['NYSE','NASDAQ']
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    dateResponse=urllib2.urlopen('http://www.eoddata.com')
    defaultStockHtml=dateResponse.read()
    intermediateDateNYSE = defaultStockHtml.split('New York Stock Exchange</td><td>')
    dateNYSE = intermediateDateNYSE[-1].split('</td>')[0]
    dateListNYSE=dateNYSE.split('/')
    if len(dateListNYSE[2])>2:
        timeNYSE = dateListNYSE[2][3:]
    else:
        timeNYSE = ''
    dateDataNYSE= '20' + dateListNYSE[2][:2] + '-' + dateListNYSE[0] + '-' + dateListNYSE[1]
    intermediateDateNASDAQ = defaultStockHtml.split('NASDAQ Stock Exchange</td><td>')
    dateNASDAQ = intermediateDateNASDAQ[-1].split('</td>')[0]
    dateListNASDAQ=dateNASDAQ.split('/')
    if len(dateListNASDAQ[2])>2:
        timeNASDAQ = dateListNASDAQ[2][3:]
    else:
        timeNASDAQ = ''
    dateDataNASDAQ= '20' + dateListNASDAQ[2][:2] + '-' + dateListNASDAQ[0] + '-' + dateListNASDAQ[1]
    print 'NYSE data date ' + dateDataNYSE
    print 'NYSE data time ' + timeNYSE
    print 'NASDAQ date data ' + dateDataNASDAQ
    print 'NASDAQ date time ' + timeNASDAQ
    if ((not overRide) and (dateDataNYSE != dateDataNASDAQ or timeNYSE != timeNASDAQ or timeNYSE != '')):
        print 'Please check dates'
    else:
        dateData=dateNYSE
        for market in marketList:
            for letter in alphabet:
                print 'Writing data for ' + market + ' ' + letter
                infile = open('listOfStocksHtml/'+market+letter+'.txt')
                for line in infile:
                    if 'Display Quote' in line:
                        lineList=line.split('<')
                        stockTicker = lineList[3].split('>')[-1]
                        stockName = lineList[6].split('>')[-1]
                        highPrice = ''.join(lineList[8].split('>')[-1].split(','))
                        lowPrice = ''.join(lineList[10].split('>')[-1].split(','))
                        closingPrice = ''.join(lineList[12].split('>')[-1].split(','))
                        volume=''.join(lineList[14].split('>')[-1].split(','))
                        openingPrice = str(float(closingPrice)-float(''.join(lineList[16].split('>')[-1].split(','))))
                        if not os.path.isfile('All/'+stockTicker+'.csv'):
                            open('All/'+stockTicker+'.csv','a').close()
                        infileDataList=[0]
                        if getLastDate(stockTicker) != dateData:
                            infileData = open('All/'+stockTicker+'.csv')
                            for line in infileData:
                                infileDataList=infileDataList+[line]
                            if len(infileDataList)==1:
                                    infileDataList=infileDataList+['Date,Open,High,Low,Close,Volume,Adj Close \n']
                            infileDataList[0]=infileDataList[1]
                            infileDataList[1]=dateData +','+openingPrice+','+highPrice+','+lowPrice+','+closingPrice+','+volume+','+'Adj.\n'
                            infileData.close()
                            outfileData=open('All/'+stockTicker+'.csv','w')
                            if len(infileDataList)<18:
                                for i in range(len(infileDataList)):
                                    outfileData.write(infileDataList[i])
                            else:
                                for i in range(18):
                                    outfileData.write(infileDataList[i])
                            outfileData.close() 
                infile.close()


def dataUnfucker():
    tickerList=getTickerList()
    for ticker in tickerList:
        tickerPath ='All/' + ticker + '.csv'
        f = open(tickerPath)
        dataList=[]
        dataList+=[f.readline()]
        if dataList[0][0] == '<':
            print ticker
            dataList[0] = 'Date,Open,High,Low,Close,Volume,Adj Close\n'
            nextLine = f.readline()
            while nextLine[0] in ['0','1','2','3']:
                dataList+=[nextLine]
                nextLine=f.readline()
                if nextLine == '':
                    break
        else:
            nextLine = f.readline() 
            while nextLine != '':
                if len(dataList) == 18:
                    break
                dataList+=[nextLine]
                nextLine=f.readline()
        for n in range(len(dataList)):
            line = dataList[n]
            lineList = line.split(',')
            if '/' in lineList[0]:
                tempLineList = lineList[0].split('/')
                lineList[0] = '20'+tempLineList[2][:2]+'-'+tempLineList[0]+'-'+tempLineList[1]
            dataList[n] = ','.join(lineList)
        f.close()
        g=open(tickerPath,'w')
        dates=[]
        for line in dataList:
            tempDate=[line.split(',')[0]]
            if not tempDate in dates:
                dates+=[tempDate]
                g.write(line)
        g.close()

def updateTickerListSP500():
    tempList=[]
    response =urllib2.urlopen('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    SP500Html = response.read()
    outfile = open('ListOfSP500html.txt','w')
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
    return tempList

def googleDataUnfucker():
    months={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    tickerList=getTickerList()[:5]
    for ticker in tickerList:
        print ticker
        fileLines=[]
        tempFile=open('AllGoogle/'+ticker+'.csv','r')
        nextLine=tempFile.readline()
        while nextLine!='':
            fileLines=fileLines+[nextLine]
            nextLine=tempFile.readline()
        tempFile.close()
        for n in range(len(fileLines)):
            tempLine=fileLines[n]
            if ',' in tempLine and not 'Date' in tempLine:
                tempLineList=tempLine.split(',')
                dateList=tempLineList[0].split('-')
                if len(dateList[0])<2:
                    dateList[0]='0'+dateList[0]
                date='20'+dateList[2]+'-'+months[dateList[1]]+'-'+dateList[0]
                fileLines[n]=date+','+(',').join(tempLineList[1:])
        tempFile=open('AllGoogle/'+ticker+'.csv','w')
        tempFile.seek(0)
        tempFile.truncate()
        for line in fileLines:
            tempFile.write(line)
        tempFile.close()

#updateTickerList()
updateTickerListSP500()
#updateDataAll(override)
#dataUnfucker()
#updateDowJones()
