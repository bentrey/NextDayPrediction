import os
import time
from dailyDataUpdate import*
from UpdateFunctions import*
from multipleGraphs import*
from singleGraph import*
from UpdateIndexJS import*
from datetime import datetime

currentPath=os.getcwd()
os.chdir(currentPath)

wait=False

while(wait):
    localTime=str(datetime.today())
    localTimeList=localTime.split(':')
    localTimeList[0]=localTimeList[0].split(' ')[1]
    localTimeList[0]=int(localTimeList[0])
    localTimeList[1]=int(localTimeList[1])

    if localTimeList[0]==7:
        if localTimeList[1]<20:
            print localTime
            time.sleep(60)
        else:
            wait=False
    else:
        print localTime
        time.sleep(1200)


updateTickerList()
updateTickerListSP500()
updateDataAll(True) 
dataUnfucker()
updateDowJones()
singleGraph()
dowJonesGraph()
multipleGraphs()
updateJS()
os.system("C:/Users/Ben/Desktop/StockProjectWeb/UpdateIndexJS.bat")
print str(datetime.today())


