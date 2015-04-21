# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

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
        return self[:, :, z]

    def getId(self):
        return 0

    def getPrimaryPixels(self):
        return self
