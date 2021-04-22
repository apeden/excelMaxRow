import scatter as sc

class PlotSurf(sc.Scatter):
    def __init__(self, surf_name, file, concs):
        self.surf_name = surf_name
        self.file = file
        self.concs = concs
        self.cut_cycs = [200, 400]
        self.params = ["Lag Time", "Max Val", "AUC"]
        self.df = None
    def addSurflabels(self):
        self.df["Surf conc"] = np.float32
        self.df["Seed"] = " " 
        surf_index = self.df.columns.get_loc("Surf conc")
        seed_index = self.df.columns.get_loc("Seed")
        for i in range(12*len(self.concs)):
            self.df.iat[i, surf_index] = self.concs[i//12]
            if ((i == 0) or (i%12 < 9)):
                self.df.iat[i, seed_index] = "Unseeded"
            else:
                self.df.iat[i, seed_index] = "MM1 Seeded"
        self.df.drop(self.df.tail(25).index, inplace = True)
