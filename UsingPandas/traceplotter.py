import matplotlib.pyplot as plt

class TracePlotter():
    def __init__(self, df):
        self.df = df
        self.sec_per_cycle = 945.6
    def getArray(self, i, num_cycles):
        for_array_df = self.df.iloc[i,14:(num_cycles+14)]
        try:
            return for_array_df.to_numpy()
        except:
            print("Could not extract numeric data as array")
    def get_feat(self, feature, i):
        series = self.df.columns.get_loc(feature)
        return df.iat[i, series]
    def singlePlot(self, i, baseline = True, num_cycles = 400):
        """helper function for tracing plots"""
        data_array = self.getArray(i+1, num_cycles)
        hours_per_cycle = self.sec_per_cycle/3600
        x_vals = [x*hours_per_cycle for x in range(1, num_cycles+1)]
        print(x_vals[0:3])
        print(data_array[0:3])
        plt.plot(x_vals, data_array)      
        if baseline:
            plt.axhline(self.df["Base threshold"][i+1], color = "g", label = "Base threshold")
        plt.legend()
        plt.ylim(0,275000)
        plt.xlim(0,(100*(num_cycles/400)))
        plt.title(self.df["Seed"][i+1])           
        plt.ylabel("Flourescence Units")
        plt.xlabel("Time (hours)")

    def plot(self, start_end, baseline = True, num_cycles = 400):        
        for i in range(start_end[0]+1, start_end[1]+1):
            plt.subplot(3, 3, i+1)
            self.singlePlot(i)
        plt.show()
