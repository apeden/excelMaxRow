import component as c

class BufferMix(c.Component):
    def __init__(self, name, description, buffermix):
        c.Component.__init__(self, name, description)
        self.buffermix  = buffermix
    def get_buffermix(self):
        return self.buffermix
