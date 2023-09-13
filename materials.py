

class Material(object):
    def __init__(self, diffuse = (1, 1, 1), specular = 1, ks = 0):
        self.diffuse = diffuse
        self.specular = specular
        self.ks = ks

