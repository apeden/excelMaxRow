"""COLLECTION OF FUNCTIONS FOR ANALYSING RTQUIC DATA FROM EXCEL
ALEX PEDEN, DECEMBER 2018"""

from openpyxl import load_workbook
import statistics

class RTQuicSheet(object):
    def __init__(self, workbook_filepath, sheet_name):   
        self.wb = None
        self.sheet = None
        self.workbook_filepath = workbook_filepath
        self.sheet_name = sheet_name
        try:
            ##set workbook as file object
            self.wb = load_workbook(self.workbook_filepath, data_only = True)
        except IOError:
            self.wb = None
            print("Could not load: "+ self.workbook_filepath)
        try:
            self.sheet = self.wb[self.sheet_name] ##get sheet as file object
        except:
            print("Sheet not found "+ self.sheet_name + "in workbook " + self.workbook_filepath)
    def getSheet(self):
        return self.sheet
    def __str__(self):
        if self.sheet != None:
            return "Contains: "+ self.workbook_path + ", " + self.sheet_name
        else:
            return "Empty"

class RTQuICData(object):
    def __init__(self, sheet, start_row, start_col, label_col = None,
                 sec_per_cyc = 949, max_hours = 100, numRows = 96):
        self.sheet = sheet    
        self.start_row = start_row
        self.start_col = start_col
        self.max_hours = max_hours
        self.numCycles = max_hours*60*60//sec_per_cyc
        self.numRows = numRows
        self.data = [[] for i in range(self.numRows)]
        self.labels = []
        self.setData()
        ##print("sheet is "+ str(self.sheet.cell(1, 1).value))
        if label_col == None:
            for row in 'A','B','C','D','E','F','G','H':
                for column in range(1,13):
                    self.labels.append(row+str(column))
        else:
            for row in range(start_row, start_row + self.numRows):
                val = self.sheet.cell(row, label_col).value
                self.labels.append(val)
    def getLabels(self):
        return self.labels
    def setData(self):
        ##print("setting data")
        ##print("self.start_row is " + str(self.start_row))
        ##print("self.numCycles is " + str(self.numCycles))
        for row in range(self.numRows):
            ##print("row loop entered")
            for column in range(self.numCycles):
                val = self.sheet.cell(row + self.start_row, column +self.start_col).value
                ##print("value is " + str(val))
                if not type(val) == int:
                    break
                self.data[row].append(val)
        ##print("self.data is " + str(self.data))
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
            readout += " and " + str(len(self.data[i])-2) + " other values.\n"
        return readout
        
        
class DataAnalyser(object):
    def __init__(self, data, data_label, sec_per_cyc = 949):
        self.sec_per_cyc = sec_per_cyc
        self.data = data
        self.data_label = data_label
    def getSecPerCyc(self):
        return self.sec_per_cyc
    def getLabel(self):
        return self.data_label
    def getMean(self):
        return statistics.mean(self.data)
    def getStd(self):
        return statistics.stdev(self.data)
    def __str__(self):
        return self.data_label, str(self.data)
    

class RowAnalyser(DataAnalyser):
    def __init__(self, data,
                 data_label, sec_per_cyc = 949, base):
        Super().__init__(self, data, data_label, sec_per_cyc = 949)
        self.base = base
        self.threshold = 0.0
        self.row_max = 0
        self.max_index = None
        self.time_to_max = None
    def setRowMax(self):
        assert(len(self.data) > 0)
        for datum in self.data:
            assert(type(datum) == int or type(assert) == float):
        self.row_max = max(self.data)
    def calc_time(self, start, end):
        return (end-start)*self.sec_per_cyc
    def set_time_to_max(self):
        max_index = self.data.index(self.row_max)
        self.time_to_max = self.cal_time(0, max_index)
    def get_time_to_max(self):
        return self.time_to_max
    def setThreshold(self, base_index = 2, factor = 3):
        base = self.data[base_index]
        assert(type(base) == int or type(base) == float)
        self.threshold = base*factor
    def getThreshold(self):
        return self.threshold
    def setLag(self):
        self.lag = 360000
        for i in range(len(self.row_list)-2):
            if (self.data[i] > self.threshold and
                self.data[i+1] > self.threshold and
                self.data[i+2] > self.threshold):
                self.lag = self.calc_time(0,i)##in seconds
                break
        if self.lag == 360000:
            print ("no lagtime found for row ")
    def getLag(self):
        return self.lag
    def set_time_to_baseline(self):
        self.time_to_baseline = 0
        for i in range(len(self.data)):
            if self.data[i] > self.base):
                 self.time_to_baseline = self.calc_time(0, i)
                 break
    def get_time_to_baseline(self):
        return self.time_to_baseline
    def set_time_baseline_to_max(self):
        self.time_baseline_to_max = self.time_to_max
        - self.time_to_baseline
    def get_time_baseline_to_max(self):
        return self.time_baseline_to_max
    def set_gradient(self):
        print ("self.row_max is ",str(self.row_max))
        print ("self.baseline is ", str(self.base))
        print ("self.time_baseline_to_max is ", str(self.time_baseline_to_max))
        if self.time_baseline_to_max > 0:
            self.gradient = (self.row_max - self.base)/self.time_baseline_to_max
            print ("gradient is ", str(self.gradient))
    def get_gradient(self):
        return self.gradient
    def is_positive(self):
        return (self.lag > 0 and (self.lag + (2* self.sec_per_cyc)) < 360000)
    "takes a time in seconds and converts to h:m format"
    def hours(self, time_sec):
        hours = str(time_sec//3600)
        minutes = str(time_sec%3600//60)
        return hours +" hours: "+ minutes + " minutes"
