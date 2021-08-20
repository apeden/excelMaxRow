import pandas as pd

class RTQuICData(object):
    basepath = "RTQuIC_for_analysis/"
    sheet_name = "All Cycles"
    skiprows = 10,
    usecols='A,N:OW'
    
    def __init__(self, excelfile, ):
        self.file = excelfile
        self.file_name = excelfile.__str__()
        self.df = None
        self.setData()
        
    def get_df(self):
        return self.df
    def setData(self):
        """If possible, return raw dataframe using excel file sheet as input"""
        ##try:
        self.df = pd.read_excel(self.basepath + self.file,
                           self.sheet_name,
                           self.skiprows)
##        except FileNotFoundError:
##            print("In getData, File ",self.file," not found")
##            self.df = None
##        except ValueError:
##            print("Check sheet name")
##            self.df = None
##        except:
##            print("In getData, Couldn't make dataframe using file ",self.file)
##            self.df = None
    def getData(self):
        return self.df
    def __str__(self):
        string  = "\n=============\n"   
        string += self.file_name +"\n=============\n"+ self.df.__str__()
        return string
