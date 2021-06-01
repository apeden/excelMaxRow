import numpy as np
import matplotlib.pyplot as plt
import rtquicdata_feat as rtq

class PlotSurf():
    def __init__(self, surfs, file, concs,
                 params = ["Lag Time", "Max Val", "AUC"],
                 cut_cycs = [200, 400],
                 c = 3,
                 unseedReps = 9,
                 seedReps = 3):
        self.surfs = surfs # now a list of surfs
        self.file = file
        self.concs = concs
        self.cut_cycs = cut_cycs
        self.params = params
        self.unseedReps = unseedReps
        self.Reps = unseedReps + seedReps
        self.df = None
    def addSurflabels(self):
        """Labels data according to surfactant concentrations
        and whether reaction was seeded or unseeded"""
        self.df["Surf"] = " "    
        self.df["Surf conc %"] = np.float32
        self.df["Surf conc mM"] = np.float32
        self.df["Surf conc PO mM"] = np.float32
        self.df["Seed"] = " " 
        surf_name_index = self.df.columns.get_loc("Surf")
        surf_conc_index = self.df.columns.get_loc("Surf conc %")
        surf_mM_index = self.df.columns.get_loc("Surf conc mM")
        surf_POmM_index = self.df.columns.get_loc("Surf conc PO mM")  
        seed_index = self.df.columns.get_loc("Seed")
        expt_set = self.Reps*len(self.concs)
        for i in range(len(self.surfs)):
            for j in range(expt_set):
                self.df.iat[(i*expt_set)+j, surf_name_index] = \
self.surfs[i].get_name()
                self.df.iat[(i*expt_set)+j, surf_conc_index] = \
self.concs[j//12]
                self.df.iat[(i*expt_set)+j, surf_mM_index] = \
10000 * (self.concs[j//12]/self.surf.get_mw())
                self.df.iat[(i*expt_set)+j, surf_POmM_index] = \
10000 * (self.concs[j//12]/self.surf.get_mw_hydrophobic())
                if ((j == 0) or (j%self.Reps < self.unseedReps)):
                    self.df.iat[(i*expt_set)+j, seed_index] = "Unseeded"
                else:
                    self.df.iat[(i*expt_set)+j, seed_index] = "MM1 Seeded"
        self.df.drop(self.df.tail(25).index, inplace = True)
        
    def plotSurf(self, xunits = 'Surf conc %'):
        """takes data from a file, makes dataframe of features,
    data in dataframe then labelled prior to being plotted"""
        for cyc in self.cut_cycs:
            self.df = None
            print("file to analyse: ",self.file)
            myResults = rtq.RTQuICData_feat(self.file, numCycles =cyc)
            self.df = myResults.getData()
            self.addSurflabels()
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
