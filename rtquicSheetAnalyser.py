from openpyxl import Workbook

from RTQuicSheet import *


class SheetAnalyser(object):
    row_num = 2 #row in destination excel file
    def __init__(self, raw_data, raw_data_sheet):
        self.raw_data = raw_data
        self.raw_data_sheet = raw_data_sheet
        self.result_list = []
        try:
            self.rtquic1 = RTQuicSheet(self.raw_data, self.raw_data_sheet)
        except:
            print("Could not generate RTQuicSheet object for analysing data")
        try:
            self.wb = Workbook()
        except:
            print("Could not generate destination workbook object")
        try:
            self.ws = self.wb.active
            print(self.ws)
        except:
            print("Could not generate active worksheet within distination workbook for " + self.raw_data)      
            raise AttributeError

    def set_result(self, row_start, row):
        self.rtquic1.set_row_list(row_start, row)
        #check a row_list was generated
        if len(self.rtquic1.get_row_list()) == 0:
            raise ValueError
            
        self.rtquic1.set_row_max()
        self.rtquic1.set_time_to_max()
        self.rtquic1.setLag()
        ##below time results (time to max and lag) in seconds    
        return (self.rtquic1.get_row_max(),
                self.rtquic1.get_time_to_max(),
                self.rtquic1.getLag())        
        

    def set_result_list(self, row_start, row):
        print("row number sent to set result list "+str(row))
        self.result_list = []
        SheetAnalyser.row_num += 1
        self.set_result(row_start, row)

        maxVal = self.rtquic1.get_row_max()
        maxHours = self.rtquic1.hours(self.rtquic1.get_time_to_max())
        lagHours = self.rtquic1.hours(self.rtquic1.getLag())
        #list of mean values with times in hours
        self.result_list = [maxVal,
                            maxHours,
                            lagHours]


    def row_filler(self):
        try:
            for i in range(len(self.result_list)):
                self.ws.cell(row = SheetAnalyser.row_num,
                        column = i + 1,
                        value = self.result_list[i])
        except:
            print("Could not fill a row")

    def data_label_row_filler(self):
        data_labels = ["Max Val", "Time to Max", "Lag time"] 

        #self.ws.cell(row = 1,
                     #column = 1,
                     #value = req 
        try:
            for i in range(len(data_labels)):
                self.ws.cell(row = 2,
                        column = i + 1,
                        value = data_labels[i])
        except:
            print("Could not fill title row")

    def save_wb(self):
        self.wb.save(self.__str__())

    def __str__(self):
        return ("Py_analysis_of_" + self.raw_data + ".xlsx")
        

class SheetAnalyserMeans(SheetAnalyser):

                
    def set_result_list(self, row_start, row):
        self.result_list = []
        SheetAnalyser.row_num += 2
        upper_row  = self.set_result(row_start, row)
        lower_row = self.set_result(row_start, row+1)
        mean_row = ()
        for i in range (len(upper_row)):
            mean_row = mean_row +(((upper_row[i]+ lower_row[i])/2),)

        maxVal = mean_row[0]
        maxHours = self.rtquic1.hours(mean_row[1])
        lagHours = self.rtquic1.hours(mean_row[2])
        #list of mean values with times in hours
        self.result_list = [maxVal,
                            maxHours,
                            lagHours]
        



try:
    t = SheetAnalyserMeans("RTQUIC_READ_18_022.xlsx","All_Cycles")
except AttributeError:
    print("Could not start SheetAnalyser. Problem with file or sheet names?")
t.data_label_row_filler()

def save_file(sheet_analyser):
    try:
        t.save_wb() 
    except PermissionError:
        print("Could not save to default result file")



for i in range(13,110,2):
    try:
        t.set_result_list(4,i)
    except ValueError:
        save_file(t)
        print("had to stop, but file still saved")
    t.row_filler()
save_file(t)
del t
