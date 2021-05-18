import numpy as np
import matplotlib.pyplot as plt
import rtquicdata_feat as rtq

class PlotSurf():
    def __init__(self, surf, file, concs,
                 params = ["Lag Time", "Max Val", "AUC"],
                 cut_cycs = [200, 400],
                 c = 3,
                 unseedReps = 9,
                 seedReps = 3):
        self.surf = surf
        self.file = file
        self.concs = concs
        self.cut_cycs = cut_cycs
        self.params = params
        self.unseedReps = unseedReps
        self.Reps = unseedReps + seedReps
        self.df = None
    def addSurflabels(self):
        self.df["Surf conc %"] = np.float32
        self.df["Seed"] = " " 
        surf_index = self.df.columns.get_loc("Surf conc %")
        seed_index = self.df.columns.get_loc("Seed")
        for i in range(self.Reps*len(self.concs)):
            self.df.iat[i, surf_index] = self.concs[i//12]
            if ((i == 0) or (i%self.Reps < self.unseedReps)):
                self.df.iat[i, seed_index] = "Unseeded"
            else:
                self.df.iat[i, seed_index] = "MM1 Seeded"
        self.df.drop(self.df.tail(25).index, inplace = True)
    def add_alt_surf_concs(self):
        self.df["Surf conc mM"] = \
10000 * (self.df["Surf conc %"]/self.surf.get_mw())
        self.df["Surf conc PO mM"] = \
10000 * (self.df["Surf conc %"]/self.surf.get_mw_hydrophobic())
    def plotSurf(self, xunits = 'Surf conc %'):
        for cyc in self.cut_cycs:
            self.df = None
            print("file to analyse: ",self.file)
            myResults = rtq.RTQuICData_feat(self.file, numCycles =cyc)
            self.df = myResults.getData()
            self.addSurflabels()
            self.add_alt_surf_concs()
            groups = self.df.groupby("Seed")
            for param in self.params:
                for name, group in groups:
                    x_, y_  = group[xunits], group[param]
                    plt.scatter(x = x_,y = y_, label = name)
                    plt.title("Effect of "+self.surf.get_name()+ \
" on RTQuIC "+param+ ": "+ str(cyc//4)+ " hours ")
                    plt.xlabel(xunits)
                    #plt.xlim(0.000001,1)
                    plt.xscale("log")
                    plt.ylabel(param)
                plt.legend()
                plt.show()
            del self.df
