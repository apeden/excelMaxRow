import pylab
from os import listdir
from RTQuicSheet import *

PATH_TO_FILES = "C:\\Users\\apeden\\OneDrive - University of Edinburgh\\excelMaxRow\\RTQuIC_for_analysis"
list_of_files = (listdir(PATH_TO_FILES))




"""takes a list of fluorescence values and adds to plot of
line graphs. x axis: 0 to 100 hours, y axis 0 to
260000 F Units"""

rows = (16,17,18,19)

def plot_rtquic(rows):
    x_values = []
    t = RTQuicSheet(PATH_TO_FILES+"\\"+list_of_files[0], "Results")
    t.set_row_list(14,rows[0])
    first_row = t.get_row_list()
    for i in range(1, len(first_row)+1):
        x_values.append((i*t.getSECONDS_PER_CYCLE())/3600)
    for row in rows:
        t.set_row_list(14,row)
        y_values = t.get_row_list()
        pylab.plot(x_values, y_values, label = str(row))
    pylab.title('RT-QuIC Fluorescence trace')
    pylab.xlabel('Hours')
    pylab.ylabel('Flourescence Units')
    pylab.legend()
    pylab.show()

plot_rtquic(rows)


