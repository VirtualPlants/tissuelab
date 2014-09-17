
from openalea.image.all import SpatialImage

class AdapterSpatialImageToImage5D(SpatialImage):

    def __init__(self, image):
        SpatialImage.__init__(image)

    def getSizeZ(self):
        return self.shape[2]

    def getSizeC(self):
        return 1

    def getSizeT(self):
        return 1

    def getPlane(self, z, c, t):
        return self[:,:,z]

    def getId(self):
        return 0

    def getPrimaryPixels(self):
        return self

