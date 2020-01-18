import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SEC_PER_CYCLE = 945.6
file = "Experimental plan RTQUIC19 003 AHP 65+study cases BATCH 17 and 18.xlsx"

def getData(file, toPrint = True):
    try:
        df = pd.read_excel("RTQuIC_for_analysis/"+file,
                           sheet_name='Results',
                           usecols='A,N:OW')
    except FileNotFoundError:
        print("In getData, File not found")
    except:
        print("In getData, Couldn't make dataframe")
    if toPrint: print("Original dataframe \n",df)
        #delete all rows indexed with NaN
    df.dropna(how = 'any', inplace = True)
    if toPrint: print("Data frame with NaN dropped \n", df)
    return df

def splitNumbers(dataframe, toPrint = True):
        #select only index and first column and save as features_df
    features_df = dataframe.iloc[:,0:1]
    if toPrint: print(features_df)
        #delete non_numeric columns that wont go to np.array
    for_array_df = dataframe.iloc[:,1:401]
        #create numpy array
    data_array_2D = for_array_df.to_numpy()
        #print numpy array
    if toPrint: print(data_array_2D)
        #copy returned to avoid SettingwithCopyWarning
    return features_df.copy(), data_array_2D.copy() 


"""Methods for calculating features"""
def maxVal(i):
    try:
        return np.amax(data_array_2D[i])
    except:
        return np.NaN
def timeToMax(i):
    time_to_max = np.argmax(data_array_2D[i])*SEC_PER_CYCLE
    if not lagTime(i) == np.NaN:
        return round(time_to_max/3600, 1)
    else:
        return np.NaN
def lagTime(i):
    t = 3* data_array_2D[i][1]
    for j in range(len(data_array_2D[i])-2):        
        if (data_array_2D[i][j] > t
            and data_array_2D[i][j+1] > t
            and data_array_2D[i][j+2] > t):
            lag_time = j*SEC_PER_CYCLE
            return round(lag_time/3600, 1)
    return np.NaN
def lagVal(i):
    baseline = data_array_2D[i][1]
    t = 3* baseline
    for j in range(len(data_array_2D[i])-2):        
        if (data_array_2D[i][j] > t
            and data_array_2D[i][j+1] > t
            and data_array_2D[i][j+2] > t):
            return data_array_2D[i][j]
    return 0.0
def gradient(i):
    try:
        gradient = (maxVal(i)-lagVal(i))/(timeToMax(i)-lagTime(i))
        return round(gradient, 1)
    except:
        return np.NaN
def areaUnderCurve(i):
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
               "AUC": areaUnderCurve}

#concatenate results from multiple excel file

def addColumn(method_name):
    features_df[method_name] = np.NaN
    col_index = features_df.columns.get_loc(method_name)
    for i in range(0,features_df.shape[0]):
        value = method_dict[method_name](i)
        features_df.iat[i, col_index] = value

##def plotTrace(i, plotGradient = True ):
##    hours_per_cycle = SEC_PER_CYCLE/3600
##    x_vals = [x*hours_per_cycle for x in range(1, len(data_array_2D[i])+1)] 
##    plt.plot(x_vals, data_array_2D[i])
##    if plotGradient:
##        g = features_df.loc[features_df.index[i], 'Gradient']
##        lagTm =
##        lagVal
##        if g != nan(plotGradient and features_df != NaN
##            plt.plot(x_vals, g(x_vals - 
##    plt.show()

df = getData(file)
df.columns = df.iloc[0]
df.drop(df.index[0] , inplace = True)
df = df[df.Description != 0]
print(df)

features_df, data_array_2D = splitNumbers(df)
for method_name in method_dict:
    addColumn(method_name)
print(features_df)

def cleanDesc(df):
    for i in range(0, len(df)-1, 2):
        df.iat[i,0] = df.iat[i,0] + " " +df.iat[i+1,0]
        df.iat[i+1,0] = df.iat[i,0] + " repeat" 
cleanDesc(features_df)
print(features_df)

#plotTrace(62)
    
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
