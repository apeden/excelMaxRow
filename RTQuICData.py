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
