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

__all__ = ['IImage5DViewer', 'IOmeroImage', 'ISpatialImage', 'IAdapter']

from openalea.oalab.legacy.catalog.interface import IInterface


class IAdapter(IInterface):
    name = 'IAdapter'


class IImage5DViewer(IInterface):
    name = 'IImage5DViewer'

    def setData(self, data):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class ISpatialImage(IInterface):

    """
    Associate meta data to np.ndarray

    Constructor

    .. code-block:: python

        def __new__ (cls, input_array, voxelsize = None,
                 vdim = None, info = None, dtype = None, **kwargs) :

    Properties :

        * resolution
        * real_shape
    """
    name = 'ISpatialImage'

    def invert_z_axis(self):
        """
        invert allong 'Z' axis
        """

    def clone(self, data):
        """Clone the current image metadata
        on the given data.

        .. warning:: vdim is defined according to self.voxelsize and data.shape

        :Parameters:
         - `data` - (array)

        :Returns Type: |SpatialImage|
        """

    @classmethod
    def valid_array(cls, array_like):
        pass


class IOmeroImage(ISpatialImage):
    name = 'IOmeroImage'

    def getSizeZ(self):
        pass

    def getSizeC(self):
        pass

    def getSizeT(self):
        pass

    def getPlane(self, z, c, t):
        pass


class IImage5D(ISpatialImage):
    name = 'IImage5D'

    sizex = int
    sizey = int
    sizez = int

    sizec = int
    sizet = int

    def extract(self, x=None, y=None, z=None, c=None, t=None):
        pass

    def pixels(self):
        pass


class IDocumentDbConnection(IInterface):

    """
    Interface used to connect to a document DB
    """
    name = "IDocumentDbConnection"
