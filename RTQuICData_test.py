from RTQuicSheet import RTQuicSheet, RTQuICData, RowAnalyser

PATH_TO_FILES = "C:\\Users\\apeden\\OneDrive - University of Edinburgh\\excelMaxRow\\RTQuIC_for_analysis"

##SINGLE SHEET ANALYSIS
##testSheet = RTQuicSheet("RTQuIC_for_analysis/RTQUIC_READ_19_008.xlsx", "All Cycles")
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
file = "Experimental plan RTQUIC19 004 AHP 65+study cases  37 38 40 39 41 42 01 02.xlsx"
testSheet = RTQuicSheet("RTQuIC Review/"+file, "Results")
testData = RTQuICData(testSheet.getSheet(), 13, 9,  label_col = 1, numRows = 96)
data = testData.getData()
data_labels = testData.getLabels()
print("\n",12*(" "),"Max Val  Time to max  Lag times"\
      + "\n",14*(" "),"======   =========    =====")
for i in range(len(data)):
    label, datum = data_labels[i], data[i]
    a = RowAnalyser(datum, label)
    a.setRowMax()
    row_max = a.getRowMax()
    a.set_time_to_max()
    time_to_max = a.get_time_to_max()
    time_to_maxHours = a.hours(time_to_max, short = False)
    a.setThreshold()
    a.setLag()
    lag = a.getLag()
    laghours = a.hours(lag, short = False)
    a.set_time_to_threshold()
    a.set_time_threshold_to_max()
    a.set_gradient()
    gradient = a.get_gradient()
    print(label.ljust(15, ' ') + str(row_max).rjust(6, ' ') + \
          "   " + str(time_to_maxHours) + "   " + str(laghours)\
          +str(gradient))
