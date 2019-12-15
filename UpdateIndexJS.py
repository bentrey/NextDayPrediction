import random
import os
import binascii
import glob
import csv
import datetime
import math
import urllib
import random
import pylab
import numpy
from collections import Counter
from xlsxwriter.workbook import Workbook
from numpy import linalg
from UpdateFunctions import*

tickerListSP500 = getTickerListSP500()
tickerList=getTickerList(2)
tickerListSP500.sort()
tickerList.sort()

currentPath=os.getcwd()
os.chdir(currentPath)

def updateFiles(prices,days):
    infile=open('indexForm.html')
    outfile=open('index.html','w')
    start = False
    for line in infile:
        if '<!-- Using data from some date -->' in line:
            print 'Date writing'
            month = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December','1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September'}
            dateString = getLastDate('A')
            dateList=dateString.split('-')
            date = datetime.datetime(int(dateList[0]),int(dateList[1]),int(dateList[2]))
            if date.weekday() == 4:
                delta = datetime.timedelta(days=3)
            else:
                delta = datetime.timedelta(days=1)
            date = date + delta
            dateLine = '<p>Predicting closing values for ' + month[date.month]+ ' ' + str(date.day) + ' ' + str(date.year) + '</p>'
            outfile.write(dateLine)
        elif '<!-- S&P 500 Stock Chart -->' in line:
            print 'S&P 500 Stock Chart writing'
            line = prices
            outfile.write(line)
        elif '<!-- Function S&P 500 Stock Chart -->' in line:
            print 'S&P 500 chart writing'
            line = 'document.getElementById("results").innerHTML=' +"'"+ prices[18:-6] + "'; \n"
            outfile.write(line)
        elif '//add stock prices' in line:
            print 'Stock prices writing'
            tickerListDow = tickerList+[('DOWJONES','DOWJONES')]
            tickerTupleList=[]
            tickerListJS= 'available = ['
            for tickerTuple in tickerListDow:
                ticker = tickerTuple[0]
                if getFileLines(ticker)>13:
                    tickerTupleList += [tickerTuple]
                    if ticker != 'DOWJONES':
                        tickerListJS += ' "' + ticker + '" ,' 
                    data = []
                    priceData = 'stockList["' + ticker + '"] = '
                    x = 'All/' + ticker + '.csv'
                    f = open(x)
                    f.readline()
                    for n in range(days):
                        dayDataList = f.readline().split(',')
                        dayDataList[-1]=dayDataList[-1][:-4]
                        if ticker == 'DOWJONES':
                            for n in range(1,len(dayDataList)-1):
                                dayDataList[n]=float(''.join(dayDataList[n].split(',')))
                            data += [dayDataList]
                        else:
                            dayDataList[4]=float(''.join(dayDataList[4].split(',')))
                            data += [dayDataList[4]]
                    if ticker == 'DOWJONES':
                        dowJonesData = str(data)+'; \n'
                    f.close()
                    priceData += str(data) + '; \n'
                    outfile.write(priceData)
            tickerListJS = tickerListJS[:-1] + ']; \n'
            outfile.write(tickerListJS)
        else:
            outfile.write(line)
    infile.close()
    outfile.close()
    
    print 'Writing allTickers.ejs'
    outfile2 = open('allTickers.ejs','w')
    infile2 = open('allTickersForm.ejs','r')
    tickerTupleList=tickerTupleList[:-1]
    tickerTupleList.sort()
    for line in infile2:
        if '<!-- symbols>' in line:
            outfile2.write('<table>')
            for tickerTuple in tickerTupleList:
                outfile2.write('<tr><td>'+tickerTuple[0]+'</td><td>'+tickerTuple[1]+'</td></tr>')
            outfile2.write('</table>')
        else:
            outfile2.write(line)
    outfile2.close()
    infile2.close()
    
    print 'Writing allValues.ejs'
    outfile3 = open('allValues.ejs','w')
    infile3 = open('allValuesForm.ejs','r')
    for line in infile3:
        if '//add stock prices' in line:
            tickerTupleList = tickerTupleList + [('DOWJONES','DOWJONES')]
            for tickerTuple in tickerTupleList:
                ticker = tickerTuple[0]
                if ticker == 'DOWJONES':
                    outfile3.write('stockList["DOWJONES"]='+dowJonesData)
                else:
                    outfile3.write('stockList["'+ticker+'"]='+str(getClosingValue(10,ticker))+'; \n')
            outfile3.write(tickerListJS)             
        else:
            outfile3.write(line)
    outfile3.close()
    infile3.close()
    
    print 'Writing SP500Values.ejs'
    outfile4 = open('SP500Values.ejs','w')
    infile4 = open('SP500ValuesForm.ejs','r')
    SP500TickerListJS= 'available = ['
    for line in infile4:
        if '//add stock prices' in line:
            SP500TickerList = getTickerListSP500() + ['DOWJONES']
            for ticker in SP500TickerList:
                if(getFileLines(ticker)>17):
                    if('BRK' in ticker or 'BF' in ticker):
                        ticker='.'.join(ticker.split('-'))
                    if ticker == 'DOWJONES':
                        outfile4.write('stockList["DOWJONES"]='+dowJonesData)
                    else:
                        outfile4.write('stockList["'+ticker+'"]='+str(getClosingValue(10,ticker))+'; \n')
                        SP500TickerListJS=SP500TickerListJS+'"'+ticker+'", '
            outfile4.write(SP500TickerListJS[:-2]+' ] \n')             
        else:
            outfile4.write(line)
    outfile4.close()
    infile4.close()
        
    print 'Writing hotStocks.ejs'
    outfile5 = open('hotStocks.ejs','w')
    infile5 = open('hotStocksForm.ejs','r')
    hotStockList=hotStocks(0)
    hotTupleList=[]
    for tickerTuple in tickerTupleList:
        if tickerTuple[0] in hotStockList:
            hotTupleList+=[tickerTuple]
    hotTupleList.sort()
    for line in infile5:
        if '<!-- symbols>' in line:
            outfile5.write('<p>Hot Stocks for '+month[date.month]+ ' ' + str(date.day) + ', ' + str(date.year)+'<p>')
            outfile5.write('<table>')
            for tickerTuple in hotTupleList:
                outfile5.write('<tr><td>'+tickerTuple[0]+'</td><td>'+tickerTuple[1]+'</td></tr>')
            outfile5.write('</table>')
        else:
            outfile5.write(line)
    outfile5.close()
    infile5.close()

    print 'Writting getValues.ejs'
    outfile6=open('getValues.ejs','w')
    infile6=open('getValuesForm.ejs','r')
    for line in infile6:
        if '<!-- hot stocks -->' in line:
            outfile6.write("<p class=\"sublead\">Get Hot Stocks 4.00 USD </p><p> Last Trading Day's average percent increase </p> <p>Hot Stock's average percent increase: " + str(getHotStockPC()*100)[:5]+'% </p> <p>S&P 500 percent increase: '+str(getSP500PC()*100)[:5]+'% </p>')
        else:
            outfile6.write(line)
    outfile6.close()
    infile6.close()

    print 'Writting AllValues.xlsx'
    outfile7=open('allValues.csv','w')
    for TickerTuple in tickerTupleList[:-1]:
        try:
            if getFileLines(TickerTuple[0])>11:
                outfile7.write('\n')
                outfile7.write(TickerTuple[0]+'\n')
                brackets=getStandDevBrackets(getPricesCDF(10,0,TickerTuple[0]))
                alert=False
                if brackets[0]<=0:
                    brackets[0]=.02
                if brackets[1]<=0:
                    alert=True
                if alert:
                    outfile7.write('The prices are fluctuating to rapidly for accurate prediction. \n')
                else:
                    outfile7.write('Expected Percentage, Low Price, High Price \n')
                    percents=['2.27%','13.59%','34.13%','34.13%','13.59%','2.27%']
                    for n in range(len(brackets)-1):
                        if n==0:
                            firstPrice=str(round(brackets[0]-.01,2))                     
                            lastPrice=str(round(brackets[1]-.01,2))
                            outfile7.write(percents[0]+','+firstPrice+','+lastPrice+'\n')
                        elif n==len(brackets)-2:
                            firstPrice=str(round(brackets[n],2))                     
                            lastPrice=str(round(brackets[n+1]-.01,2))
                            outfile7.write(percents[-1]+','+firstPrice+','+lastPrice+'\n')
                        else:
                            firstPrice=str(round(brackets[n],2))                     
                            lastPrice=str(round(brackets[n+1]-.01,2))
                            outfile7.write(percents[n]+','+firstPrice+','+lastPrice+'\n')
        except ZeroDivisionError:
            print TickerTuple[0]+' zero division error.'
    outfile7.close()
    workbook=Workbook('allValues.xlsx')
    worksheet=workbook.add_worksheet()
    with open('allValues.csv', 'rb') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()

    print 'Writting SP500Values.xlsx'
    outfile8=open('SP500Values.csv','w')
    for TickerTuple in SP500TickerList[:-1]:
        TickerTuple='.'.join(TickerTuple.split('-'))
        if getFileLines(TickerTuple)>11:
            outfile8.write('\n')
            outfile8.write(TickerTuple+'\n')
            brackets=getStandDevBrackets(getPricesCDF(10,0,TickerTuple))
            alert=False
            if brackets[0]<=0:
                brackets[0]=.02
            if brackets[1]<=0:
                alert=True
            if alert:
                outfile8.write('The prices are fluctuating to rapidly for accurate prediction. \n')
            else:
                outfile8.write('Expected Percentage, Low Price, High Price \n')
                percents=['2.27%','13.59%','34.13%','34.13%','13.59%','2.27%']
                for n in range(len(brackets)-1):
                    if n==0:
                        firstPrice=str(round(brackets[0]-.01,2))                     
                        lastPrice=str(round(brackets[1]-.01,2))
                        outfile8.write(percents[0]+','+firstPrice+','+lastPrice+'\n')
                    elif n==len(brackets)-2:
                        firstPrice=str(round(brackets[n],2))                     
                        lastPrice=str(round(brackets[n+1]-.01,2))
                        outfile8.write(percents[-1]+','+firstPrice+','+lastPrice+'\n')
                    else:
                        firstPrice=str(round(brackets[n],2))                     
                        lastPrice=str(round(brackets[n+1]-.01,2))
                        outfile8.write(percents[n]+','+firstPrice+','+lastPrice+'\n')
    outfile8.close()
    workbook=Workbook('SP500Values.xlsx')
    worksheet=workbook.add_worksheet()
    with open('SP500Values.csv', 'rb') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()

