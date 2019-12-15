from UpdateFunctions import*

print 'Updating Stock Symbols'
UpdateTickerList()
tickerList=getTickerList()
progress = 0
total = len(tickerList)
print 'Symbols Updated'
print'Updating Stock Data'
for x in tickerList:
    print str(tickerList.index(x)+1) + '/' + str(len(tickerList))
    pullHistoricalData(x,20)
print 'Stock Data Updated'
print 'Updating Dow Jones'
updateDowJones()
print 'Dow Jones Updated'
