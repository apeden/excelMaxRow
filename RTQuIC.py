##Get one or more excel files containing rtquic data
##extract data for one or more files 
##extract     ...all data from ONE file  = RTQuICData
class ExtractData(object):
    def __init__(self, file_name, start_row, start_col, label_column =False): 
        pass
    def setData(): ##gets all data using openpyxl
        pass
    def getData(): ##
    """flourescence readings for one or more data rows,
    as a list, or list or lists, as appropriate
    """
    def getLabels():
        pass
    def __str__(self):
        pass ###return self.FileName and data as previously coded for
                                    
class AnalyseData(object): ##performed on a row
    def __init__(self, data):
        pass                       
    def getMean(self, range = (0, len(self.data)):
        pass

class AnalyseRow(AnalyseData):
    def __init__(self, data, base):
        AnalyseData.__init__(self, data)            
    def getMaxVal(self):
        pass
    def getLagTime(self, factor = 3, SD = False, units = secs):
        pass
    def getTimeToMax(self, factor = 3, SD = False, units = secs):
        pass
    def getGradient(self, scale = 1):
        pass
    def getAUC(self):
        pass

