import rtquicdata as rd

class RTQuICData_feat(rd.RTQuICData):   
    def __init__(self, excelfile, start_row_col  = (1, 3),
                 numCycles = 400, SEC_PER_CYCLE = 945.6):
        super().__init__(excelfile)
        print("RTQuICData_feat obj instatiated with" , excelfile)
        self.start_row, self.start_col = start_row_col
        self.numCycles = numCycles
        self.SEC_PER_CYCLE = 945.6
        self.da = None
        self.method_dict = {"Base":self.base,
                            "Base threshold":self.base_threshold,
                            "Max Val": self.maxVal,
                            "Time to Max": self.timeToMax,
                            "Time to 75% max": self.timeTo75Max,
                            "Lag Time": self.lagTime,
                            "Lag Val": self.lagVal,
                            "Gradient": self.gradient,
                            "AUC": self.areaUnderCurve,
                            "Time to base": self.time_to_base}
        self.setArray()
        self.get_features_df()

    def setArray(self):
        ##try:
        self.da = self.df.iloc[self.start_row:, self.start_col:(self.start_col + self.numCycles + 1)].to_numpy()
        ##except:
            ##print("Could not extract numeric data as array")
           ## self.da = None
            
    def getArray(self):
        return self.da

    def threshold_cycle(self, i, v):
        """helper function for finding first cycle where three successive
        cycles give flourescence values greater than a given value v
        """
        for c in range(len(self.da[i])-2):        
            if (self.da[i][c] > v
                and self.da[i][c+1] > v
                and self.da[i][c+2] > v):
                return c

    """Below are methods for calculating features"""
    def maxVal(self, i):
        try:
            return np.amax(self.da[i])
        except:
            return np.NaN
        
    def _75maxVal(self, i):
        """for calculating value that is 75% max"""
        return 0.75*self.maxVal(i)

    def base(self, i):
        return self.da[i][2]

    def base_threshold(self, i):
        return self.df["Base"].mean() + 5*self.df["Base"].std()

    def time_to_base(self, i):
        base_cyc = self.threshold_cycle(i, self.base_threshold(i))
        try:
            base_start = base_cyc*self.SEC_PER_CYCLE
            base_start /= 3600
            return base_start
        except:
            return np.NaN

    def timeToMax(self, i):
        """in hours"""
        time_to_max = np.argmax(self.da[i])*self.SEC_PER_CYCLE
        if not self.time_to_base(i) == np.NaN:
            return round(time_to_max/3600, 1)
        else:
            return np.NaN
        
    def timeTo75Max(self, i):
        """in hours"""
        _75max = self._75maxVal(i)
        time_to_0_75_max = np.argmax(self.da[i] > _75max)*self.SEC_PER_CYCLE
        if not self.time_to_base(i) == np.NaN:
            return round(time_to_0_75_max/3600, 1)
        else:
            return np.NaN

    def lagTime(self, i):
        v = 3* self.da[i][1]
        try:
            lagtime_sec = self.threshold_cycle(i, v)*self.SEC_PER_CYCLE
            return round(lagtime_sec/3600, 1)
        except:
            lagtime_sec = self.numCycles*self.SEC_PER_CYCLE
            return round(lagtime_sec/3600, 1)

            
    def lagVal(self, i):
        v = 3* self.da[i][1]
        c = self.threshold_cycle(i, v)
        if c != None:
            return self.da[i][c]
        else:
            return np.NaN
            
    def areaUnderCurve(self, i):   
        val_above_baseline = self.da[i] - self.base(i)
        
        area = val_above_baseline.sum()
        if area > 0:
            return area
        else:
            return 0.0

    def gradient(self, i):
        """calculated as increase in fluorescence units
        per unit time (in hours)
        between the baseline and the 75% max val
        """
        min_ = self.base_threshold(i)
        max_ = self._75maxVal(i)
        gradient_start_cyc = self.threshold_cycle(i, min_)
        gradient_end_val = max_
        gradient_end_cyc = self.threshold_cycle(i, max_)
        #print("gradient start flouresence" ,gradient_start_val)
        #print("gradient start cycle"       ,gradient_start_cyc)
        #print("gradient end flouresence"   ,gradient_end_val)
        #print("gradient end cycle"   ,gradient_end_cyc)
        try:
            gradient = (max_ - min_)/(gradient_end_cyc - gradient_start_cyc)
        except:
            return np.NaN
        gradient /= self.SEC_PER_CYCLE
        gradient *= 3600
        return round(gradient, 1)   
       
    def addColumn(self, method_name):
        self.df[method_name] = np.NaN
        col_index = self.df.columns.get_loc(method_name)
        for i in range(0, self.da.shape[0]):
            value = self.method_dict[method_name](i)
            self.df.iat[i, col_index] = value


    def get_features_df(self):
        """for excel file of rtquic data,
        Returns a full dataframe of features
        """

        for method_name in self.method_dict:
            self.addColumn(method_name)
        
