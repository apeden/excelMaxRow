import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math

toPrint = False
##for setting NaN lag times to 100
default_lag = True
basepath = "RTQuIC_for_analysis/"
SEC_PER_CYCLE = 945.6
num_cycles = 400
files = []

plt.subplots_adjust(wspace = 0.4)
plt.subplots_adjust(hspace = 0.6)


"""data and variables below relevant to 65+ study"""
##for relabelling duplicate samples
clean_labels = True


POSITIVES =(
"38/07",
"39/09",
"41/08",
"44/10",
"48/06",
"43/10",
"48/11",
"54/05",
"56/12",
"57/12",
"65/13",
"66/13",
"67/13")

M_POS_CONTROLS = "MM1", "15.689", 

V_POS_CONTROLS = "VV2", "15.692"

NEGATIVES = "MM","MV","VV" "15.32", "15.323", "15.317"

pos_control_colour = {"MM1":"r",
                   "15.689":"r",
                   "VV2":"b",
                   "15.692":"b"}

type_colour = {"Blinded positive":"r",
               "MM1 Positive control":"b",
               "VV2 Positive control":"m",
               "Negative control":"g",
               "test sample":"y"}



"""data below relevant to the analysis of substrates"""

substrates = {
#"HS23NM 140211 unseeded":"g",
##"HS23NM 140211 MM1 seeded":"b",
##"431 HuM129F9STOP ID50161 unseeded":"g",
##"431 HuM129F9STOP ID50161 MM1 seeded":"b",
#"432 HuV129F6STOP ID50162 unseeded":"g",
##"432 HuV129F6STOP ID50162 MM1 seeded":"b",
##"432 HuV129F11STOP ID204751 unseeded":"g",
##"432 HuV129F11STOP ID204751 MM1 seeded":"b",
##"200409 HS23NV A unseeded":"g",
"200409 HS23NV A MM1 seeded":"b",
##'Ha Fl PrP "M" unseeded':"g",
##'Ha Fl PrP "M" MM1 seeded':"b",
}

substrates2 = {
##"hs90H(m) 240111 unseeded":"g",
##"hs90H(m) 240111 MM1 seeded":"b",
##"hs90H(v) 250111 unseeded":"g",
##"hs90H(v) 250111 MM1 seeded":"b",
##"hs90H(M) 260111 unseeded":"g",
##"hs90H(M) 260111 MM1 seeded":"b",
##"hs90n(V) 10211 unseeded":"g",
##"hs90n(V) 10211 MM1 seeded":"b",
##"Bank vole 501059 F25a unseeded":"g",
##"Bank vole 501059 F25a MM1 seeded":"b",
##"Bank vole 501059 F25b unseeded":"g",
##"Bank vole 501059 F25b MM1 seeded":"b",
##"432 HuV129F11bSTOP ID204751 17/11/15 unseeded":"g",
"432 HuV129F11bSTOP ID204751 17/11/15 MM1 seeded":"b",
##"431 HuM129F13STOP ID204320 10/06/15 unseeded":"g",
##"431 HuM129F13STOP ID204320 10/06/15 MM1 seeded":"b"
}


subconcs = {
"HS23NM 140211 unseeded":(0.52,"M"),
"431 HuM129F9STOP ID50161 unseeded":(0.272,"M"),
"432 HuV129F6STOP ID50162 unseeded":(0.253,"V"),
"432 HuV129F11STOP ID204751 unseeded":(0.252,"V"),
"200409 HS23NV A":(0.226,"V"),
"hs90H(m) 240111 unseeded":(0.416,"M"),
"hs90H(v) 250111 unseeded":(0.173,"V"),
"hs90H(M) 260111 unseeded":(0.615,"M"),
"hs90n(V) 10211 unseeded":(0.409,"V"),
"432 HuV129F11bSTOP ID204751 17/11/15 unseeded":(0.238,"V"),
"431 HuM129F13STOP ID204320 10/06/15 unseeded":(0.186,"M")
}


codon_colour = {"M":"r",
               "V":"b",
               }


with os.scandir(basepath) as entries:
    for entry in entries:
        try:
            assert(entry.is_file())
            files.append(entry.name)
        except:
            print(entry.name, " is apparently a problem file.")
    for file in files:
        print(file)

