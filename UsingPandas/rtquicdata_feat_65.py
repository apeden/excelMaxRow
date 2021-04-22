import rtquicdata as rd

class RTQuICData_feat_65(rd.RTQuICData):
    def __init__(self, excelfile, start_row_col  = (1, 3),
                 numCycles = 400, SEC_PER_CYCLE = 945.6):
        super().__init__(excelfile, start_row_col  = (1, 3),
                 numCycles = 400, SEC_PER_CYCLE = 945.6)


    def base_threshold(self, i):
        #unlabeled rows are excluded from calculation of base threshold
        df_dropna = self.df.dropna(subset =["Description"])
        return df_dropna["Base"].mean() + 5*df_dropna["Base"].std()
