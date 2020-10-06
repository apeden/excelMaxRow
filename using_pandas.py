import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math


toPrint = False
SEC_PER_CYCLE = 945.6
num_cycles = 400
files = []
basepath = "RTQuIC_for_analysis/"
plt.subplots_adjust(wspace = 0.4)
plt.subplots_adjust(hspace = 0.6)

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

POS_CONTROLS = "MM1", "VV2", "15.689", "15.692"

NEGATIVES = "MM","MV","VV" "15.32", "15.323", "15.317"

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
    
##def splitNumbers(dataframe):
##    """split off numeric rtquic data from (equivalently indexed) data labels
##    Return a 2D array (numeric data) and simple dataframe of labels
##    """
##    features_df = dataframe.iloc[:,0:1]
##    if toPrint: print(features_df)
##    for_array_df = dataframe.iloc[:,1:401]
##    try:
##        data_array_2D = for_array_df.to_numpy()
##    except:
##        print("Could not extract numeric data as array")
##    if toPrint: print(data_array_2D)
##    return features_df.copy(), data_array_2D.copy() 

def getArray(i, dataframe):
    for_array_df = dataframe.iloc[i,1:num_cycles+1]
    try:
        return for_array_df.to_numpy()
    except:
        print("Could not extract numeric data as array")


def threshold_cycle(v, data_array):
    """helper function for finding first cycle where three successive
    cycles give flourescence values greater than a given value v
    """
    for c in range(len(data_array)-2):        
        if (data_array[c] > v
            and data_array[c+1] > v
            and data_array[c+2] > v):
            return c

"""Below are methods for calculating features"""
def maxVal(i, dataframe):
    data_array = getArray(i, dataframe)
    try:
        return np.amax(data_array)
    except:
        return np.NaN
    
def _75maxVal(i, dataframe):
    """for calculating value that is 75% max"""
    return 0.75*maxVal(i, dataframe)

def base(i, dataframe):
    data_array = getArray(i, dataframe)
    return data_array[2]

def base_threshold(i, dataframe):
    """unlabeled rows are excluded from calculation of base threshold"""
    dataframe_dropna = dataframe.dropna(subset =["Description"])
    return dataframe_dropna["Base"].mean() + 5*dataframe_dropna["Base"].std()


def time_to_base(i, dataframe):
    data_array = getArray(i, dataframe)
    base_cyc = threshold_cycle(base_threshold(i, dataframe),
                                         data_array)
    try:
        base_start = base_cyc*SEC_PER_CYCLE
        base_start /= 3600
        return base_start
    except:
        return np.NaN


def timeToMax(i, dataframe):
    """in hours"""
    data_array = getArray(i, dataframe)
    time_to_max = np.argmax(data_array)*SEC_PER_CYCLE
    if not time_to_base(i, dataframe) == np.NaN:
        return round(time_to_max/3600, 1)
    else:
        return np.NaN
    
def timeTo75Max(i, dataframe):
    """in hours"""
    _75max = _75maxVal(i, dataframe)
    data_array = getArray(i, dataframe)
    time_to_0_75_max = np.argmax(data_array > _75max)*SEC_PER_CYCLE
    if not time_to_base(i, dataframe) == np.NaN:
        return round(time_to_0_75_max/3600, 1)
    else:
        return np.NaN

def lagTime(i, dataframe):
    data_array = getArray(i, dataframe)
    v = 3* data_array[1]
    try:
        lagtime_sec = threshold_cycle(v, data_array)*SEC_PER_CYCLE
        return round(lagtime_sec/3600, 1)
    except:
        return np.NaN

def lagVal(i, dataframe):
    data_array = getArray(i, dataframe)
    v = 3* data_array[1]
    c = threshold_cycle(v, data_array)
    if c != None:
        return data_array[c]
    else:
        return np.NaN
        
def areaUnderCurve(i, dataframe):
    data_array = getArray(i, dataframe)
    baseline = base_threshold(i, dataframe)
    val_above_baseline = data_array - baseline
    area = val_above_baseline.sum()
    if area > 0:
        return area
    else:
        return 0.0

def gradient(i, dataframe):
    """calculated as increase in fluorescence units
    per unit time (in hours)
    between the baseline and the 75% max val
    """
    data_array = getArray(i, dataframe)
    min_ = base_threshold(i, dataframe)
    max_ = _75maxVal(i, dataframe)
    gradient_start_val = min_
    gradient_start_cyc = threshold_cycle(gradient_start_val, data_array)
    gradient_end_val = max_
    gradient_end_cyc = threshold_cycle(gradient_end_val, data_array)
    #print("gradient start flouresence" ,gradient_start_val)
    #print("gradient start cycle"       ,gradient_start_cyc)
    #print("gradient end flouresence"   ,gradient_end_val)
    #print("gradient end cycle"   ,gradient_end_cyc)
    try:
        gradient = (gradient_end_val - gradient_start_val)/(gradient_end_cyc - gradient_start_cyc)
    except:
        return np.NaN
    gradient /= SEC_PER_CYCLE
    gradient *= 3600
    return round(gradient, 1)   
   
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