class RTQuICData(object):
    basepath = "RTQuIC_for_analysis/"
    sheet_name = "All Cycles"
    skiprows = 10,
    usecols='A,N:OW'
    
    def __init__(self, excelfile):
        self.file = excelfile
        self.file_name = excelfile.__str__()
        self.df = None
        self.setData()
        
    def get_df(self):
        return self.df
    def setData(self):
        """If possible, return raw dataframe using excel file sheet as input"""
        try:
            self.df = pd.read_excel(RTQuICData.basepath + self.file,
                               RTQuICData.sheet_name,
                               RTQuICData.skiprows)
        except FileNotFoundError:
            print("In getData, File ",self.file," not found")
            self.df = None
        except ValueError:
            print("Check sheet name")
            self.df = None
        except:
            print("In getData, Couldn't make dataframe using file ",file)
            self.df = None
    def getData(self):
        return self.df
    def __str__(self):
        string  = "\n=============\n"   
        string += self.file_name +"\n=============\n"+ self.df.__str__()
        return string



class RTQuICData_feat(RTQuICData):
    def __init__(self, excelfile, start_row_col  = (1, 3),
                 numCycles = 400, SEC_PER_CYCLE = 945.6):
        super().__init__(excelfile)
        self.start_row, self.start_col = start_row_col
        self.numCyles = numCycles
        self.SEC_PER_CYCLE = 945.6
        self.da = None
        self.setArray()

    def setArray(self):
        try:
            self.da = self.df.iloc[self.start_row:,
                                self.start_col:self.start_col +\
                                num_cycles+ 1 ]
        except:
            print("Could not extract numeric data as array")
            self.da = None
            
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
            base_start = base_cyc*SEC_PER_CYCLE
            base_start /= 3600
            return base_start
        except:
            return np.NaN

    def timeToMax(self, i):
        """in hours"""
        time_to_max = np.argmax(self.da[i])*SEC_PER_CYCLE
        if not self.time_to_base(i) == np.NaN:
            return round(time_to_max/3600, 1)
        else:
            return np.NaN
        
    def timeTo75Max(self, i):
        """in hours"""
        _75max = self._75maxVal(i)
        time_to_0_75_max = np.argmax(self.da[i] > _75max)*SEC_PER_CYCLE
        if not self.time_to_base(i) == np.NaN:
            return round(time_to_0_75_max/3600, 1)
        else:
            return np.NaN

    def lagTime(self, i):
        v = 3* self.da[i][1]
        try:
            lagtime_sec = self.threshold_cycle(i, v)*SEC_PER_CYCLE
            return round(lagtime_sec/3600, 1)
        except:
            if default_lag:
                lagtime_sec = num_cycles*SEC_PER_CYCLE
                return round(lagtime_sec/3600, 1)
            else:
                return np.NaN
            
    def lagVal(self, i):
        v = 3* self.da[1]
        c = self.threshold_cycle(v)
        if c != None:
            return self.da[c]
        else:
            return np.NaN
            
    def areaUnderCurve(self, i):
        val_above_baseline = self.da - self.base_threshold(i)
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
        gradient_start_cyc = self.threshold_cycle(min_)
        gradient_end_val = max_
        gradient_end_cyc = self.threshold_cycle(max_)
        #print("gradient start flouresence" ,gradient_start_val)
        #print("gradient start cycle"       ,gradient_start_cyc)
        #print("gradient end flouresence"   ,gradient_end_val)
        #print("gradient end cycle"   ,gradient_end_cyc)
        try:
            gradient = (max_ - min_)/(gradient_end_cyc - gradient_start_cyc)
        except:
            return np.NaN
        gradient /= SEC_PER_CYCLE
        gradient *= 3600
        return round(gradient, 1)   
       
    method_dict = {"Base":base,
                   "Base threshold":base_threshold,
                   "Max Val": maxVal,
                   "Time to Max": timeToMax,
                   "Time to 75% max": timeTo75Max,
                   "Lag Time": lagTime,
                   "Lag Val": lagVal,
                   "Gradient": gradient,
                   "AUC": areaUnderCurve,
                   "Time to base": time_to_base}

    def addColumn(self, method_name):
        self.df[method_name] = np.NaN
        col_index = self.df.columns.get_loc(method_name)
        for i in range(0, self.df.shape[0]):
            self.getArray(i)
            value = RTQuICData.method_dict[method_name](self, i)
            self.df.iat[i, col_index] = value

    def addFileTag(self, file):
        self.df["file name"] = file
        
    def cleanDesc(self):
        """ modify df to create correct unique descriptions
        of the duplicate rows (assuming duplicates are used)
        """    
        for i in range(0, len(self.df)-1, 2):
            ##try:
            ##if not pd.isnull(self.df.iat[i+1,0]):
            self.df.iat[i,0] = str(self.df.iat[i,0]) + " " + str(self.df.iat[i+1,0])
            self.df.iat[i+1,0] = str(self.df.iat[i,0]) + " repeat"
            ##except:
              ##  print("Problem cleaning labels at index ",i)

    def get_features_df(self,file):
        """for excel file of rtquic data,
        Returns a full dataframe of features
        and an associated (and comparably indexed) numpy file of the raw data
        """
        self.getData(file)
        try:
            self.df.columns = self.df.iloc[0]
        except:
            print("Couldn't set columns for ",file)
        self.df.drop(self.df.index[0], inplace = True)    
        self.df = self.df[self.df.Description != 0]
        if toPrint: print("Basic dataframe for ",file,"\n",self.df)
        for method_name in RTQuICData.method_dict:
            self.addColumn(method_name)
        try:
            self.addFileTag(file)
        except:
            print("problem tagging filename ", file) 
        if clean_labels:
            ##try:
            self.cleanDesc()
            if toPrint: print(self.df)
            ##except:
                ##print("Problem cleaning row names for ",file,"\n")
        self.df = self.df.dropna(subset =["Description"])
        if clean_labels:
            self.df = self.df.loc[self.df['Description'] != "nan nan repeat"]
            self.df = self.df.loc[self.df['Description'] != "nan nan"]
        if toPrint:
            print("Shape of dataframe", self.df.shape, "\n")
        self.df = self.df.replace([np.inf, -np.inf], np.nan)
        
    def build_master_frame(self, files):
        self.get_features_df(self.files[0]) 
        self.mf = self.df
        self.df = None
        for file in self.files[1:]:     
            masterframe2 = None
            try:
                self.get_features_df(file)
            except:
                print("Problem building data from ",file)
            self.mf = pd.concat([self.mf, self.df], sort = False)


