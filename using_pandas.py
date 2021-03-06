import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math

toPrint = True
SEC_PER_CYCLE = 945.6
#file = "Experimental plan RTQUIC19 003 AHP 65+study cases BATCH 17 and 18.xlsx"
files = []
basepath = "RTQuIC_for_analysis/"

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

POS_CONTROLS = "MM1","VV2"

NEGATIVES = "MM","MV","VV"

with os.scandir(basepath) as entries:
    for entry in entries:
        try:
            assert(entry.is_file())
            files.append(entry.name)
        except:
            print(entry.name, " is apparently a problem file.")
    for file in files:
        print(file)
                
def getData(file):
    """If possible, return raw dataframe using excel file sheet as input"""
    try:
        df = pd.read_excel(basepath+file,
                           sheet_name='Results',
                           skiprows = 10,
                           usecols='A,N:OW')
        return df
    except FileNotFoundError:
        print("In getData, File ",file," not found")
    except:
        print("In getData, Couldn't make dataframe using file ",file)
    #if toPrint: print("Original dataframe for ",file,"\n",df)
        #delete all rows with NaN in second column
    #df.dropna(how = "any", inplace = True)
    #if toPrint: print("Data frame for ",file," with NaN dropped \n", df)
    
def splitNumbers(dataframe):
    """split off numeric rtquic data from (equivalently indexed) data labels
    Return a 2D array (numeric data) and simple dataframe of labels
    """
    features_df = dataframe.iloc[:,0:1]
    if toPrint: print(features_df)
    for_array_df = dataframe.iloc[:,1:401]
    try:
        data_array_2D = for_array_df.to_numpy()
    except:
        print("Could not extract numeric data as array")
    if toPrint: print(data_array_2D)
    return features_df.copy(), data_array_2D.copy() 

def threshold_cycle(v, data_array_2D, i):
    """helper function for finding first cycle where three successive
    cycles give flourescence values greater than a given value v
    """
    for c in range(len(data_array_2D[i])-2):        
        if (data_array_2D[i][c] > v
            and data_array_2D[i][c+1] > v
            and data_array_2D[i][c+2] > v):
            return c

"""Below are methods for calculating features"""
def maxVal(i, data_array_2D, features_df):
    try:
        return np.amax(data_array_2D[i])
    except:
        return np.NaN
    
def _75maxVal(i, data_array_2D, features_df):
    """helper function foor calculating value that is 75% max"""
    return 0.75*maxVal(i, data_array_2D, features_df)

def timeToMax(i, data_array_2D, features_df):
    """in hours"""
    time_to_max = np.argmax(data_array_2D[i])*SEC_PER_CYCLE
    if not time_to_base(i, data_array_2D, features_df) == np.NaN:
        return round(time_to_max/3600, 1)
    else:
        return np.NaN
    
def timeTo75Max(i, data_array_2D, features_df):
    """in hours"""
    _75max = _75maxVal(i, data_array_2D, features_df)
    time_to_0_75_max = np.argmax(data_array_2D[i] > _75max)*SEC_PER_CYCLE
    if not time_to_base(i, data_array_2D, features_df) == np.NaN:
        return round(time_to_0_75_max/3600, 1)
    else:
        return np.NaN

def lagTime(i, data_array_2D, features_df):
    v = 3* data_array_2D[i][1]
    try:
        lagtime_sec = threshold_cycle(v, data_array_2D, i)*SEC_PER_CYCLE
        return round(lagtime_sec/3600, 1)
    except:
        return np.NaN

def lagVal(i, data_array_2D, features_df):
    v = 3* data_array_2D[i][1]
    c = threshold_cycle(v, data_array_2D, i)
    if c != None:
        return data_array_2D[i][c]
    else:
        return np.NaN

def base(i, data_array_2D, features_df):
    return data_array_2D[i,2]

def base_threshold(i, data_array_2D, features_df):
    """unlabeled rows are excluded from calculation of base threshold"""
    features_df = features_df.dropna(subset =["Description"])
    return features_df["Base"].mean() + 5*features_df["Base"].std()

