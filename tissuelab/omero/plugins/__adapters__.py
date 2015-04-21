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

__all__ = []

from openalea.oalab.legacy.catalog.factories import ObjectFactory


AdapterSpatialImageToImage5D = ObjectFactory(name='AdapterSpatialImageToImage5D',
                                             description="A sample to show adapter mechanism",
                                             category="test",
                                             interfaces=["IAdapter", "ISpatialImage", "IOmeroImage"],
                                             nodemodule="openalea.omero.adapters",
                                             nodeclass="AdapterSpatialImageToImage5D",
                                             adapter_inputs=['ISpatialImage'],
                                             adapter_outputs=['IOmeroImage'],
                                             )
__all__.append('AdapterSpatialImageToImage5D')
