"""COLLECTION OF CLASSES FOR ANALYSING RTQUIC DATA FROM EXCEL
ALEX PEDEN, DECEMBER 2018
"""

from openpyxl import load_workbook as load
import statistics as stat

class RTQuicSheet(object):
    def __init__(self, workbook_filepath, sheet_name):   
        self.wb = None
        self.sheet = None
        self.workbook_filepath = workbook_filepath
        self.sheet_name = sheet_name
        try:
            ##set workbook as file object
            self.wb = load(self.workbook_filepath,
                                    data_only = True)
        except IOError:
            self.wb = None
            print("Could not load: "+ self.workbook_filepath)
        try:
            ##get sheet as file object
            self.sheet = self.wb[self.sheet_name] 
        except:
            print("Sheet not found "
                  + self.sheet_name + "in workbook "
                  + self.workbook_filepath)
    def getSheet(self):
        return self.sheet
    def __str__(self):
        if self.sheet != None:
            return "Contains: " + self.workbook_path + ", "
            + self.sheet_name
        else:
            return "Empty"

class RTQuICData(object):
    def __init__(self, sheet, start_row, start_col, label_col = None,
                 sec_per_cyc = 945.6, max_hours = 100, numRows = 96):
        self.sheet = sheet    
        self.start_row = start_row
        self.start_col = start_col
        self.max_hours = max_hours
        self.sec_per_cyc = sec_per_cyc
        self.numCycles = int(max_hours*60*60/sec_per_cyc)
        self.numRows = numRows
        self.data = [[] for i in range(self.numRows)]
        self.labels = []
        self.setData()
        if label_col == None:
            for row in 'A','B','C','D','E','F','G','H':
                for column in range(1,13):
                    self.labels.append(row+str(column))
        else:
            for row in range(start_row, start_row + self.numRows):
                val = self.sheet.cell(row, label_col).value
                if not type(val) == str:
                    val = str(val)
                self.labels.append(val)
    def getSecPerCyc(self):
        return self.sec_per_cyc
    def getLabels(self):
        return self.labels
    def setData(self):
        for row in range(self.numRows):
            for column in range(self.numCycles):
                val = self.sheet.cell(row + self.start_row, column + \
                                      self.start_col).value
                if not type(val) == int:
                    break
                self.data[row].append(val)
    def getData(self):
        return self.data
    def setNumCycles(self, numCycles):
        self.numCycles = numCycles
    def getNumCycles(self):
        return self.numCycles
    def __str__(self):
        readout = "Data\n"
        for i in range(self.numRows):
            readout += self.labels[i] + ":"
            for j in range(2):
                readout += " " + str(self.data[i][j])
            readout += " and " + str(len(self.data[i])-2) + \
                       " other values.\n"
        return readout
        
class DataAnalyser(object):
    def __init__(self, data, data_label, sec_per_cyc = 945.6):
        self.sec_per_cyc = sec_per_cyc
        self.data = data
        self.data_label = data_label
    def getLabel(self):
        return self.data_label
    def getMean(self):
        return stat.mean(self.data)
    def getStd(self):
        return stat.stdev(self.data)
    def __str__(self):
        return self.data_label + ": " + str(self.data)
    
class RowAnalyser(DataAnalyser):
    def __init__(self, data, data_label,
                 sec_per_cyc = 945.6, maxLag = 360000):
        DataAnalyser.__init__(self, data, data_label, sec_per_cyc)
        self.threshold = 0.0
        self.row_max = 0
        self.maxLag = maxLag
        self.lag = maxLag
        self.max_index = 0
        self.time_to_max = maxLag
        self.time_to_threshold = None
        self.time_threshold_to_max = None
        self.gradient = None
    def setRowMax(self):
        assert(len(self.data) > 0)
        for datum in self.data:
            assert(type(datum) == int or type(datum) == float)
        self.row_max = max(self.data)
    def getRowMax(self):
        return self.row_max
    def calc_time(self, start, end):
        return int((end-start)*self.sec_per_cyc)
    def set_time_to_max(self):
        max_index = self.data.index(self.row_max)
        if max_index > 0:
            self.time_to_max = self.calc_time(0, max_index)
    def get_time_to_max(self):
        return self.time_to_max
    def setThreshold(self, base_index = 2, factor = 3):
        base = self.data[base_index]
        assert(type(base) == int or type(base) == float)
        self.threshold = base*factor
    def getThreshold(self):
        return self.threshold
    def setLag(self, toPrnt = False):
        for i in range(len(self.data)-2):
            if (self.data[i] > self.threshold and
                self.data[i+1] > self.threshold and
                self.data[i+2] > self.threshold):
                self.lag = self.calc_time(0,i)##in seconds
                break
        if (toPrnt == True) and (self.lag == self.maxLag):
            print ("no lagtime found for row ")
    def getLag(self):
        return self.lag
    def set_time_to_threshold(self):
        for i in range(len(self.data)):
            if self.data[i] > self.threshold:
                 self.time_to_threshold = self.calc_time(0, i)
                 break
    def get_time_to_threshold(self):
        return self.time_to_threshold
    def set_time_threshold_to_max(self, toPrnt = False): 
        try:
            self.time_threshold_to_max = self.time_to_max \
                                         - self.time_to_threshold
        except:
            if toPrnt: print("Could not set Threshold to max")
    def set_gradient(self, toPrnt = False):
        if toPrnt:
            print ("self.row_max is ",str(self.row_max), \
                    "\nself.threshold is ", str(self.threshold), \
                    "\nself.time_threshold_to_max is ", \
                    str(self.time_threshold_to_max))
        try:
            if self.time_threshold_to_max > 0:
                self.gradient = (self.row_max - self.threshold)\
                            /self.time_threshold_to_max
            if toPrnt:
                print ("gradient is ", str(self.gradient))
        except:
            if toPrnt: print("could not set gradient")
    def get_gradient(self):
        return self.gradient
    def setAUC(self, base_index = 2):
        total, self.AUC = 0, 0  
        for datum in self.data:
            if datum - self.data[base_index] > 0:
                total += datum
        self.AUC = total/400
    def getAUC(self):
        return self.AUC
    def is_positive(self):
        if self.lag > 0 and (self.lag
                            + (2* self.sec_per_cyc)) < self.maxLag:
            return True
        return False
    """"Takes a time in seconds and converts to h:m format."""
    def hours(self, time_sec, short = True):
        hours = str(time_sec//3600)
        minutes = str(time_sec%3600//60)
        if short:
            return hours.rjust(3, ' ') +":"+ minutes.rjust(2, '0')
        return hours.rjust(3, ' ') +"h: "+ minutes.rjust(2, '0') + "m"