def time_to_base(i, data_array_2D, features_df):
    base_cyc = threshold_cycle(base_threshold(i, data_array_2D, features_df),
                                         data_array_2D, i)
    try:
        base_start = base_cyc*SEC_PER_CYCLE
        base_start /= 3600
        return base_start
    except:
        return np.NaN
        
def areaUnderCurve(i, data_array_2D, features_df):
    baseline = base_threshold(i, data_array_2D, features_df)
    val_above_baseline = data_array_2D[i] - baseline
    area = val_above_baseline.sum()
    if area > 0:
        return area
    else:
        return 0.0

def gradient(i, data_array_2D, features_df):
    """calculated as increase in fluorescence units
    per unit time (in hours)
    between the baseline and the 75% max val
    """
    min_ = base_threshold(i, data_array_2D, features_df)
    max_ = _75maxVal(i, data_array_2D, features_df)
    gradient_start_val = min_
    gradient_start_cyc = threshold_cycle(gradient_start_val, data_array_2D, i)
    gradient_end_val = max_
    gradient_end_cyc = threshold_cycle(gradient_end_val, data_array_2D, i)
    #print("gradient start flouresence" ,gradient_start_val)
    #print("gradient start cycle"       ,gradient_start_cyc)
    #print("gradient end flouresence"   ,gradient_end_val)
    #print("gradient end cycle"   ,gradient_end_cyc)
    try:
        gradient = (gradient_end_val - gradient_start_val)/(gradient_end_cyc - gradient_start_cyc)
        gradient /= SEC_PER_CYCLE
        gradient *= 3600
        return round(gradient, 1)    
    except:
        return np.NaN
   
method_dict = { "Base":base,
                "Base threshold":base_threshold,
                "Max Val": maxVal,
                "Time to Max": timeToMax,
                "Time to 75% max": timeTo75Max,
                "Lag Time": lagTime,
                "Lag Val": lagVal,
                "Gradient": gradient,
                "AUC": areaUnderCurve,
                "Time to base": time_to_base}

def addColumn(method_name, method_dict, features_df, data_array_2D):
    features_df[method_name] = np.NaN
    col_index = features_df.columns.get_loc(method_name)
    for i in range(0,features_df.shape[0]):
        value = method_dict[method_name](i, data_array_2D, features_df)
        features_df.iat[i, col_index] = value

def addFileTag(features_df, file):
    features_df["file name"] = file
    
def cleanDesc(df):
    """ modify df to create correct unique descriptions
    of the duplicate rows (assuming duplicates are used)
    """    
    for i in range(0, len(df)-1, 2):
        try:
            if not pd.isnull(df.iat[i+1,0]):
                df.iat[i,0] = str(df.iat[i,0]) + " " + str(df.iat[i+1,0])
            df.iat[i+1,0] = str(df.iat[i,0]) + " repeat"
        except:
            print("Problem cleaning labels at index ",i)


def get_features_df(file):
    """for excel file of rtquic data,
    Returns a full dataframe of features
    and an associated (and comparably indexed) numpy file of the raw data
    """
    df = getData(file)
    try:
        df.columns = df.iloc[0]
    except:
        print("Couldn't set columns for ",file)
    df.drop(df.index[0], inplace = True)    
    df = df[df.Description != 0]
    if toPrint: print("Basic dataframe for ",file,"\n",df)
    try:
        features_df, data_array_2D = splitNumbers(df)
    except:
        print("Problem with splitting row labels and numbers for ",file)
    for method_name in method_dict:
        addColumn(method_name, method_dict, features_df, data_array_2D)
    try:
        addFileTag(features_df, file)
    except:
        print("problem tagging filename ", file) 
    try:
        cleanDesc(features_df)
        if toPrint: print(features_df)
    except:
        print("Problem cleaning row names for ",file,"\n")
    ##features_df = features_df.dropna(subset =["Description"])
    if toPrint:
        print("Shape of dataframe", features_df.shape, "\n",
              "Shape of accompanying numpy array", data_array_2D.shape, "\n")
    return features_df, data_array_2D
    
def build_master_frame(files):
    masterframe = None
    masterframe, _ = get_features_df(files[0])
    for file in files[1:]:     
        masterframe2 = None
        try:
            masterframe2, _ = get_features_df(file)
        except:
            print("Problem building data from ",file)
        masterframe = pd.concat([masterframe, masterframe2])
    return masterframe

