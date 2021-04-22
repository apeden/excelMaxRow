import rtquicdata_feat as rtq
import matplotlib.pyplot as plt

class Scatter(object):
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
                    plt.title("Effect of "+self.surf_name+ " on RTQuIC "+param+ ": "+ str(cyc//4)+ " hours ")
                    plt.xlabel('Surf conc')
                    plt.xlim(0.000001,1)
                    plt.xscale("log")
                    plt.ylabel(param)
                plt.legend()
                plt.show()
            del self.df
