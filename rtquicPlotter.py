import pylab as plt
from RTQuicSheet import *


"""takes a list of fluorescence values and adds to plot of
line graphs. x axis: 0 to 100 hours, y axis 0 to
260000 F Units"""


def getResults(file):
    testSheet = RTQuicSheet("RTQuIC Review/"+file, "Results")
    testData = RTQuICData(testSheet.getSheet(), 13, 9,
                      label_col = 1, numRows = 96)
    plateData = testData.getData()
    data_labels = testData.getLabels()
    cycle_time = testData.getSecPerCyc()/3600 # in hour
    return plateData, data_labels, cycle_time

def display(title, xlabel, ylabel, base = None):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if not base == None:
        plt.axhline(base)
    plt.legend()
    plt.show()


title= 'RT-QuIC Fluorescence trace'
xlabel='Hours'
ylabel='Flourescence Units'

def plotRange(file, rowRange, title, xlabel, ylabel):
    x_values, y_values  = [],[]
    plateData, data_labels, cycle_time\
               = getResults(file)
    for i in range(len(plateData[0])):
        time_hours = (i+1)*cycle_time
        x_values.append(time_hours)    
    for i in rowRange:
        label, row_data = data_labels[i], plateData[i]   
        y_values = row_data
        plt.plot(x_values, y_values, label = str(label))
    display(title, xlabel, ylabel)


def plotOne(file, row, title, xlabel, ylabel, base = False):
    x_values, y_values  = [],[]
    plateData, data_labels, cycle_time\
               = getResults(file)
    for i in range(len(plateData[row])):
        time_hours = (i+1)*cycle_time
        x_values.append(time_hours)    
    label, row_data = data_labels[row], plateData[row]   
    y_values = row_data
    plt.plot(x_values, y_values, label = str(label))
    if base:
        display(title, xlabel, ylabel, base = row_data[2])
    else:
        display(title, xlabel, ylabel)



file = "Experimental plan RTQUIC19 004 AHP 65+study cases  37 38 40 39 41 42 01 02.xlsx"
plotRange(file, (6,14,20, 43), title, xlabel, ylabel)
#plotOne(file, 1, title, xlabel, ylabel, True)

