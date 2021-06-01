import additive as a
import buffermix as b
import substrate as su
import seed as se
import rtquicplate as r
import rtquicdata_feat as rd
import surf as sf
import os
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
  



basepath = "RTQuIC_for_analysis/"
files = []

with os.scandir(basepath) as entries:
    for entry in entries:
        try:
            assert(entry.is_file())
            files.append(entry.name)
        except:
            print(entry.name, " is apparently a problem file.")
    for file in files:
        print(file)

""" master mix components"""
##components and dilution factors

##Basic buffermixes, components and dilution factors
wilham = {"5XPBS":0.2, "2M NaCl":0.085, "0.1M EDTA":0.01, "1mM ThT":0.01}
salvadores = {"1M Tris-HCl pH7.4": 0.1, "1mM ThT": 0.005}

##Surfactants
surfactants = ["F-127", "F-68", "PE-P84", "F108"]
surfact_concs = [0, 0.0001, 0.0005, 0.001, 0.0011, 0.1]
surfact_concs2 = [0, 0.000033, 0.000066, 0.0001, 0.00016, 0.00033, 0.0005]
surfact_concs3 = [0.00001, 0.000033, 0.000066, 0.0001, 0.00033, 0.00066, 0.001]## first conc was actually zero, but I am plotting on a log scale

##substrate protein batches and dilution factors
sb_dil_fact = {"HaFLPrP 'M'":0.222,
               "abeta#1":0.1,
               "HS23NM 140111" :(0.1/0.52)}

##physical_parameters of various assays
rtquic =    {"plate_shaker":"BMG-floustar/omega","rpm":900, "config":"double orbital", "shake on":87, "shake off": 33,   "read every":15, "plate_type":96, "reaction_vol":100, "max_time": 100, "temp":42, "excite":435, "emit": 485}
abetaPMCA = {"plate_shaker":"Thermomixer",       "rpm":500, "config":"double orbital", "shake on":60, "shake off": 1740, "read every":60, "plate_type":96, "reaction_vol":100, "max_time": 200, "temp":22, "excite":435, "emit": 485}

##molecular_weights
mw = {"HamFLPrP": 22803.23,
      "abeta_42":4514.10,
      "abeta_40:":4329.86}

additives_S, buffermixes_S = [],[]

for surf in surfactants[:1]:
    buff = a.Additive(surf, surf, 0.05, surfact_concs)
    additives_S.append(buff)
additive_68 = [a.Additive("F-68", "F-68", 0.05, surfact_concs)]
additive_68_2 = [a.Additive("F-68", "F-68", 0.005, surfact_concs2)]
additive_P84_P108 = [a.Additive("P-84", "P-84", 0.005, surfact_concs3), a.Additive("F-108", "F-108", 0.005, surfact_concs3[1:])]

buffermixes_S.append(b.BufferMix("wilham","RTQuIC buffer mix", wilham)) 

seeds_M = [se.Seed("Water","Water as control", 9,2), se.Seed("MM1 (10^-3)", "MM1 sCJD seed diluted 1 in 1000", 3,2)]
seeds_M2 = [se.Seed("Water","Water as control", 3,2), se.Seed("MM1 (10^-3)", "MM1 sCJD seed diluted 1 in 1000", 3,2)]
substrates_M = [su.Substrate("HS23NM 140111", "Hu recPrP substrate M at codon 129", (0.1/0.52))]


##ex5 = RTQuICplate(substrates_M, buffermixes_S, additives_S, seeds_M, "9-12-20")
##ex6 = RTQuICplate(substrates_M, buffermixes_S, additive_68, seeds_M, "10-12-20")
##ex7 = RTQuICplate(substrates_M, buffermixes_S, additive_68_2, seeds_M, "18-02-21")
##ex8 = RTQuICplate(substrates_M, buffermixes_S, additive_68, seeds_M, "?-12-20")
ex9 = r.RTQuICplate(substrates_M, buffermixes_S, additive_P84_P108, seeds_M2, "?-5-21")
print(ex9)
ex9.get_mastermixes()
##print(ex10)
##ex10.get_mastermixes()

##set up datfram for adding data
df_blank = ex9.getPlate()
##obtain and analyse data
df_data = rd.RTQuICData_feat(files[24], numCycles = 200).get_df()
##print(df_data)
##join above two dataframas
df_labelled_data = pd.concat([df_blank, df_data], axis = 1)
##plot the data

params = ["Lag Time"]

surfs = sf.Surf("F-108", 3000, 14000, 80), sf.Surf("P-84", 2250, 3750, 80)
for surf in surfs:
    df_surf = df_labelled_data[df_labelled_data["Add"] == surf.get_name()]
    groups = df_surf.groupby("Seed")
    for param in params:
        for name, group in groups:
            x_, y_  = group["Conc"], group[param]
            print(x_)
            print(type(surf.get_mw()))
            print(type(x_))
            plt.scatter(x = x_.astype(float),y = y_, label = name)
            plt.title("Effect of "+ surf.get_name()+ \
    " on RTQuIC "+param)
            plt.xlabel("Conc %")            
            plt.xscale("log")
            plt.xlim(0.00001,0.001)
            plt.ylabel(param)
        plt.legend()
        plt.show()    