class RTQuICData_feat_65(RTQuICData):
    def __init__(self, excelfile, start_row_col  = (1, 3),
                 numCycles = 400, SEC_PER_CYCLE = 945.6):
        super().__init__(excelfile, start_row_col  = (1, 3),
                 numCycles = 400, SEC_PER_CYCLE = 945.6)


    def base_threshold(self, i):
        #unlabeled rows are excluded from calculation of base threshold
        df_dropna = self.df.dropna(subset =["Description"])
        return df_dropna["Base"].mean() + 5*df_dropna["Base"].std()





myResults = RTQuICData_feat(files[17])
myResults.setArray()
print(myResults.getArray())

##class RTQuICData(object):
##    def __init__(self, files):
##        self.files = files
##        self.df = None ##will be a dataframe
##        self.da = None ##will be a dataarray
##        self.mf = None ##will be a masterframe
##        self.build_master_frame(files)
##                  
##    def getMasterFrame(self):
##        return self.mf
##
##    def getData(self, file):
##        """If possible, return raw dataframe using excel file sheet as input"""
##        try:
##            self.df = pd.read_excel(basepath+file,
##                               sheet_name='Results',
##                               skiprows = 10,
##                               usecols='A,N:OW')
##        except FileNotFoundError:
##            print("In getData, File ",file," not found")
##            self.df = None
##        except ValueError:
##            print("Check sheet name")
##            self.df = None
##        except:
##            print("In getData, Couldn't make dataframe using file ",file)
##            self.df = None
##        #if toPrint: print("Original dataframe for ",file,"\n",self.df)
##            #delete all rows with NaN in second column
##        #self.df.dropna(how = "any", inplace = True)
##        #if toPrint: print("Data frame for ",file," with NaN dropped \n", self.df)
##        
##    def getArray(self, i):
##        for_array_df = self.df.iloc[i,1:num_cycles+1]
##        try:
##            self.da = for_array_df.to_numpy()
##        except:
##            print("Could not extract numeric data as array")
##            self.da = None
##
##    def threshold_cycle(self, v):
##        """helper function for finding first cycle where three successive
##        cycles give flourescence values greater than a given value v
##        """
##        for c in range(len(self.da)-2):        
##            if (self.da[c] > v
##                and self.da[c+1] > v
##                and self.da[c+2] > v):
##                return c
##
##    """Below are methods for calculating features"""
##    def maxVal(self, i):
##        try:
##            return np.amax(self.da)
##        except:
##            return np.NaN
##        
##    def _75maxVal(self, i):
##        """for calculating value that is 75% max"""
##        return 0.75*self.maxVal(i)
##
##    def base(self, i):
##        return self.da[2]
##
##    def base_threshold(self, i):
##        #unlabeled rows are excluded from calculation of base threshold
##        df_dropna = self.df.dropna(subset =["Description"])
##        return df_dropna["Base"].mean() + 5*df_dropna["Base"].std()
##
##    def time_to_base(self, i):
##        base_cyc = self.threshold_cycle(self.base_threshold(i))
##        try:
##            base_start = base_cyc*SEC_PER_CYCLE
##            base_start /= 3600
##            return base_start
##        except:
##            return np.NaN
##
##    def timeToMax(self, i):
##        """in hours"""
##        time_to_max = np.argmax(self.da)*SEC_PER_CYCLE
##        if not self.time_to_base(i) == np.NaN:
##            return round(time_to_max/3600, 1)
##        else:
##            return np.NaN
##        
##    def timeTo75Max(self, i):
##        """in hours"""
##        _75max = self._75maxVal(i)
##        time_to_0_75_max = np.argmax(self.da > _75max)*SEC_PER_CYCLE
##        if not self.time_to_base(i) == np.NaN:
##            return round(time_to_0_75_max/3600, 1)
##        else:
##            return np.NaN
##
##    def lagTime(self, i):
##        v = 3* self.da[1]
##        try:
##            lagtime_sec = self.threshold_cycle(v, self.da)*SEC_PER_CYCLE
##            return round(lagtime_sec/3600, 1)
##        except:
##            if default_lag:
##                lagtime_sec = num_cycles*SEC_PER_CYCLE
##                return round(lagtime_sec/3600, 1)
##            else:
##                return np.NaN
##            
##    def lagVal(self, i):
##        v = 3* self.da[1]
##        c = self.threshold_cycle(v)
##        if c != None:
##            return self.da[c]
##        else:
##            return np.NaN
##            
##    def areaUnderCurve(self, i):
##        val_above_baseline = self.da - self.base_threshold(i)
##        area = val_above_baseline.sum()
##        if area > 0:
##            return area
##        else:
##            return 0.0
##
##    def gradient(self, i):
##        """calculated as increase in fluorescence units
##        per unit time (in hours)
##        between the baseline and the 75% max val
##        """
##        min_ = self.base_threshold(i)
##        max_ = self._75maxVal(i)
##        gradient_start_cyc = self.threshold_cycle(min_)
##        gradient_end_val = max_
##        gradient_end_cyc = self.threshold_cycle(max_)
##        #print("gradient start flouresence" ,gradient_start_val)
##        #print("gradient start cycle"       ,gradient_start_cyc)
##        #print("gradient end flouresence"   ,gradient_end_val)
##        #print("gradient end cycle"   ,gradient_end_cyc)
##        try:
##            gradient = (max_ - min_)/(gradient_end_cyc - gradient_start_cyc)
##        except:
##            return np.NaN
##        gradient /= SEC_PER_CYCLE
##        gradient *= 3600
##        return round(gradient, 1)   
##       
##    method_dict = {"Base":base,
##                   "Base threshold":base_threshold,
##                   "Max Val": maxVal,
##                   "Time to Max": timeToMax,
##                   "Time to 75% max": timeTo75Max,
##                   "Lag Time": lagTime,
##                   "Lag Val": lagVal,
##                   "Gradient": gradient,
##                   "AUC": areaUnderCurve,
##                   "Time to base": time_to_base}
##
##    def addColumn(self, method_name):
##        self.df[method_name] = np.NaN
##        col_index = self.df.columns.get_loc(method_name)
##        for i in range(0, self.df.shape[0]):
##            self.getArray(i)
##            value = RTQuICData.method_dict[method_name](self, i)
##            self.df.iat[i, col_index] = value
##
##    def addFileTag(self, file):
##        self.df["file name"] = file
##        
##    def cleanDesc(self):
##        """ modify df to create correct unique descriptions
##        of the duplicate rows (assuming duplicates are used)
##        """    
##        for i in range(0, len(self.df)-1, 2):
##            ##try:
##            ##if not pd.isnull(self.df.iat[i+1,0]):
##            self.df.iat[i,0] = str(self.df.iat[i,0]) + " " + str(self.df.iat[i+1,0])
##            self.df.iat[i+1,0] = str(self.df.iat[i,0]) + " repeat"
##            ##except:
##              ##  print("Problem cleaning labels at index ",i)
##
##    def get_features_df(self,file):
##        """for excel file of rtquic data,
##        Returns a full dataframe of features
##        and an associated (and comparably indexed) numpy file of the raw data
##        """
##        self.getData(file)
##        try:
##            self.df.columns = self.df.iloc[0]
##        except:
##            print("Couldn't set columns for ",file)
##        self.df.drop(self.df.index[0], inplace = True)    
##        self.df = self.df[self.df.Description != 0]
##        if toPrint: print("Basic dataframe for ",file,"\n",self.df)
##        for method_name in RTQuICData.method_dict:
##            self.addColumn(method_name)
##        try:
##            self.addFileTag(file)
##        except:
##            print("problem tagging filename ", file) 
##        if clean_labels:
##            ##try:
##            self.cleanDesc()
##            if toPrint: print(self.df)
##            ##except:
##                ##print("Problem cleaning row names for ",file,"\n")
##        self.df = self.df.dropna(subset =["Description"])
##        if clean_labels:
##            self.df = self.df.loc[self.df['Description'] != "nan nan repeat"]
##            self.df = self.df.loc[self.df['Description'] != "nan nan"]
##        if toPrint:
##            print("Shape of dataframe", self.df.shape, "\n")
##        self.df = self.df.replace([np.inf, -np.inf], np.nan)
##        
##    def build_master_frame(self, files):
##        self.get_features_df(self.files[0]) 
##        self.mf = self.df
##        self.df = None
##        for file in self.files[1:]:     
##            masterframe2 = None
##            try:
##                self.get_features_df(file)
##            except:
##                print("Problem building data from ",file)
##            self.mf = pd.concat([self.mf, self.df], sort = False)
##
##def status(row):
##    for item in POSITIVES:
##        if item in row['Description']:
##            return "Blinded positive"
##    for item in M_POS_CONTROLS:
##        if item in row['Description']:
##            return "MM1 Positive control"
##    for item in V_POS_CONTROLS:
##        if item in row['Description']:
##            return "VV2 Positive control" 
##    for item in NEGATIVES:
##        if item in row['Description']:
##            return "Negative control"
##    return "test sample"
##
##def add_sub_conc(row):
##    for item in subconcs:
##        if item in row['Description']:
##            return subconcs[item][0]
##
##def add_sub_codon(row):
##    for item in subconcs:
##        if item in row['Description']:
##            return subconcs[item][1]
##
##def get_feat(feature, i, df):
##    series = df.columns.get_loc(feature)
##    return df.iat[i, series]
##
##def singlePlot(i, df, description = None, color = None, labels = True, parameters = False,):
##    """helper function for tracing plots"""
##    data_array = getArray(i, df)
##    hours_per_cycle = SEC_PER_CYCLE/3600
##    x_vals = [x*hours_per_cycle for x in range(1, num_cycles+1)]
##    plt.plot(x_vals, data_array, color)
##    if parameters:
##        gradient = get_feat("Gradient",i,df)
##        gradient_start = get_feat("Time to base",i,df)
##        gradient_base = base_threshold(i, df)
##        plt.plot(x_vals, [((x*gradient)+ gradient_base) for x in (x_vals - gradient_start)], label = "Gradient")      
##        parameters = (("Max Val","r"), ("Base threshold","g"), ("Lag Val","b"))
##        for parameter, c, in parameters:
##            plt.axhline(get_feat(parameter,i,df), color = c, label = parameter)
##        plt.legend()
##    plt.ylim(0,275000)
##    plt.xlim(0,(100*(num_cycles/400)))
##    if labels:
##        plt.title(description)           
##        plt.ylabel("Flourescence Units")
##        plt.xlabel("Time (hours)")
##
##def plot_all_trace(file): 
##    df = get_features_df(file)
##    num_traces = df.shape[0]       
##    for i in range(0, num_traces-9, 4):
##        for j in range(9):
##            plt.subplot(3, 3, j+1)
##            singlePlot(i+j, df, description, color, labels = False)
##        plt.show()
##
##def plot_by_description(file, description_dict):    
##    df = get_features_df(file) 
##    j = 1
##    for key, value in description_dict.items():
##        plt.subplot(2, 1, j)
##        for i in range(df.shape[0]):
##            try:
##                if key in get_feat("Description", i, df):
##                    singlePlot(i, df, key, color = value)
##                    print("plot for ", get_feat("Description", i, df))
##            except TypeError:
##                print("This for description in excel column",get_feat("Description", i, df))
##        j += 1
##    plt.show()
##
##method = {"file name":0,
##          "Description":1,
##          "Base":0,
##          "Max Val":1,
##          "Time to Max":1,
##          "Time to 75% max":0,
##          "Lag Time":1,
##          "Lag Val":1,
##          "Gradient":1,
##          "AUC":1,
##          "Base threshold":0,
##          "Time to base":0,
##          "Sample type":1,
##          "Substrate conc":1,
##          "Substrate codon":1
##          }
##
##def percentage_positive (df):
##    percentages = []    
##    for i in range(5):
##        df_sample = df.sample(replace = True, frac = 0.2)
##        num_samples = len(df_sample)
##        print("num samples ", num_samples)
##        df_sample = df_sample.dropna(subset =["Lag Time"])
##        num_positives = len(df_sample[df_sample["Lag Time"] <=100])
##        print("num_positives ", num_positives)
##        percentages.append(100*(num_positives/num_samples))
##    print(percentages)
##    print("False positive: ",np.mean(percentages),"% +/- ", np.std(percentages))
##    return np.mean(percentages), np.std(percentages)
##    
##def mean_lagtime (df):
##    """calculates mean of samples that have lagtimes. Those with NaN excluded"""
##    df = df.dropna(subset = ["Lag Time"])
##    print("Mean lagtime: ",df["Lag Time"].mean())
##    print("Std lagtime: ",df["Lag Time"].std())
##    print("n: ",len(df))
##    return df.mean(), df.std()

