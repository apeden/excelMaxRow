import pandas as pd
import numpy as np

class RTQuICplate(object):
    row = ["A","B","C","D","E","F","G","H"]
    well_vol = 100
    seed_vol = 2
    additive_vol = 10
    noSeedVol = well_vol - seed_vol
    noSeedNoAddVol = noSeedVol - additive_vol
    def __init__(self, substrates, buffermixes, additives, seeds, date):
        self.substrates = substrates
        self.seeds = seeds 
        self.buffermixes = buffermixes
        self.additives = additives
        self.seeds = seeds
        self.date = date
        self.mastermixes = []
        ##mastermixes of each buffer comp will be split into submastermixes
        ##for each additive dilution
        self.subMastermixes = []
        self.plate = {} #it would be much better if this were a dataframe
        self.df_plate = pd.DataFrame(index=np.arange(96),columns = ["Well","Sub","Buff","Add","Conc","Seed","Seed vol"])
        self.setPlate()
        self.setMasterMixes()
        self.setSubMasterMixes()
    def getDate(self):
        return self.date       
    def setPlate(self):
        i = 0
        if i < 96:
            for sub in self.substrates:           
                for buff in self.buffermixes:
                    for add in self.additives:
                        for conc in add.get_concs():
                            for seed in self.seeds:
                                for r in range(seed.get_numReps()):
                                    self.df_plate.iloc[[i],[0]] = [RTQuICplate.row[i//12] + str((i%12)+1)]
                                    self.df_plate.iloc[[i],[1]] = sub.get_name()
                                    self.df_plate.iloc[[i],[2]] = buff.get_name()
                                    self.df_plate.iloc[[i],[3]] = add.get_name()
                                    self.df_plate.iloc[[i],[4]] = str(conc)
                                    self.df_plate.iloc[[i],[5]] = seed.get_name()
                                    self.df_plate.iloc[[i],[6]] = seed.get_seedVol()
                                    i += 1
        else:
            raise ValueError('full')
        
    def setMasterMixes(self, wasteFac = 1.2):
        ##numReps per mastermix
        numReps = numSeedReps = numAddConcs = 0
        for seed in self.seeds:
            numSeedReps += seed.get_numReps()
        for add in self.additives:
            numAddConcs += add.get_numConcs()
        numBuffs = len(self.buffermixes)
        numSubs = len(self.substrates)       
        numReps = numSeedReps * numAddConcs * numBuffs * numSubs
        for sub in self.substrates:
            for buffmix in self.buffermixes:
                mm_vols = \
                {"Tot vol mastermix (incl. add)": RTQuICplate.noSeedVol * numReps * wasteFac,
                 "Seed vol (ul/well)": RTQuICplate.seed_vol,
                 "MM vol w/o additive":RTQuICplate.noSeedNoAddVol * numReps * wasteFac}              
                mm_vols[sub.get_name()+" vol"] = sub.get_dilFac() * numReps *  wasteFac * RTQuICplate.well_vol
                water_vol = mm_vols["MM vol w/o additive"] - mm_vols[sub.get_name()+" vol"] 
                for buff_part, fact in buffmix.get_buffermix().items():
                    mm_vols[buff_part] = fact * numReps * 1.2 * RTQuICplate.well_vol
                    water_vol -= mm_vols[buff_part] 
                mm_vols["Water"] = water_vol 
                self.mastermixes.append(mm_vols)

    def setSubMasterMixes(self, wasteFac = 1.1):    
        numSeedReps = 0 ##numReps per submastermix
        for seed in self.seeds:
            numSeedReps += seed.get_numReps()
        vol_before_Additive = numSeedReps * wasteFac * RTQuICplate.noSeedNoAddVol
        for sub in self.substrates:
            for buffmix in self.buffermixes:
                for add in self.additives:
                    for conc in add.get_concs():
                        name = sub.get_name() + " " + buffmix.get_name() + \
" " + add.get_name() + " " + str(conc) +"%"  
                        submm = {"Name": name,
                                 "Stock conc (%)": str(add.get_stock_conc())+"%",
                                 "Subvol of MM" : vol_before_Additive,
                                 "Vol of add. stock": \
(conc*10/add.get_stock_conc()) * RTQuICplate.additive_vol * wasteFac * numSeedReps}
                        submm["Vol of water"] = (RTQuICplate.additive_vol * \
wasteFac * numSeedReps) - submm["Vol of add. stock"]
                        self.subMastermixes.append(submm)
    def get_description_str(self, component):
        string = ""
        for elem in component:
             string += " " + elem.get_description() +"/"
        return string
                        
    def get_mastermixes(self):
        print("Mastermixes and submastermixes\n==========\n")
        print("Mastermixes (vols in ul)\n==========\n")
        for mix in self.mastermixes:
            for key, value in mix.items():
                print(key + ": " + str(round(value,1)))
            print ("\n=========\n")
        print("Submastermixes (vols in ul)\n==========\n")
        for mix in self.subMastermixes:
            for key, value in mix.items():
                if type(value) != str:
                    print(key + ": " + str(round(value,1)))
                else:
                    print(key + ": " + value)
            print ("\n=========\n")
        return self.mastermixes, self.subMastermixes
    def getPlate(self):
        return self.df_plate
    def __str__(self):
        string = "Plate setup\n=======\n"
        string += "In this experiment on "+\
self.getDate() + " subtrate(s) ("+\
self.get_description_str(self.substrates) +") will be seeded with ("+\
self.get_description_str(self.seeds) +") seeds in ("+\
self.get_description_str(self.buffermixes) + ") buffer(s) in the prescence of (" +\
self.get_description_str(self.additives) + ").\n==========\n"+\
        self.df_plate.__str__()
        return string
