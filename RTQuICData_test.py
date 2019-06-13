from RTQuicSheet import RTQuicSheet, RTQuICData, RowAnalyser

PATH_TO_FILES = "C:\\Users\\apeden\\OneDrive - University of Edinburgh\\excelMaxRow\\RTQuIC_for_analysis"

##SINGLE SHEET ANALYSIS
testSheet = RTQuicSheet("RTQuIC_for_analysis/RTQUIC_READ_19_008.xlsx", "All Cycles")
##testData = RTQuICData(testSheet.getSheet(), 13, 4)
##print(testData)

##SINGLE SHEET ANALYSIS USING A COLUMN IN THE EXCEL FILE FOR LABELS
##testData = RTQuICData(testSheet.getSheet(), 13, 4, 3)
##print(testData)

##SINGLE SHEET ANALYSIS -REDUCED MAX HOURS
##testData = RTQuICData(testSheet.getSheet(), 13, 4, 3, max_hours = 50)
##print(testData)

##SINGLE SHEET ANALYSIS -REDUCED NUM ROWS
##testData = RTQuICData(testSheet.getSheet(), 13, 4, 3, numRows = 50)
##print(testData)

##FOR EACH ROW IN DATA, PRINT LABEL, LAG, MAXVAL AND TIME TO MAX
testData = RTQuICData(testSheet.getSheet(), 13, 4, 3, numRows = 96)
data = testData.getData()
data_labels = testData.getLabels()
print("\nTime to Max, Max Val and Lag times\n====================")
for i in range(len(data)):
    label, datum = data_labels[i], data[i]
    a = RowAnalyser(datum, label)
    ##set max val
    a.setRowMax()
    row_max = a.getRowMax()
    ##set time to max
    a.set_time_to_max()
    time_to_max = a.get_time_to_max()
    time_to_maxHours = a.hours(time_to_max)
    ##set lag time
    a.setThreshold()
    a.setLag()
    lag = a.getLag()
    laghours = a.hours(lag)
    print(label.ljust(15, ' ') + str(row_max).rjust(6, ' ') + \
          "   " + str(time_to_maxHours) + "   " + str(laghours))
