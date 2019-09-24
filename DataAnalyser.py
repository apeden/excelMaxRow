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
