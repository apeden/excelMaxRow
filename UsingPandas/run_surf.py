import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math
import seaborn as sns
import rtquicdata
import rtquicdata_feat
import rtquicdata_feat_65
import strip
import scatter
import plotsurf
import surf as sf


basepath = "RTQuIC_for_analysis/"
files = []

plt.subplots_adjust(wspace = 0.4)
plt.subplots_adjust(hspace = 0.6)

with os.scandir(basepath) as entries:
    for entry in entries:
        try:
            assert(entry.is_file())
            files.append(entry.name)
        except:
            print(entry.name, " is apparently a problem file.")
    for file in files:
        print(file)

f68 = sf.Surf("F-68", 1800, 8350, 80)
f127 = sf.Surf("F-127", 3600, 12600, 70)
f38 = sf.Surf("F-38", 900, 5000, 80)
f108 = sf.Surf("F-108", 3000, 14000, 80)
p84 = sf.Surf("P-84", 2250, 3750, 80)

##plotting strip plots
exp5 = [f127,files[20],[0, 0.0001, 0.0005, 0.001, 0.0011, 0.1]]
exp6 = [f68,files[21],[0, 0.0001, 0.0005, 0.001, 0.0011, 0.1]]
exp7 = [f127,files[22],[0, 0.000033, 0.000066, 0.0001, 0.00016, 0.00033, 0.0005]]
exp8 = [f68,files[23],[0, 0.0001, 0.0005, 0.001, 0.0011, 0.1]]


e = plotsurf.PlotSurf([p84,f108],files[24],[0.00001, 0.000033, 0.000066, 0.0001, 0.00033, 0.00066, 0.001], cut_cycs = [200], params = ["Lag Time"])
##0.00001 was actually zero, but I am plotting a log scale

e.plotSurf()
e.plotSurf("Surf conc mM")
e.plotSurf("Surf conc PO mM")
