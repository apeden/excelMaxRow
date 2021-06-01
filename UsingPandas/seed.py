import component as c

class Seed (c.Component):
    def __init__(self, name, description, numReps, seedVol):
        c.Component.__init__(self, name,description)
        self.numReps = numReps
        self.seedVol = seedVol
    def get_numReps(self):
        return self.numReps
    def get_seedVol(self):
        return self.seedVol  
