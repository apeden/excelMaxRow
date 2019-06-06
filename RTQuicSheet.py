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
            print("Could not open file"+ self.workbook_filepath)
        try:
            self.sheet = self.wb[self.sheet_name] ##get sheet as file object
        except:
            print("Could not find sheet "+ self.sheet_name + "in source data file for " + self.workbook_filepath)
    def getSheet(self):
        return self.sheet
    def __str__(self):
        if self.sheet != None:
            return self.sheet_name
        else:
            return "No sheet object available"

class RTQuICData(object):
    def __init__(self, sheet, start_row, start_col, label_col = None,
                 sec_per_cyc = 949, max_hours = 100, numRows = 8):
        self.sheet = sheet    
        self.start_row = start_row
        self.start_col = start_col
        self.max_hours = max_hours
        self.numCycles = max_hours*60*60//sec_per_cyc
        self.numRows = 8
        self.data = [[] for i in range(self.numRows)]
        self.labels = []
        self.setData()
        ##print("sheet is "+ str(self.sheet.cell(1, 1).value))
        if label_col == None:
            for row in 'A','B','C','D','E','F','G','H':
                for column in range(1,13):
                    self.labels.append(row+str(column))
        else:
            for row in range(start_row, (self.numRows*12) + 1):
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
        readout = "Data "
        for i in range(self.numRows):
            readout += self.labels[i] + ":"
            for j in range(2):
                readout += " " + str(self.data[i][j])
            readout += " and " + str(len(self.data[i])-2) + " other values.\n"
        return readout
        
class SheetBase(object):
    def __init__(self, sheet):
        self.sheet = sheet
        self.baseMean = 0.0
        self.baseSTDEV = 0.0
        self.baseline = 0.0
        self.column_list = []
    """
    reads a selected column from a sheet file object and returns a list of what's in it.
    column_start refers the row number where you want to start reading downwards from
    breaks when an empty cell is encountered
    """
    def set_column_list(self, column, row_start):
        print("column number sent to set_column_list "+str(column))
        val = 0
        row = row_start
        while True:
            val = self.get_cell_val(row, column)
            if not type(val) == int:
                break
            self.column_list = self.column_list + [val]
            row += 1
        print(self.column_list[0:20])
    def get_cell_val(self, row, column):
        try:
            val = self.sheet.cell(row, column).value
        except:
            print("A problem occurred reading data from a row")
        return val
    def get_column_list(self):
        return self.column_list
    def setBaseMean(self):
        self.baseMean = statistics.mean(self.column_list)
    def getBaseMean(self):
        return self.baseMean
    def setBaseSTDEV(self):
        self.baseSTDEV = statistics.stdev(self.column_list)
    def getBaseSTDEV(self):
        return self.baseSTDEV
    def setBaseline(self):
        self.baseline = self.baseMean + 3* self.baseSTDEV
    def getBaseline(self):
        return self.baseline
    def __str__(self):
        return "Analysis of sheet " +str(self.sheet)

        
class RowAnalyser(SheetBase):
    def __init__(self, sheet):
        SheetBase().__init__(self, sheet)
        self.SECONDS_PER_CYCLE = 949
        self.row_label = ""
        self.row_list = []
        self.column_list = []
        self.row_max = None ##will be flourescence units
        self.time_to_max = None ##will be in seconds
        self.threshold = None ##will be flourescence units
        self.lag = None ##will be in seconds
        self.time_to_baseline = None ##will be in seconds
        self.time_baseline_to_max = None ##will be in seconds
        self.gradient = 0.0 ## fluoresecent units/sec
    def getSECONDS_PER_CYCLE(self):
        return self.SECONDS_PER_CYCLE
    def set_row_label(self, row):
        try:
            val = self.sheet.cell(row, column=1).value
        except:
            print("A problem occurred setting the row label.")
        self.row_label = val
    def get_row_label(self):
        return self.row_label
    """
    reads a selected row (up to 1000 cells) from a sheet file object and returns a list of what's in it.
    column_start refers the column number i.e. A = 1, B = 2 etc where you want to start
    reading the row (left to right).
    breaks when an empty cell is encountered
    """
    def set_row_list(self, column_start, row):
        print("row number sent to set_row_list "+str(row))
        self.row_list = []
        for column in range(column_start, 1000):
            val = self.get_cell_val(row, column)
            if val == None:
                break
            self.row_list = self.row_list + [val]
        print(self.row_list[0:20])
    def get_row_list(self):
        return self.row_list
    """
    reads from a row as a list of ints and/or floats and obtains maximum value
    and time (in hours) when max value occurred
    """
    def set_row_max(self):
        print("Called self row max.")
        print("Before call it's: " +str(self.row_max))
        try:
            assert(len(self.row_list) > 0)
        except:
            print("Row list is empty. Cannot analyse row")
            self.row_max = None
        for elem in self.row_list:
            if(type(elem) == int or type(elem) == float):
                self.row_max = max(self.row_list)
            else:
                print("item in row list is not a number")
                self.row_max = None
        print("Now it's " +str(self.row_max))
    def get_row_max(self):
        return self.row_max
    def calculate_time_sec(self, start, end):
        return (end-start)*self.SECONDS_PER_CYCLE
    def set_time_to_max(self):
        self.time_to_max = self.calculate_time_sec(0, self.row_list.index(self.row_max))
    def get_time_to_max(self):
        return self.time_to_max
    def setThreshold(self):
        assert(type(self.row_list[2]) == int or type(self.row_list[2]) == float)
        self.threshold = self.row_list[2]*3
    def getThreshold(self):
        return self.threshold
    def setLag(self):
        self.lag = 360000
        for i in range(len(self.row_list)-2):
            if (self.row_list[i] > self.threshold and
                self.row_list[i+1] > self.threshold and
                self.row_list[i+2] > self.threshold):
                self.lag = self.calculate_time_sec(0,i)##in seconds
                break
        if self.lag == 360000:
            print ("no lagtime found for row ")
    def getLag(self):
        return self.lag
    def set_time_to_baseline(self):
        self.time_to_baseline = 0
        for i in range(len(self.row_list)):
            if self.row_list[i] > int(self.baseline):
                 self.time_to_baseline = self.calculate_time_sec(0, i)
                 break
    def get_time_to_baseline(self):
        return self.time_to_baseline
    def set_time_baseline_to_max(self):
        self.time_baseline_to_max = self.time_to_max - self.time_to_baseline
    def get_time_baseline_to_max(self):
        return self.time_baseline_to_max
    def set_gradient(self):
        print ("self.row_max is ",str(self.row_max))
        print ("self.baseline is ", str(self.baseline))
        print ("self.time_baseline_to_max is ", str(self.time_baseline_to_max))
        if self.time_baseline_to_max > 0:
            self.gradient = (self.row_max - self.baseline)/self.time_baseline_to_max
            print ("gradient is ", str(self.gradient))
    def get_gradient(self):
        return self.gradient
    def is_positive(self):
        return (self.lag > 0 and (self.lag + (2* self.SECONDS_PER_CYCLE)) < 360000)
    "takes a time in seconds and converts to h:m format"
    def hours(self, time_sec):
        hours = str(time_sec//3600)
        minutes = str(time_sec%3600//60)
        return hours +" hours: "+ minutes + " minutes"
