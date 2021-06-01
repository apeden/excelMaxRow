import component as c

class Substrate(c.Component):
    def __init__(self, name, description, dilFac):
        c.Component.__init__(self, name, description)
        self.dilFac = dilFac
    def get_dilFac(self):
        return self.dilFac
