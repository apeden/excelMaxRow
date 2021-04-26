class Surf(object):
    def __init__(self, name, mwh, mw, percentPO):
        self.name = name
        self.mw_hydrophobic = mwh
        self.mw = mw
        self.percentPO = percentPO
    def get_name(self):
        return self.name
    def get_mw_hydrophobic(self):
        return self.mw_hydrophobic
    def get_mw(self):
        return self.mw
    def get_percentPO(self):
        return self.percentPO
        
