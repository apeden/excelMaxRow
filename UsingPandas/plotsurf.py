import numpy as np
import matplotlib as pyplot

class PlotSurf():
    def __init__(self, surf, file, concs):
        self.surf = surf
        self.file = file
        self.concs = concs
        self.cut_cycs = [200, 400]
        self.params = ["Lag Time", "Max Val", "AUC"]
        self.df = None
    def addSurflabels(self):
        self.df["Surf conc %"] = np.float32
        self.df["Seed"] = " " 
        surf_index = self.df.columns.get_loc("Surf conc %")
        seed_index = self.df.columns.get_loc("Seed")
        for i in range(12*len(self.concs)):
            self.df.iat[i, surf_index] = self.concs[i//12]
            if ((i == 0) or (i%12 < 9)):
                self.df.iat[i, seed_index] = "Unseeded"
            else:
                self.df.iat[i, seed_index] = "MM1 Seeded"
        self.df.drop(self.df.tail(25).index, inplace = True)
    def add_alt_surf_concs(self):
        self.df["Surf conc mM"] = \
10000 * (self.df["Surf conc %"]/self.surf_get_mw())
        self.df["Surf conc PO mM"] = \
10000 * (self.df["Surf conc %"]/self.surf_get_mw_hydrophobic())
    def plotSurf(self):
        for cyc in self.cut_cycs:
            self.df = None
            print("file to analyse: ",self.file)
            myResults = rtq.RTQuICData_feat(self.file, numCycles =cyc)
            self.df = myResults.getData()
            self.addSurflabels()
            groups = self.df.groupby("Seed")
            for param in self.params:
                for name, group in groups:
                    x_, y_  = group['Surf conc'], group[param]
                    plt.scatter(x = x_,y = y_, label = name)
                    plt.title("Effect of "+self.surf_name+ \
" on RTQuIC "+param+ ": "+ str(cyc//4)+ " hours ")
                    plt.xlabel('Surf conc')
                    plt.xlim(0.000001,1)
                    plt.xscale("log")
                    plt.ylabel(param)
                plt.legend()
                plt.show()
            del self.df