#get_features_df("Experimental plan RTQUIC17 018 AHP 65+study RETRO cases SD039 05 to 39 09.xlsx")

#########  Build master frame   #################################################
                
##mf = RTQuICData(files).getMasterFrame()
##
##with pd.option_context('display.max_rows',
##                       No   ne,
##                       #'display.max_columns',
##                       #None
##                       ): 
##
##    print(mf)

##### Reset index ###############################################################
##mf.set_index(pd.Series([x for x in range(len(mf))]), inplace = True)


###Additional columns
##mf['Sample type'] = mf.apply (lambda row: status(row), axis=1)
##mf['Substrate conc'] = mf.apply (lambda row: add_sub_conc(row), axis=1)
##mf['Substrate codon'] = mf.apply (lambda row: add_sub_codon(row), axis=1)


####### Filter out the positive reactions from the masterframe ####################
##mf.dropna(inplace = True)
##mf = mf[mf["Sample type"] == "Negative control"]
##mf = mf[mf["Description"].str.contains("Negative")]
##num_samples = len(mf)
##print("num samples ", num_samples)
##mf = mf.dropna(subset =["Lag Time"])
##num_positives = len(mf[mf["Lag Time"] <=100])
##print(100*(num_positives/num_samples))

##percentage_positive (mf)
##mf = mf[mf["Description"].str.contains("200409 HS23NV A MM1 seeded")]
##mf.drop(mf[mf["Description"] == "MM1 and VV2 FC"].index, inplace = True) 
##mf.drop(mf[mf["Description"] == "MM1 and VV2 FC repeat"].index, inplace = True) 
##mean_lagtime (mf)