def addColumn(method_name, method_dict, dataframe):
    dataframe[method_name] = np.NaN
    col_index = dataframe.columns.get_loc(method_name)
    for i in range(0,dataframe.shape[0]):
        value = method_dict[method_name](i, dataframe)
        dataframe.iat[i, col_index] = value
    return dataframe

def addFileTag(dataframe, file):
    dataframe["file name"] = file
    return dataframe
    
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

def get_features_df(file, clean_labels = True):
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
    for method_name in method_dict:
        addColumn(method_name, method_dict, df)
    try:
        addFileTag(df, file)
    except:
        print("problem tagging filename ", file) 
    if clean_labels:
        try:
            cleanDesc(df)
            if toPrint: print(df)
        except:
            print("Problem cleaning row names for ",file,"\n")
    df = df.dropna(subset =["Description"])
    if clean_labels:
        df = df.loc[df['Description'] != "nan repeat"]
    if toPrint:
        print("Shape of dataframe", df.shape, "\n")
    df = df.replace([np.inf, -np.inf], np.nan)
    return df
    
def build_master_frame(files):
    masterframe = None
    masterframe = get_features_df(files[0])  
    for file in files[1:]:     
        masterframe2 = None
        try:
            masterframe2 = get_features_df(file)
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

def singlePlot(i, df, description = None, color = None, labels = True, parameters = False,):
    """helper function for tracing plots"""
    data_array = getArray(i, df)
    hours_per_cycle = SEC_PER_CYCLE/3600
    x_vals = [x*hours_per_cycle for x in range(1, num_cycles+1)]
    plt.plot(x_vals, data_array, color)
    if parameters:
        gradient = get_feat("Gradient",i,df)
        gradient_start = get_feat("Time to base",i,df)
        gradient_base = base_threshold(i, df)
        plt.plot(x_vals, [((x*gradient)+ gradient_base) for x in (x_vals - gradient_start)], label = "Gradient")      
        parameters = (("Max Val","r"), ("Base threshold","g"), ("Lag Val","b"))
        for parameter, c, in parameters:
            plt.axhline(get_feat(parameter,i,df), color = c, label = parameter)
        plt.legend()
    plt.ylim(0,275000)
    plt.xlim(0,(100*(num_cycles/400)))
    if labels:
        plt.title(description)           
        plt.ylabel("Flourescence Units")
        plt.xlabel("Time (hours)")

def plot_all_trace(file): 
    df = get_features_df(file)
    num_traces = df.shape[0]       
    for i in range(0, num_traces-9, 4):
        for j in range(9):
            plt.subplot(3, 3, j+1)
            singlePlot(i+j, df, description, color, labels = False)
        plt.show()

def plot_by_description(file, description_dict):    
    df = get_features_df(file) 
    j = 1
    for key, value in description_dict.items():
        plt.subplot(3, 2, j)
        for i in range(df.shape[0]):
            try:
                if key in get_feat("Description", i, df):
                    singlePlot(i, df, key, color = value)
                    print("plot for ", get_feat("Description", i, df))
            except TypeError:
                print("This for description in excel column",get_feat("Description", i, df))
        j += 1
    plt.show()

method = {"file name":0,
          "Description":1,
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
                
mf = build_master_frame(files)


##### Reset index ###############################################################
##mf.set_index(pd.Series([x for x in range(len(mf))]), inplace = True)
mf['Sample type'] = mf.apply (lambda row: status(row), axis=1)
##
####### Filter out the positive reactions from the masterframe ####################
##mf.dropna(inplace = True)




def percentage_positive (num_trials, df):
    percentages = []    
    for i in range(5):
        df_sample = df.sample(replace = True, frac = 0.2)
        num_samples = len(df_sample)
        print("num samples ", num_samples)
        df_sample = df_sample.dropna(subset =["Lag Time"])
        num_positives = len(df_sample[df_sample["Lag Time"] <=100])
        print("num_positives ", num_positives)
        percentages.append(100*(num_positives/num_samples))
    print(percentages)
    print("False positive: ",np.mean(percentages),"% +/- ", np.std(percentages))
    return np.mean(percentages), np.std(percentages)
    
        


num_trials =10
mf = mf[mf["Sample type"] == "Negative control"]
with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
    print(mf.loc[:,["Description","Sample type","Lag Time"]])
percentage_positive (num_trials, mf)


##### select features for printing: 1= print, 0= don't print ####################
for_display = []
for selected in method:
    if method[selected]:
        for_display.append(selected)

##with pd.option_context('display.max_rows', None, 'display.max_columns', None):    
    ##print(mf[for_display])


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

##substrates = {"HS23NM 140211 unseeded":"r",
##              "431 HuM129F9STOP ID50161 unseeded":"b",
##              "432 HuV129F6STOP ID50162 unseeded":"g",
##              "432 HuV129F11STOP ID204751 unseeded":"c",
##              "200409 HS23NV A unseeded":"m",
##              'Ha Fl PrP "M" unseeded':"y"}
##
##plot_by_description("Labeled RTQUIC20 002 partial.xlsx",substrates)

