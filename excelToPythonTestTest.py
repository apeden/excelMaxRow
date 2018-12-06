from openpyxl import load_workbook

from excelToPythonTest import *


rtquic1 = RTQuicSheet("RTQUIC_18_019.xlsx",'All_Cycles')
print(rtquic1)
rtquic1.set_row_list(4,31)
rtquic1.set_row_max()
print(rtquic1.get_row_max())

##getting lag time data
rtquic1.setLag()
print(rtquic1.getLag())
#in hours
lagHours = rtquic1.hours(rtquic1.getLag)
print(lagHours())

##getting max time data
rtquic1.set_time_to_max()
print(rtquic1.get_time_to_max())
#in hours
maxHours = rtquic1.hours(rtquic1.get_time_to_max)
print(maxHours())
