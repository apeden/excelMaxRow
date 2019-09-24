from openpyxl import load_workbook as load

class RTQuicSheet(object):
    def __init__(self, workbook_filepath, sheet_name):   
        self.wb = None
        self.sheet = None
        self.workbook_filepath = workbook_filepath
        self.sheet_name = sheet_name
        try:
            ##set workbook as file object
            self.wb = load(self.workbook_filepath,
                                    data_only = True)
        except IOError:
            self.wb = None
            print("Could not load: "+ self.workbook_filepath)
        try:
            ##get sheet as file object
            self.sheet = self.wb[self.sheet_name] 
        except:
            print("Sheet not found "
                  + self.sheet_name + " in workbook "
                  + self.workbook_filepath)
    def getSheet(self):
        return self.sheet
    def __str__(self):
        if self.sheet != None:
            return "Contains: " + self.workbook_path + ", "
            + self.sheet_name
        else:
            return "Empty"
