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

import mimetypes
from openalea.core.path import path

from openalea.oalab.mimedata.qcodec import QMimeCodec
from openalea.oalab.mimedata.exception import MimeConversionError
from openalea.oalab.mimedata.builtin import BuiltinDataCodec 

def read_omero_image(raw_data, mimetype_in, mimetype_out):
    print "Omero Codec :",raw_data
    return None, {}


class IOmeroImageCodec(QMimeCodec):
    """
    'openalealab/omero' -> 'openalea/interface.IImage'
    """

    def _raw_data(self, mimedata, mimetype_in, mimetype_out):
        """
        'openalealab/omero' -> file id in Omero DB ?
        """
        return mimedata

    def quick_check(self, mimedata, mimetype_in, mimetype_out):
        return True

    def qtdecode(self, mimedata, mimetype_in, mimetype_out):
        raw_data = self._raw_data(mimedata, mimetype_in, mimetype_out)
        if raw_data is None:
            return None, {}
        else:
            return self.decode(raw_data, mimetype_in, mimetype_out)

    def decode(self, raw_data, mimetype_in, mimetype_out, **kwds):
        if mimetype_in == 'openalealab/omero':
            if mimetype_out == 'openalea/interface.IImage':
                return read_omero_image(raw_data, mimetype_in, mimetype_out)
        return None, {}
