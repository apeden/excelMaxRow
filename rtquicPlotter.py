import pylab as plt
from RTQuicSheet import *


"""takes a list of fluorescence values and adds to plot of
line graphs. x axis: 0 to 100 hours, y axis 0 to
260000 F Units"""

def plotRange(file, start_row, end_row):
    x_values, y_values  = [],[]
    testSheet = RTQuicSheet("RTQuIC Review/"+file, "Results")
    testData = RTQuICData(testSheet.getSheet(), 13, 9,
                      label_col = 1, numRows = 96)
    plateData = testData.getData()
    data_labels = testData.getLabels()
    cycle_time = testData.getSecPerCyc()/3600 # in hour
    for i in range(len(plateData[0])):
        time_hours = (i+1)*cycle_time
        x_values.append(time_hours)    
    for i in range(start_row, end_row):
        label, row_data = data_labels[i], plateData[i]   
        y_values = row_data
        plt.plot(x_values, y_values, label = str(label))
    plt.title('RT-QuIC Fluorescence trace')
    plt.xlabel('Hours')
    plt.ylabel('Flourescence Units')
    plt.axhline(100000)
    plt.legend()
    plt.show()


file = "Experimental plan RTQUIC19 004 AHP 65+study cases  37 38 40 39 41 42 01 02.xlsx"
plotRange(file, start_row = 0, end_row = 96)


