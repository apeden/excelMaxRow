####COLLECTION OF FUNCTIONS FOR ANALYSING RTQUIC DATA FROM EXCEL####
####ALEX PEDEN, DECEMBER 2018#####

from openpyxl import load_workbook


class RTQuicSheet(object):
    

    SECONDS_PER_CYCLE = 949
    def __init__(self, excel_workbook_name, sheet_name):
        #clear previous workbook
        self.wb = None
        self.excel_workbook_name = excel_workbook_name
        self.sheet_name = sheet_name
        ##set workbook as file object
        try:
            self.wb = load_workbook(self.excel_workbook_name, data_only = True)
        except IOError:
            self.wb = None
            print("Could not open file"+ self.excel_workbook_name)
        ##get sheet as file object
    
        self.sheet = self.wb[self.sheet_name]
        self.row_label = ""
        self.row_list = []
        self.row_max = None
        self.time_to_max = None ##eventually will be in seconds
        self.threshold = None 
        self.lag = None ##eventually will be in seconds


    """gets a work book object"""
    def get_wb(self):
        
        return wb
    
    def set_row_label(self, row):
        try:
            val = self.sheet.cell(row, column=1).value
        except AttributeError:   
            print("A problem occurred setting the row label.")
        self.row_label = val

    def get_row_label(self):
        return self.row_label


    """
    reads a selected row from a sheet file object and returns a list of what's in it.
    row_start refers the column number i.e. A = 1, B = 2 etc where you want to start
    reading the row (left to right).
    """
    def set_row_list(self, row_start, row):
        print("row number sent to set_row_list "+str(row))
        self.row_list = []
        for i in range(row_start, 1000):        
            try:
                val = self.sheet.cell(row, column=i).value
            except AttributeError:   
                print("A problem occurred reading data from a row")
                
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

    def set_time_to_max(self):
        ## in seconds
        self.set_row_max()
        self.time_to_max = self.row_list.index(self.row_max)*(RTQuicSheet.SECONDS_PER_CYCLE) 

    def get_time_to_max(self):
        return self.time_to_max

    """
    reads from a row as a list of ints and/or doubles and obtains first of
    three consecutive values that are three times above the baseline along with
    the time to reach this value, or else returns  "no values found"
    """
    def setThreshold(self):
        assert(type(self.row_list[2]) == int or type(self.row_list[2]) == float)
        self.threshold = self.row_list[2]*3

    def setLag(self):
        self.setThreshold()
        self.lag = 0
        for i in range(len(self.row_list)-2):
            if (self.row_list[i] > self.threshold and
                self.row_list[i+1] > self.threshold and
                self.row_list[i+2] > self.threshold):
                self.lag = i*(RTQuicSheet.SECONDS_PER_CYCLE)##in seconds
                return           
        print ("no lagtime found for row ")
        
    def getLag(self):
            return  self.lag ##in seconds

    "takes a time in seconds and converts to h:m format"
    def hours(self, time_sec):
        hours = str(time_sec//3600) 
        minutes = str(time_sec%3600//60)
        return hours +" hours: "+ minutes + " minutes"


    def __str__(self):
        return "Workbook: "+ self.excel_workbook_name + " Sheet: " + self.sheet_name
        