def evalFuncCDFInv(Func,y):
    if y>Func[-1][1]:
        xn=Func[-1][0]
        yn=Func[-1][1]
        mi=(Func[-1][0]-Func[-2][0])/(Func[-1][1]-Func[-2][1])
        if Func[-1][1]==Func[-2][1]:
            z0=math.log(Func[0][1]/(1-Func[0][1]))
            z1=math.log(Func[-1][1]/(1-Func[-1][1]))
            zy=math.log(y/(1-y))
            x=Func[0][0]+(Func[-1][0]-Func[0][0])/(z1-z0)*(zy-z0)
        elif (2*yn-y)/y>0:
            x=xn-yn*math.log((2*yn-y)/y)*mi/2
        else:
            x=0
    elif y<Func[0][1]:
        x0=Func[0][0]
        y0=Func[0][1]
        mi=(Func[1][0]-Func[0][0])/(Func[1][1]-Func[0][1])
        if Func[1][1]==Func[0][1]:
            z0=math.log(Func[0][1]/(1-Func[0][1]))
            z1=math.log(Func[-1][1]/(1-Func[-1][1]))
            zy=math.log(y/(1-y))
            x=Func[0][0]+(Func[-1][0]-Func[0][0])/(z1-z0)*(zy-z0)
        elif y/(2*x0-y)>0:
            x = x0+y0*math.log(y/(2*x0-y))*mi/2
        else:
            x=0
    else:
        n=1
        while(y>Func[n][1]):
            n=n+1
        x=(Func[n][1]*Func[n-1][0]+y*Func[n][0]-y*Func[n-1][0]-Func[n-1][1]*Func[n][0])/(Func[n][1]-Func[n-1][1])
    return x

