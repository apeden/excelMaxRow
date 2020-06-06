import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
    """Return raw dataframe using excel file sheet as input"""
    try:
        df = pd.read_excel(basepath+file,
                           sheet_name='Results',
                           skiprows = 10,
                           usecols='A,N:OW')
    except FileNotFoundError:
        print("In getData, File ",file," not found")
    except:
        print("In getData, Couldn't make dataframe using file ",file)
    if toPrint: print("Original dataframe for ",file,"\n",df)
        #delete all rows with NaN in second column
    #df.dropna(how = "any", inplace = True)
    if toPrint: print("Data frame for ",file," with NaN dropped \n", df)
    return df

def splitNumbers(dataframe):
    features_df = dataframe.iloc[:,0:1]
    if toPrint: print(features_df)
    for_array_df = dataframe.iloc[:,1:401]
    try:
        data_array_2D = for_array_df.to_numpy()
    except:
        print("Could not extract numeric data as array")
    if toPrint: print(data_array_2D)
    return features_df.copy(), data_array_2D.copy() 

"""helper function for finding first cycle where three successive
cycles give flourescence values greater than a given value v
"""
def threshold_cycle(v, data_array_2D, i):
    for c in range(len(data_array_2D[i])-2):        
        if (data_array_2D[i][c] > v
            and data_array_2D[i][c+1] > v
            and data_array_2D[i][c+2] > v):
            print ("threshold cycle is ",str(c))
            return c

"""Methods for calculating features"""
def maxVal(i, data_array_2D):
    try:
        return np.amax(data_array_2D[i])
    except:
        return np.NaN
    
def timeToMax(i, data_array_2D):
    """in hours"""
    time_to_max = np.argmax(data_array_2D[i])*SEC_PER_CYCLE
    if not lagTime(i, data_array_2D) == np.NaN:
        return round(time_to_max/3600, 1)
    else:
        return np.NaN
    
def lagTime(i, data_array_2D):
    v = 3* data_array_2D[i][1]
    try:
        lagtime_sec = threshold_cycle(v, data_array_2D, i)*SEC_PER_CYCLE
        return round(lagtime_sec/3600, 1)
    except:
        return np.NaN

def lagVal(i, data_array_2D):
    v = 3* data_array_2D[i][1]
    c = threshold_cycle(v, data_array_2D, i)
    if c != None:
        return data_array_2D[i][c]
    else:
        return np.NaN

def gradient(i, data_array_2D, interval = 10):
    """calculated as increase in fluorescence units
    per unit time (in hours) for a specified interval
    between the baseline and the max val
    """
    baseline_mean = np.mean(data_array_2D[:][2])
    baseline_std = np.std(data_array_2D[:][2])
    min_ = baseline_mean + 5*baseline_std
    max_ = maxVal(i, data_array_2D)
    range_ = max_ - min_
    gradient_start_val = min_ + ((range_/2) - (range_*(interval/100)*(1/2)))
    gradient_start_cyc = threshold_cycle(gradient_start_val, data_array_2D, i)
    gradient_end_val = max_ - ((range_/2) - (range_*(interval/100)*(1/2)))
    gradient_end_cyc = threshold_cycle(gradient_end_val, data_array_2D, i)
    print("gradient start flouresence" ,gradient_start_val)
    print("gradient start cycle"       ,gradient_start_cyc)
    print("gradient end flouresence"   ,gradient_end_val)
    print("gradient end cycle"   ,gradient_end_cyc)
    try:
        gradient = (gradient_end_val - gradient_start_val)/(gradient_end_cyc - gradient_start_cyc)
        gradient /= SEC_PER_CYCLE
        gradient *= 3600
        print("gradient"   ,gradient)
        return round(gradient, 1)
        
    except:
        return np.NaN

def base_threshold(i, data_array_2D):
    baseline_mean = np.mean(data_array_2D[:][2])
    baseline_std = np.std(data_array_2D[:][2])
    return baseline_mean + 5*baseline_std


def gradientStart(i, data_array_2D, interval = 10):
    """used purely as a starting point for
    drawing the line of best fit
    """
    baseline_mean = np.mean(data_array_2D[:][2])
    baseline_std = np.std(data_array_2D[:][2])
    min_ = baseline_mean + 5*baseline_std
    max_ = maxVal(i, data_array_2D)
    range_ = max_ - min_
    try:
        gradient_start_val = min_ + ((range_- interval)/2)
        gradient_start_cyc = threshold_cycle(gradient_start_val, data_array_2D, i)
        gradient_start = gradient_start_cyc*SEC_PER_CYCLE
        gradient_start /= 3600
        print("Gradient start is ",str(gradient_start))
        return gradient_start
    except:
        return np.NaN

def areaUnderCurve(i, data_array_2D):
    baseline = data_array_2D[i][1]
    val_above_baseline = data_array_2D[i] - baseline
    area = val_above_baseline.sum()
    if area > 0:
        return area
    else:
        return 0.0
    
