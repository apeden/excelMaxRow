class Strip(object):
    def plotSurf(self):
        for cyc in self.cut_cycs:
            self.df = None
            print("file to analyse: ",self.file)
            myResults = RTQuICData_feat(self.file, numCycles =cyc)
            self.df = myResults.getData()
            self.addSurflabels()
            for param in self.params:          
                x_, y_  = 'Surf conc', param
                sns.stripplot(x = x_,y = y_,hue = "Seed", data = self.df)
                plt.title("Effect of "+self.surf_name+ " on RTQuIC "+param+ ": "+ str(cyc//4)+ " hours ")
                plt.legend([],[], frameon=False)
                plt.show()
            del self.df
