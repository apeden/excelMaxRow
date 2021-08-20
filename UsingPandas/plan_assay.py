import additive as a
import buffermix as b
import substrate as su
import seed as se

import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

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
surfact_concs4 = [0.00001, 0.000033, 0.0001, 0.00033, 0.001]## first conc was actually zero, but I am plotting on a log scale

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

##additives
additives_S, buffermixes_S = [],[]

for surf in surfactants[:1]:
    buff = a.Additive(surf, surf, 0.05, surfact_concs)
    additives_S.append(buff)
additive_68 = [a.Additive("F-68", "F-68", 0.05, surfact_concs)]
additive_68_2 = [a.Additive("F-68", "F-68", 0.005, surfact_concs2)]
additive_P84_P108 = [a.Additive("P-84", "P-84", 0.005, surfact_concs3), a.Additive("F-108", "F-108", 0.005, surfact_concs3[1:])]
additive_Tetronic_F127 = [a.Additive("Tetronic", "Tetronic", 0.005, surfact_concs3), a.Additive("F-127", "F-127", 0.005, surfact_concs3[1:])]
additive_blank =[a.Additive("Blank", "Blank", 1, [0])]
additive_F127 = [a.Additive("F-127", "F-127", 0.005, surfact_concs4)]

buffermixes_S.append(b.BufferMix("wilham","RTQuIC buffer mix", wilham)) 

seeds_M = [se.Seed("Water","Water as control", 9,2), se.Seed("MM1 (10^-3)", "MM1 sCJD seed diluted 1 in 1000", 3,2)]
seeds_M2 = [se.Seed("Water","Water as control", 3,2), se.Seed("MM1 (10^-3)", "MM1 sCJD seed diluted 1 in 1000", 3,2)]
seeds_M3 = [se.Seed("Water","Water as control", 2,2), se.Seed("MM1(1e-3)", "MM1 sCJD seed diluted 1 in 1000", 2,2)]
seeds_65 = [se.Seed("SD31 FC", "(1e-3) Ex#21.051 diluted 1 in 1000", 2, 2),
            se.Seed("SD31 CB", "(1e-3) Ex#21.054 diluted 1 in 1000", 2, 2),
            se.Seed("MM", "Ex#15.317(10^-3) MM diluted 1 in 1000", 2, 2),
            se.Seed("MV", "Ex#15.320(10^-3), MV diluted 1 in 1000", 2, 2),
            se.Seed("VV", "Ex#15.323(10^-3),VV diluted 1 in 1000", 2, 2),
            se.Seed("MM1", "(10^-3), MM1 sCJD seed diluted 1 in 1000", 2, 2),
            se.Seed("VV2", "(10^-3), VV2 sCJD seed diluted 1 in 1000", 2, 2)]
                 
substrates_M = [su.Substrate("HS23NM 140111", "Hu recPrP substrate M at codon 129", (0.1/0.52))]
substrates_65 = [su.Substrate("HaFLPrP 'M'", "Hu recPrP substrate M at codon 129", 0.222)]


##========= DRAW UP PLAN FOR PLATE =============================================

import rtquicplate as r

##ex5 = RTQuICplate(substrates_M, buffermixes_S, additives_S, seeds_M, "9-12-20")
##ex6 = RTQuICplate(substrates_M, buffermixes_S, additive_68, seeds_M, "10-12-20")
##ex7 = RTQuICplate(substrates_M, buffermixes_S, additive_68_2, seeds_M, "18-02-21")
##ex8 = RTQuICplate(substrates_M, buffermixes_S, additive_68, seeds_M, "?-12-20")
##ex9 = r.RTQuICplate(substrates_M, buffermixes_S, additive_P84_P108, seeds_M2, "?-5-21")
##ex10 = r.RTQuICplate(substrates_M, buffermixes_S, additive_Tetronic_F127, seeds_M2, "?-8-21")
##ex11 = r.RTQuICplate(substrates_65, buffermixes_S, additive_blank, seeds_65, "?-8-21")
##ex12 = r.RTQuICplate(substrates_65, buffermixes_S, additive_F127, seeds_M3, "?-8-21")
ex12a = r.RTQuICplate(substrates_65, buffermixes_S, additive_Tetronic_F127, seeds_M3, "?-8-21")

ex12a.get_mastermixes()
plan_df = ex12a.getPlate()
plan_df["Seeded"] = True
plan_df.loc[plan_df["Seed"] == "Water", 'Seeded'] = False
plan_df = plan_df.iloc[0:52,:]

##print(df)
##print("\n======\nF-127 concentrations")
##print(df.pivot(index = "Well row", columns = "Well col", values = "Conc"))
##print("\n======\nSeed scheme")
##print(df.pivot(index = "Well row", columns = "Well col", values = "Seed"))

##========= GET DATA FOR ABOVE PLATE ============================================

import rtquicdata_feat as d 

data = d.RTQuICData_feat("RTQUIC_21_004.xlsx", numCycles = 200)
data_df = data.getData()
print(data_df["Lag Time"])

##====== MERGE TWO DFS INTO A MASTER FRAME =======================================================

mf = plan_df.join(data_df)
print(mf[["Add","Conc","Seed","Seeded","Lag Time"]])


##=====ISOLATE RESULTS OF JUST ONE POLOXAMER============================
mf_T90R4 = mf.iloc[:,0:28]
print(mf_T90R4[["Add","Conc","Seed","Seeded","Lag Time"]])

##=======PLOT LAG TIME VERSUS CONC=======================



##groups = self.df.groupby("Seed")
##for name, group in groups:
##    x_, y_  = group[xunits], group["Lag Time"]
##    plt.scatter(x = x_,y = y_, label = name)
##    plt.title("Effect of "+self.surf.get_name()+ \
##" on RTQuIC "+param+ ": "+ str(cyc//4)+ " hours ")
##                    plt.xlabel(xunits)
##                    #plt.xlim(0.000001,1)
##                    plt.xscale("log")
##                    plt.ylabel(param)
##                plt.legend()
##                plt.show()