method_dict = {"Max Val": maxVal,
               "Time to Max": timeToMax,
               "Lag Time": lagTime,
               "Lag Val": lagVal,
               "Gradient": gradient,
               "Gradient Start" : gradientStart,
               "AUC": areaUnderCurve,
               "Base threshold":base_threshold}

def addColumn(method_name, features_df, data_array_2D):
    features_df[method_name] = np.NaN
    col_index = features_df.columns.get_loc(method_name)
    for i in range(0,features_df.shape[0]):
        value = method_dict[method_name](i, data_array_2D)
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
    df = getData(file)
    try:
        df.columns = df.iloc[0]
    except:
        print("Couldn't set columns for ",file)
    try:
        df.drop(df.index[0], inplace = True)    
        df = df[df.Description != 0]
    except:
        print("Problem with cleaning null or zero rows for ",file)
    if toPrint: print("Basic dataframe for ",file,"\n",df)
    try:
        features_df, data_array_2D = splitNumbers(df)
    except:
        print("Problem with splitting row labels and numbers for ",file)
    for method_name in method_dict:
        try:
            addColumn(method_name, features_df, data_array_2D)
        except:
            print("Problem calculating ",method_name, " for ",file)
    try:
        addFileTag(features_df, file)
    except:
        print("problem tagging filename ", file) 
    try:
        cleanDesc(features_df)
        if toPrint: print(features_df)
        return features_df, data_array_2D
    except:
        print("Problem cleaning row names for ",file,"\n",features_df)

    
def build_master_frame(files):
    masterframe = None
    try:
        masterframe = get_features_df(files[0])
    except:
        print("Problem building first data from ",files[0])
    for file in files[1:]:     
        masterframe2 = None
        try:
            masterframe2 = get_features_df(file)
        except:
            print("Problem building data from ",file)
        try:
            masterframe = pd.concat([masterframe, masterframe2])
        except:
            print("Problem concatenating dataframe from ",file)
    return masterframe

#get_features_df("Experimental plan RTQUIC17 018 AHP 65+study RETRO cases SD039 05 to 39 09.xlsx")

##mf = build_master_frame(files)
##print(mf.index)
##mf.set_index(pd.Series([x for x in range(len(mf))]), inplace = True)
##print(mf.index)

#######Filter out the positive reactions from the masterframe
##mf.dropna(inplace = True)
##mf = mf[mf.Gradient > 0]
##with pd.option_context('display.max_rows', None, 'display.max_columns', None):    
##    print("Master dataframe\n========\n", mf)

##from sklearn.preprocessing import MinMaxScaler
##
##mms = MinMaxScaler()
##var_norm = mms.fit_transform(mf.iloc[:,2:])
##print("Numpy array of normalised data\n========\n",
##      var_norm,
##      "\n",type(var_norm))
##norm_df = pd.DataFrame(data = var_norm, columns = mf.iloc[:,2:].columns)
##norm_df["Description"] = pd.Series(mf["Description"])
##print("Normalised data frame\n========\n",
##      norm_df)
##print(norm_df.columns)
##plt.scatter(norm_df["Time to Max"],norm_df["Lag Time"])
##from pandas.plotting import scatter_matrix
##scatter_matrix(norm_df)
##plt.show()

##
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

def plotTrace(file, description):
    hours_per_cycle = SEC_PER_CYCLE/3600
    features_df, data_array_2D = get_features_df(file)
    desc_index = features_df.columns.get_loc("Description")
    grad_index = features_df.columns.get_loc("Gradient")
    grad_start_index = features_df.columns.get_loc("Gradient Start")
    max_index = features_df.columns.get_loc("Max Val")
    base_index = features_df.columns.get_loc("Base threshold")
    
    for i in range(0, features_df.shape[0]):
        if features_df.iat[i, desc_index] == description:
            x_vals = [x*hours_per_cycle for x in range(1, len(data_array_2D[i])+1)] 
            plt.plot(x_vals, data_array_2D[i])
            #print (features_df[description])
            with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
                print (features_df)
            gradient = features_df.iat[i, grad_index]
            gradient_start = features_df.iat[i, grad_start_index]
            plt.plot(x_vals, [x*gradient for x in x_vals- gradient_start])
            plt.ylabel("Flourescence Units")
            plt.xlabel("Time (hours)")
            plt.axhline(features_df.iat[i, max_index])
            plt.axhline(features_df.iat[i, base_index])
            plt.title(file+"\n"+description)
            plt.show()
            return
    print("Could not find data to plot")
            
plotTrace("Experimental plan RTQUIC18 008 AHP 65+study cases SD 012 18 BATCH 6 and 7 MARCELO FLY.xlsx","SD012/18 FC")

##    if plotGradient:
##        g = features_df.loc[features_df.index[i], 'Gradient']
##        lagTm =
##        lagVal
##        if g != nan(plotGradient and features_df != NaN
##            plt.plot(x_vals, g(x_vals - 
    
