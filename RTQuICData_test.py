from RTQuicSheet import RTQuicSheet, RTQuICData, RowAnalyser


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

file = "RTQuIC Review/Experimental plan RTQUIC19 004 AHP 65+study cases  37 38 40 39 41 42 01 02.xlsx"




class DataExpresser(object):
    def __init__(self, file, startRow, startCol, label_col = None):
        self.file = file
        self.startRow = startRow
        self.startCol = startCol
        self.label_col = label_col
        self.features = []
    def setFeatures(self, toPrnt = True):
        """Perform line by line analysis of data.
        Calculate features and create dict of features for each line
        Add dict to a list of dicts (self.features)
        Optional: print to screen.

        Return nothing
        """
        testSheet = RTQuicSheet(self.file,"Results")
        testData = RTQuICData(testSheet.getSheet(),
                              self.startRow,
                              self.startCol,
                              self.label_col,
                              numRows = 96)
        data = testData.getData()
        data_labels = testData.getLabels()
        
        if toPrnt:
            print("Row".ljust(3, ' '),
                  "Label".ljust(14, ' '),
                  "RowMax".ljust(9, ' '),
                  "Time to Max".ljust(14, ' '),
                  "Lag".ljust(14, ' '),
                  "Gradient".ljust(9, ' '),
                  "Area under curve".ljust(19, ' '))
        for i in range(len(data)):
            label, datum = data_labels[i], data[i]
            a = RowAnalyser(datum, label)
            a.setRowMax()
            row_max = a.getRowMax()
            a.set_time_to_max()
            time_to_maxHours = a.hours(a.get_time_to_max(), short = False)
            a.setThreshold()
            a.setLag()
            laghours = a.hours(a.getLag(), short = False)
            a.set_time_to_threshold()
            a.set_time_threshold_to_max()
            a.set_gradient()
            gradient = a.get_gradient()
            a.setAUC()
            AUC = a.getAUC()
            gradient = a.get_gradient()
            if not gradient == None:
                gradient = round(gradient, 4)
            self.features.append(
                {"Label":data_labels[i],
                 "RowMax":row_max,
                 "Time to Max":a.get_time_to_max(),
                 "Lag":a.getLag(),
                 "Gradient":gradient,
                 "Area under curve":AUC})
            if toPrnt:
                print(str(i).ljust(4, ' ')\
                      + label.ljust(15, ' ')\
                      + str(row_max).ljust(10, ' ')\
                      + str(time_to_maxHours).ljust(15, ' ')\
                      + str(laghours).ljust(15, ' ')\
                      + str(gradient).ljust(10, ' ')\
                      + str(round(AUC)).ljust(20, ' '))
    def getFeatures(self):
        return self.features

d =  DataExpresser(file, 13, 9, 1)


d.setFeatures()
print(d.getFeatures())
