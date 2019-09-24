from DataAnalyser import DataAnalyser

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
        self.isRepPos = None
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
            aboveBase = datum - self.data[base_index]
            if aboveBase > 0:
                total += aboveBase
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
    def isRepPos(self):
        return True
