import component as c

class Additive(c.Component):
    def __init__(self, name, description, stock_conc, concs):
        c.Component.__init__(self, name, description)
        self.stock_conc = stock_conc
        self.concs = concs
    def get_stock_conc(self):
        return self.stock_conc
    def get_concs(self):
        return self.concs
    def get_numConcs(self):
        return len(self.concs)
