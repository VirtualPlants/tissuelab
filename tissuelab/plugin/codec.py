# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014-2016 INRIA - CIRAD - INRA
#
#       File author(s):
#           Guillaume Cerutti <guillaume.cerutti@inria.fr>
#           Guillaume Baty <guillaume.baty@inria.fr>-
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

from openalea.core.plugin.plugin import PluginDef
from openalea.oalab.mimedata.plugin import QMimeCodecPlugin


@PluginDef
class IOmeroImageCodecPlugin(QMimeCodecPlugin):
    implement = 'IQMimeCodec'
    qtdecode = [
        ('openalealab/omero', 'openalea/interface.IImage'),
    ]

    def __call__(self):
        from tissuelab.omero.mimedata import IOmeroImageCodec
        return IOmeroImageCodec