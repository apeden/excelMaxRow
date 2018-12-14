from openpyxl import Workbook
from os import listdir

PATH_TO_FILES = "C:\\Users\\apeden\\OneDrive - University of Edinburgh\\excelMaxRow\\RTQuIC_for_analysis"

list_of_files = (listdir(PATH_TO_FILES)) 



from RTQuicSheet import *


class SheetAnalyser(object):
     
    def __init__(self, raw_data, raw_data_sheet):
        self.row_num = 2 #row in destination excel file
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
        self.rtquic1.set_row_label(row)
        self.rtquic1.set_row_list(row_start, row)
        #check a row_list was generated
        if len(self.rtquic1.get_row_list()) == 0:
            raise ValueError   
        self.rtquic1.set_row_max()
        self.rtquic1.set_time_to_max()
        self.rtquic1.setLag()
        ##below time results (time to max and lag) in seconds    


    def get_result(self):
        return (self.rtquic1.get_row_label(),
                self.rtquic1.get_row_max(),
                self.rtquic1.get_time_to_max(),
                self.rtquic1.getLag())        
        

    def set_result_list(self, row_start, row):
        print("row number sent to set result list "+str(row))
        self.result_list = []
        self.row_num += 1
        self.set_result(row_start, row)
        Label = self.rtquic1.get_row_label()
        maxVal = self.rtquic1.get_row_max()
        maxHours = self.rtquic1.hours(self.rtquic1.get_time_to_max())
        lagHours = self.rtquic1.hours(self.rtquic1.getLag())
        #list of mean values with times in hours
        self.result_list = [Label,
                            maxVal,
                            maxHours,
                            lagHours]


    def row_filler(self):
        try:
            for i in range(len(self.result_list)):
                self.ws.cell(row = self.row_num,
                        column = i + 1,
                        value = self.result_list[i])
        except:
            print("Could not fill a row")

    def data_label_row_filler(self):
        data_labels = ["Label", "Max Val", "Time to Max", "Lag time"] 
        self.ws.cell(row =1, column =1, value = self.raw_data)
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
        source_file = self.raw_data.replace("-", "_")
        source_file = source_file.replace(" ", "_")
        return ("Analysis_of_"+ "string")
        

class SheetAnalyserMeans(SheetAnalyser):

                
    def set_result_list(self, row_start, row):
        self.result_list = []
        self.row_num += 2
        self.set_result(row_start, row)
        upper_row  = self.get_result()
        self.set_result(row_start, row+1)
        lower_row = self.get_result()
        mean_row = ()
        for i in range (1,len(upper_row)):
            mean_row = mean_row +(((upper_row[i]+ lower_row[i])/2),)
        Label = self.rtquic1.get_row_label()
        maxVal = mean_row[0]
        maxHours = self.rtquic1.hours(mean_row[1])
        lagHours = self.rtquic1.hours(mean_row[2])
        #list of mean values with times in hours
        self.result_list = [Label,
                            maxVal,
                            maxHours,
                            lagHours]
        

def analyse(workbook, sheet):
    try:
        t = SheetAnalyser(workbook, sheet)
    except AttributeError:
        print("Could not start SheetAnalyser. Problem with file or sheet names?")
    t.data_label_row_filler()
    for i in range(13,110):
        try:
            t.set_result_list(14,i)
        except ValueError:
            save_file(t)
            print("had to stop, but file still saved")
            return
        t.row_filler()
    save_file(t)
    del t


def save_file(sheet_analyser):
    try:
        sheet_analyser.save_wb() 
    except PermissionError:
        print("Could not save to default result file")

analyse(PATH_TO_FILES+"\\"+list_of_files[0], "Results")
