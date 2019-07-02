import pylab
from RTQuicSheet import *


"""takes a list of fluorescence values and adds to plot of
line graphs. x axis: 0 to 100 hours, y axis 0 to
260000 F Units"""

def plotRTQuIC(file):
    x_values, y_values  = [],[]
    testSheet = RTQuicSheet("RTQuIC Review/"+file, "Results")
    testData = RTQuICData(testSheet.getSheet(), 13, 9,
                      label_col = 1, numRows = 96)
    plateData = testData.getData()
    for i in range(len(plateData)):
        label, row_data = data_labels[i], data[i]
        a = RowAnalyser(row_data, label)
        cycle_time = testData.getSecPerCyc()/3600 # in hour
        for i in range(len(row_data)):
            time_hours = (i+1)*cycle_time
            x_values.append(time_hours)
            y_values.append(row_data[i])
            pylab.plot(x_values, y_values, label = str(row))
        pylab.title('RT-QuIC Fluorescence trace')
        pylab.xlabel('Hours')
        pylab.ylabel('Flourescence Units')
        pylab.legend()
        pylab.show()

plotRTQuIC("Experimental plan RTQUIC19 004 AHP 65+study cases  37 38 40 39 41 42 01 02.xlsx")