##with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
##    print(mf.loc[:,["Description","Sample type","Lag Time"]])


##### select features for printing: 1= print, 0= don't print ####################
##for_display = []
##for selected in method:
##    if method[selected]:
##        for_display.append(selected)

##with pd.option_context('display.max_rows', None, 'display.max_columns', None):    
##    print(mf[for_display])

##from sklearn.preprocessing import MinMaxScaler
######
##mms = MinMaxScaler()
##var_norm = mms.fit_transform(mf[for_display])
###print("Numpy array of normalised data\n========\n",
###     var_norm,
###      "\n",type(var_norm))
##norm_df = pd.DataFrame(data = var_norm, columns = mf[for_display].columns)
##for category in "Description", "Sample type":
##    norm_df[category] = mf[category].reset_index(drop = True)
####print("Normalised data frame\n========\n", norm_df)
##print(norm_df.columns)

def pairwise_compare(var1, var2, df):
    assert var1 in df.columns
    assert var2 in df.columns
    for sample_type, colour in type_colour.items():
        subset_df = df.loc[df["Sample type"] == sample_type]
        plt.scatter(subset_df[var1],
                    subset_df[var2],
                    c = colour,
                    label = sample_type)
    plt.title(var1+ " vs "+ var2)
    plt.xlabel(var1 + " (min to max)")
    plt.ylabel(var2 + " (min to max)")
    plt.legend()
    plt.show()


