from RTQuicSheet import RTQuicSheet
from RTQuICData import RTQuICData
from RowAnalyser import RowAnalyser
#from DataAnalyser import DataAnalyser


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
testData = RTQuICData(testSheet.getSheet(), 13, 4, 3, numRows = 50)
print(testData)

##FOR EACH ROW IN DATA, PRINT LABEL, LAG, MAXVAL AND TIME TO MAX

class DataExpresser(object):
    def __init__(self, file, sheet, startRow, startCol, label_col = None):
        self.file = file
        self.sheet = sheet
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
        testSheet = RTQuicSheet(self.file,self.sheet)
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
                 "Area under curve":AUC,
                 "Positive?":a.is_positive(),
                 "Data":datum}
                
                 )
            print(str(i).ljust(4, ' ')\
                  + label.ljust(15, ' ')\
                  + str(row_max).ljust(10, ' ')\
                  + str(time_to_maxHours).ljust(15, ' ')\
                  + str(laghours).ljust(15, ' ')\
                  + str(gradient).ljust(10, ' ')\
                  + str(round(AUC)).ljust(20, ' ')
                  + str(a.is_positive()).ljust(20, ' '))
    def setRepPos(self):
        for i in range(0,len(self.features),2):
            if self.features[i]["Positive?"] \
               and self.features[i+1]["Positive?"]:
                self.features[i]["RepPositive?"] = True
                self.features[i+1]["RepPositive?"] = True
            else:
                self.features[i]["RepPositive?"] = False
                self.features[i+1]["RepPositive?"] = False
    def getFeatures(self):
        return self.features
    def reportRepPos(self):
        print("The following wells were repeat positive")
        for featDict in self.features:
            if featDict["RepPositive?"]:
                print(featDict["Label"]
                      +": lag time: "
                      +str(featDict["Lag"])
                      +": max val: "
                      +str(featDict["RowMax"]))
                      



