from openpyxl import Workbook

from excelToPythonTest import *


class SheetAnalyser(object):
    row_num = 2 #class variable
    def __init__(self, result_file_name, raw_data, raw_data_sheet):
        self.result_file_name = result_file_name
        self.raw_data = raw_data
        self.raw_data_sheet = raw_data_sheet
        self.rtquic1 = None
        self.setRTQuic()
        try:
            self.wb = Workbook()
        except:
            print("Could not generate workbook")
        try:
            self.ws = self.wb.active
        except:
            print("Could not access active worksheet")
        
        self.result_list = []
        
    def setRTQuic(self):
        try:
            self.rtquic1 = RTQuicSheet(self.raw_data, self.raw_data_sheet)
            print(type(self.rtquic1))
        except:
            print("Could not generate RTQuicSheet object")

    def set_result_list(self, row_start, row):
        print("row number sent to set result list "+str(row))
        
        self.result_list = []
        SheetAnalyser.row_num += 1
        self.rtquic1.set_row_list(row_start, row)
        self.rtquic1.set_row_max()
        self.rtquic1.set_time_to_max()
        self.rtquic1.setLag()

        maxHours = self.rtquic1.hours(self.rtquic1.get_time_to_max)
        lagHours = self.rtquic1.hours(self.rtquic1.getLag)
        
        
        self.result_list = [self.rtquic1.get_row_max(),
                                maxHours(),
                                lagHours()]


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
        try:
            for i in range(len(data_labels)):
                self.ws.cell(row = 2,
                        column = i + 1,
                        value = self.result_list[i])
        except:
            print("Could not fill title row")

    def save_wb(self):
        self.wb.save(self.result_file_name)
        

t = SheetAnalyser("testbook.xlsx","RTQUIC_18_019.xlsx",'All_Cycles')
t.data_label_row_filler()
for i in range(13,110):
    t.set_result_list(4,i)
    t.row_filler()
t.save_wb()
del t