def pairwise_compare_2(var1, var2, df):
    assert var1 in df.columns
    assert var2 in df.columns
    for codon_type, colour in codon_colour.items():
        subset_df = df.loc[df["Substrate codon"] == codon_type]
        plt.scatter(subset_df[var1],
                    subset_df[var2],
                    c = colour,
                    label = codon_type)
    plt.title(var1+ " vs "+ var2)
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.legend()
    plt.show()


def pairwise_compare_3(var1, var2, df):
    assert var1 in df.columns
    assert var2 in df.columns
    for pos_descr, colour in pos_control_colour.items():
        subset_df = df.loc[pos_descr in df["Description"]]
        plt.scatter(subset_df[var1],
                    subset_df[var2],
                    c = colour)
    plt.title(var1+ " vs "+ var2)
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.legend()
    plt.show()

##pairwise_compare_2( "Substrate conc", "Lag Time", mf)

#from pandas.plotting import scatter_matrix
#scatter_matrix(norm_df)
##
##correlation = norm_df.corr()
##
##print(correlation)
##
##fig = plt.figure()
##ax = fig.add_subplot(111)
##cax = ax.matshow(correlation, vmin=-1, vmax=1)
##fig.colorbar(cax)
##plt.show()

### Create dataframe out of result so we can use .describe() later
##var_norm_df = pd.DataFrame(data = var_norm, columns = X.columns)
##
##plt.subplot(1, 2, 1) 
##plt.hist(x=X['INDUS'], bins='auto', rwidth=0.85)
##plt.title('Not scaled')
##
##plt.subplot(1, 2, 2) 
##plt.hist(x=var_norm_df['INDUS'], bins='auto', rwidth=0.85)
##plt.title('Min-max scaled')
##plt.tight_layout()
##plt.show()
##
##print(X['INDUS'].describe())
##print(var_norm_df['INDUS'].describe())
    
#generate an array of RT-QuIC plate data

##print(for_array_df)
##for_array_df_numeric = for_array_df.apply(pd.to_numeric)
##print(for_array_df_numeric)
##print(for_array_df_numeric.T.describe())

##print("Conversion to array \n ",data_array_2D)
##labelled_row_data_df = non_nan_df.iloc[1:,0:1]
##labelled_row_data_df.rename(columns={'Back to experimental setup': 'Labels'}, inplace = True)
##print("Just labels df\n", labelled_row_data_df)
##print(len(data_array_2D[:]))
##labelled_row_data_df["Row Data"]= data_array_2D[:]
##print(labelled_row_data_df)

#df = df[pd.notnull(df[0])]
       
#plotTrace("Experimental plan RTQUIC18 008 AHP 65+study cases SD 012 18 BATCH 6 and 7 MARCELO FLY.xlsx")


##plot_by_description("RT-QUIC READ 20.003.xlsx",substrates)

