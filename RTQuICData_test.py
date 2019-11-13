from RTQuicSheet import RTQuicSheet
from RTQuICData import RTQuICData
from DataExpresser import DataExpresser
#from tracePlotter import TracePlotter 

##SINGLE SHEET ANALYSIS
#testSheet = RTQuicSheet("RTQuIC_for_analysis/RTQUIC_READ_19_008.xlsx", "All Cycles")
##testData = RTQuICData(testSheet.getSheet(), 13, 4)
##print(testData)

##SINGLE SHEET ANALYSIS USING A COLUMN IN THE EXCEL FILE FOR LABELS
##testData = RTQuICData(testSheet.getSheet(), 13, 4, 3)
##print(testData)

##SINGLE SHEET ANALYSIS -REDUCED MAX HOURS
##testData = RTQuICData(testSheet.getSheet(), 13, 4, 3, max_hours = 50)
##print(testData)

##SINGLE SHEET ANALYSIS -REDUCED NUM ROWS
#testData = RTQuICData(testSheet.getSheet(), 13, 4, 3, numRows = 50)
#print(testData)

##FOR EACH ROW IN DATA, PRINT LABEL, LAG, MAXVAL AND TIME TO MAX
                      
file = "RTQuIC_for_analysis/RT-QUIC READ 19 013.xlsx"
sheet = "All Cycles"

#testSheet = RTQuicSheet("RTQuIC_for_analysis/RTQUIC_READ_19_008.xlsx", "All Cycles")
#testData = RTQuICData(testSheet.getSheet(), 13, 4)
d = DataExpresser(file, sheet, 13, 4)
d.setFeatures()
d.setRepPos()
d.reportRepPos()
dataDicts = d.getFeatures()
#xVals = testData.getReadTimes()
#TracePlotter.plot(xVals, dataDicts, ("B7","B8","C1","C2"))