def determinant(matrix):
    levicivita=[[[0,0,0],[0,0,1],[0,-1,0]],[[0,0,-1],[0,0,0],[1,0,0]],[[0,1,0],[-1,0,0],[0,0,0]]]
    det=0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                det=det+levicivita[i][j][k]*matrix[0][i]*matrix[1][j]*matrix[2][k]
    return det
    
def funcInver(Func):
    #returns interchange of x and y
    inverFunc=[]
    for x in range(len(Func)):
        inverFunc += [(Func[x][1],Func[x][0])]
    return inverFunc

def getPricesCDF(days,daysPrev,stock):
    #days is the number of previous days data used, stockList is the list of stocks used
    #get dowJonesPrediction
    weights=[.1,1]
    dowJones=getClosingValue(days+daysPrev,'DOWJONES')[daysPrev:]
    dowJonesHighValue=getHighValue(days+daysPrev,'DOWJONES')[daysPrev:]
    dowJonesLowValue=getLowValue(days+daysPrev,'DOWJONES')[daysPrev:]
    change=[0]*(days-1)
    for n in range(days-1):
        change[n]=dowJones[n]-dowJones[n+1]
    dowJones=[dowJones[0]+numpy.mean(change)]+dowJones
    sigma=[0]*days
    for n in range(days):
        sigma[n]=dowJonesHighValue[n]-dowJonesLowValue[n]
    sigma=[weights[0]]+sigma
    m = [[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]
    tau = [0.,0.,0.]
    for i in range(3):
        for j in range(3):
            for t in range(-1,10):
                m[i][j]=m[i][j]+t**(i+j)/sigma[t+1]
    m[1][1]=m[1][1]+weights[1]
    for i in range(3):
        for t in range(-1,10):
            tau[i]=tau[i]+dowJones[t+1]*t**i/sigma[t+1]
    tau[1]=tau[1]+weights[1]*(dowJones[1]-dowJones[0])
    detm=determinant(m)
    mx=[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]
    my=[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]
    mz = [[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]
    for i in range(3):
        mx[i][0]=tau[i]
        my[i][0]=m[i][0]
        mz[i][0]=m[i][0]
        mx[i][1]=m[i][1]
        my[i][1]=tau[i]
        mz[i][1]=m[i][1]
        mx[i][2]=m[i][2]
        my[i][2]=m[i][2]
        mz[i][2]=tau[i]
    dowJonesPrediction=determinant(mx)/detm-determinant(my)/detm+determinant(mz)/detm
    #getting priceCDF
    closingValue=getClosingValue(days+daysPrev,stock)[daysPrev:]
    closingValuePC=[]
    for n in range(days-1):
        if (closingValue[n]*dowJones[n+2]/closingValue[n+1]/dowJones[n+1]>.7 and closingValue[n]*dowJones[n+2]/closingValue[n+1]/dowJones[n+1]<1.3):
            closingValuePC= closingValuePC+[closingValue[n]*dowJones[n+2]/closingValue[n+1]/dowJones[n+1]]
    closingValuePC.sort()
    CDFPC=[0]*len(closingValuePC)
    for n in range(len(closingValuePC)):
        CDFPC[n]=[closingValuePC[n],(n+0.5)/len(closingValuePC)]
    priceCDF=[0]*len(CDFPC)
    for n in range(len(CDFPC)):
        priceCDF[n]=[closingValue[0]*dowJonesPrediction/dowJones[1]*CDFPC[n][0],CDFPC[n][1]]
    return priceCDF
    
def get12StandDevBrackets(PricesCDF):
    #returns list of prices, 3 stand dev away from mean in half stand dev increments
    priceBrackets=[]
    halfStandDev=[.0013,.0062,.0228,.0668,.1587,.3085,.5,.6915,.8413,.9332,.9772,.9938,.9987]
    for x in halfStandDev:
        priceBrackets += [round(evalFuncCDFInv(PricesCDF,x),2)]
    return priceBrackets

def getStandDevBrackets(PricesCDF):
    #returns list of prices, 3 stand dev away from mean in half stand dev increments
    priceBrackets=[]
    standDev=[.0001,.0228,.1587,.5000,.8413,.9772,.9999]
    priceBrackets=[0]*len(standDev)
    for n in range(len(standDev)):
        priceBrackets[n] = round(evalFuncCDFInv(PricesCDF,standDev[n]),2)
    return priceBrackets

def whichBracketTest(daysPred,daysPrev,stock):
    #returnhs a bracket for a previous number of days
    brackets = get12StandDevBrackets(getPricesCDF(daysPred,daysPrev,stock))
    value=getClosingValue(daysPrev,stock)[-1]
    for x in range(len(brackets)-1):
        if (brackets[x] <= value and (value <= brackets[x+1])):
            return (x,x+1)


def getNextDayPercentChange(ticker):
    price = getClosingValue(10,ticker)
    sumP = 3*[0]
    for m in range(3):
        for n in range(10):
            sumP[m]+= n**(m)*price[n]
    alpha = -1.0/13272.0*sumP[2]+3.0/4424.0*sumP[1]-1.0/1106.0*sumP[0]
    beta = 3.0/4424.0*sumP[2]+4343.0/729960.0*sumP[1]-2823.0/60830.0*sumP[0]
    delta = -1.0/1106.0*sumP[2]-2823.0/60830.0*sumP[1]+10177.0/30415.0*sumP[0]
    nextDayPrice = alpha - beta + delta
    return [(nextDayPrice-price[0])/price[0],beta-2*alpha,2*alpha]

def updateJS():
    bracket=[]
    print 'Prices writing'
    for x in tickerListSP500:
        if getFileLines(x)>12:
            bracket += [whichBracketTest(10,1,x)]
    brackDict=Counter(bracket)
    tempSum=len(bracket)
    brackDict=Counter(bracket)
    prices = '<div id="results"><table width="400"><tr><td>Expected Percentage</td><td></td> <td>Actual Number in Bracket</td> </tr>'\
    +'<tr><td>2.28% </td><td></td><td>' + str(brackDict[(0,1)]+brackDict[(1,2)]) + '/' + str(tempSum)+'</td><td>'+str(round(float(brackDict[(0,1)]+brackDict[(1,2)])/float((tempSum))*100.0,2))+'% </td></tr>'\
    +'<tr><td>13.59% </td><td></td><td>' + str(brackDict[(2,3)]+brackDict[(3,4)]) + '/' + str(tempSum)+'</td><td>'+str(round(float(brackDict[(2,3)]+brackDict[(3,4)])/float((tempSum))*100.0,2))+ '% </td></tr>'\
    +'<tr><td>34.13% </td><td></td><td>' + str(brackDict[(4,5)]+brackDict[(5,6)]) + '/' + str((tempSum))+'</td><td>'+str(round(float(brackDict[(4,5)]+brackDict[(5,6)])/float((tempSum))*100.0,2))+ '% </td></tr>'\
    +'<tr><td>34.13% </td><td></td><td>' + str(brackDict[(6,7)]+brackDict[(7,8)]) + '/' + str((tempSum))+'</td><td>'+str(round(float(brackDict[(6,7)]+brackDict[(7,8)])/float((tempSum))*100.0,2))+ '% </td></tr>'\
    +'<tr><td>13.59% </td><td></td><td>' + str(brackDict[(8,9)]+brackDict[(9,10)]) + '/' + str((tempSum))+'</td><td>'+str(round(float(brackDict[(8,9)]+brackDict[(9,10)])/float((tempSum))*100.0,2))+ '% </td></tr>'\
    +'<tr><td>2.28% </td><td></td><td>' + str(brackDict[(10,11)]+brackDict[(11,12)]) + '/' + str((tempSum))+'</td><td>'+str(round(float(brackDict[(10,11)]+brackDict[(11,12)])/float((tempSum))*100.0,2))+ '% </td></tr></table></div>'
    updateFiles(prices,10)

def hotStocks(daysPrev,numberOfHotStocks=30,directory=''):
    tickerList=getTickerList(0)
    dowJones=getClosingValue(12+daysPrev,'DOWJONES')
    dowJones=dowJones[daysPrev:]
    stockInfoList=[]
    PCList=[]
    for ticker in tickerList:
        if os.path.isfile('All/'+ticker+'.csv'):
            if getFileLines(ticker)>(11+daysPrev):
                highValue=getHighValue(12+daysPrev,ticker)
                closingValue=getClosingValue(12+daysPrev,ticker)
                lowValue=getLowValue(12+daysPrev,ticker)
                highValue=highValue[daysPrev:]
                closingValue=closingValue[daysPrev:]
                lowValue=lowValue[daysPrev:]
                for n in range(10):
                    highValue[n]=highValue[n]*dowJones[n]/dowJones[n+1]
                    lowValue[n]=lowValue[n]*dowJones[n]/dowJones[n+1]
                    closingValue[n]=closingValue[n]*dowJones[n]/dowJones[n+1]
                change=[]
                for n in range(9):
                    change+=[closingValue[n]-closingValue[n+1]]
                closingValue = [closingValue[0]+numpy.mean(change)] + closingValue
                sigma=[0]*10
                for n in range(len(sigma)):
                    difference = highValue[n]-closingValue[n]
                    if difference == 0:
                        sigma[n]=0.01
                    else:
                        sigma[n]=difference
                sigma = [.005]+sigma
                m=numpy.matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
                tau=numpy.matrix([[0.],[0.],[0.]])
                for i in range(3):
                    for j in range(3):
                        for t in range(-1,10):
                            m[i,j]+=(float(t)**(i+j))/sigma[t+1]
                for i in range(3):
                    for t in range(-1,10):
                        tau[i,0]+=(closingValue[t+1]*t**i)/sigma[t+1]
                mi=linalg.inv(m)
                if linalg.det(mi) != 0:
                    coefficents=mi*tau
                else:
                    coefficents=numpy.matrix([[0.0],[0.0],[0.0]])
                dowJonesPrediction = coefficents[0,0]-coefficents[1,0]+coefficents[2,0]
                RMSEP = 0
                if not 0.0 in closingValue:
                    for i in range(10):
                        RMSEP+=(coefficents[0,0]+coefficents[1,0]*i+coefficents[2,0]*i**2-closingValue[i+1])**2/closingValue[i+1]
                    PC = (dowJonesPrediction-closingValue[1])/closingValue[1]
                    stockInfoList+=[[RMSEP,PC,ticker]]
                    PCList+=[PC]
    stockInfoList.sort()
    highRMSEP=stockInfoList[-(2*len(stockInfoList))/100][0]
    ChiSq=0.02
    PCLow=min(PCList)
    hotStockList=[[PCLow,'TEMP']]*numberOfHotStocks
    while [PCLow,'TEMP'] in hotStockList and ChiSq<highRMSEP+0.02:
        print "Finding hot stocks for Chi squared " + str(ChiSq)
        for stock in stockInfoList:
            RMSEP = stock[0]
            PC = stock[1]
            ticker = stock[2]
            if RMSEP < ChiSq and PC>hotStockList[0][0]and not [PC,ticker] in hotStockList:
                hotStockList[0]=[PC,ticker]
                hotStockList.sort()
        ChiSq+=.15*highRMSEP
    tempList=[]
    for stock in hotStockList:
        tempList+=[stock[1]]
    return tempList
        
def getHotStockPC():
    print 'Get Hot Stocks percent change'
    tickerList = getHotStockTicker()
    pricesPC = []
    for ticker in tickerList:
        if getFileLines(ticker)>12:
            prices=getClosingValue(2,ticker)
            pricesPC+=[(prices[0]-prices[1])/prices[1]]
    return sum(pricesPC)/len(pricesPC)

def getSP500PC():
    tickerList = getTickerListSP500()
    pricesPC = []
    for ticker in tickerList:
        if getFileLines(ticker)>10:
            prices=getClosingValue(2,ticker)
            pricesPC+=[(prices[0]-prices[1])/prices[1]]
    return sum(pricesPC)/len(pricesPC)

def getHotStockTicker(daysPrev=1):
    tempList=[]
    stocks = hotStocks(daysPrev)
    for stock in stocks:
        tempList+=[stock]
    return tempList