def status(row):
    for item in POSITIVES:
        if item in row['Description']:
            return "Blinded positive"
    for item in POS_CONTROLS:
        if item in row['Description']:
            return "Positive control"    
    for item in NEGATIVES:
        if item in row['Description']:
            return "Negative control"
    return "test sample"

type_colour = {"Blinded positive":"r",
               "Positive control":"b",
               "Negative control":"g",
               "test sample":"y"}

def get_feat(feature, i, df):
    series = df.columns.get_loc(feature)
    return df.iat[i, series]

def plotTrace(file, description = None):
    hours_per_cycle = SEC_PER_CYCLE/3600
    features_df, data_array_2D = get_features_df(file)
    num_traces = features_df.shape[0]
    x_vals = [x*hours_per_cycle for x in range(1, len(data_array_2D[0])+1)]
    
    def singlePlot(i, labels = True):
        plt.plot(x_vals, data_array_2D[i])
        gradient = get_feat("Gradient",i,features_df)
        gradient_start = get_feat("Time to base",i,features_df)
        gradient_base = base_threshold(i, data_array_2D, features_df)
        plt.plot(x_vals, [((x*gradient)+ gradient_base) for x in (x_vals - gradient_start)], label = "Gradient")      
        parameters = (("Max Val","r"), ("Base threshold","g"), ("Lag Val","b"))
        for parameter, c, in parameters:
            plt.axhline(get_feat(parameter,i,features_df), color = c, label = parameter)
        plt.ylim(0,200000)
        plt.xlim(0,100)
        if labels:
            plt.legend()
            plt.ylabel("Flourescence Units")
            plt.xlabel("Time (hours)")
        
    if description == None:
        for i in range(0, num_traces-9, 4):
            for j in range(9):
                plt.subplot(3, 3, j+1)
                singlePlot(i+j, labels = False)
            plt.subplots_adjust(wspace = 0.4)
            plt.subplots_adjust(hspace = 0.6)
            plt.show()
    else:
        for i in range(num_traces):
            if get_feat("Description", i, features_df) == description:                
                singlePlot(i)            
                plt.show()

method = {"file name":0,
          "Description":0,
          "Base":0,
          "Max Val":1,
          "Time to Max":1,
          "Time to 75% max":0,
          "Lag Time":1,
          "Lag Val":1,
          "Gradient":1,
          "AUC":1,
          "Base threshold":0,
          "Time to base":0,
          "Sample type":0}

#get_features_df("Experimental plan RTQUIC17 018 AHP 65+study RETRO cases SD039 05 to 39 09.xlsx")

#########  Build master frame   #################################################
                
##mf = build_master_frame(files)

##### Reset index ###############################################################
##mf.set_index(pd.Series([x for x in range(len(mf))]), inplace = True)
##mf['Sample type'] = mf.apply (lambda row: status(row), axis=1)
##
####### Filter out the positive reactions from the masterframe ####################
##mf.dropna(inplace = True)
##mf = mf[mf.Gradient > 0]

##### select features for printing: 1= print, 0= don't print ####################
##for_display = []
##for selected in method:
##    if method[selected]:
##        for_display.append(selected)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):    
#   print("Master dataframe\n========\n", mf)

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

def pairwise_compare(var1, var2):
    assert var1 in norm_df.columns
    assert var2 in norm_df.columns
    for sample_type, colour in type_colour.items():
        subset_df = norm_df.loc[norm_df["Sample type"] == sample_type]
        plt.scatter(subset_df[var1],
                    subset_df[var2],
                    c = colour,
                    label = sample_type)
    plt.title(var1+ " vs "+ var2)
    plt.xlabel(var1 + " (min to max)")
    plt.ylabel(var2 + " (min to max)")
    plt.legend()
    plt.show()

##pairwise_compare("AUC", "Lag Time")

##from pandas.plotting import scatter_matrix
##scatter_matrix(norm_df)
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
plotTrace("Experimental plan RTQUIC18 008 AHP 65+study cases SD 012 18 BATCH 6 and 7 MARCELO FLY.xlsx", "VV2 pos control FC")

