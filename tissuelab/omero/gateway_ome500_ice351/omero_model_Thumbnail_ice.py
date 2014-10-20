# **********************************************************************
#
# Copyright (c) 2003-2013 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
#
# Ice version 3.5.1
#
# <auto-generated>
#
# Generated from file `Thumbnail.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy
import omero_model_IObject_ice
import omero_RTypes_ice
import omero_System_ice
import omero_Collections_ice

# Included module omero
_M_omero = Ice.openModule('omero')

# Included module omero.model
_M_omero.model = Ice.openModule('omero.model')

# Included module Ice
_M_Ice = Ice.openModule('Ice')

# Included module omero.sys
_M_omero.sys = Ice.openModule('omero.sys')

# Included module omero.api
_M_omero.api = Ice.openModule('omero.api')

# Start of module omero
__name__ = 'omero'

# Start of module omero.model
__name__ = 'omero.model'

if 'Pixels' not in _M_omero.model.__dict__:
    _M_omero.model._t_Pixels = IcePy.declareClass('::omero::model::Pixels')
    _M_omero.model._t_PixelsPrx = IcePy.declareProxy('::omero::model::Pixels')

if 'Details' not in _M_omero.model.__dict__:
    _M_omero.model._t_Details = IcePy.declareClass('::omero::model::Details')
    _M_omero.model._t_DetailsPrx = IcePy.declareProxy('::omero::model::Details')

if 'Thumbnail' not in _M_omero.model.__dict__:
    _M_omero.model.Thumbnail = Ice.createTempClass()
    class Thumbnail(_M_omero.model.IObject):
        def __init__(self, _id=None, _details=None, _loaded=False, _version=None, _pixels=None, _mimeType=None, _sizeX=None, _sizeY=None, _ref=None):
            if Ice.getType(self) == _M_omero.model.Thumbnail:
                raise RuntimeError('omero.model.Thumbnail is an abstract class')
            _M_omero.model.IObject.__init__(self, _id, _details, _loaded)
            self._version = _version
            self._pixels = _pixels
            self._mimeType = _mimeType
            self._sizeX = _sizeX
            self._sizeY = _sizeY
            self._ref = _ref

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::model::IObject', '::omero::model::Thumbnail')

        def ice_id(self, current=None):
            return '::omero::model::Thumbnail'

        def ice_staticId():
            return '::omero::model::Thumbnail'
        ice_staticId = staticmethod(ice_staticId)

        def getVersion(self, current=None):
            pass

        def setVersion(self, theVersion, current=None):
            pass

        def getPixels(self, current=None):
            pass

        def setPixels(self, thePixels, current=None):
            pass

        def getMimeType(self, current=None):
            pass

        def setMimeType(self, theMimeType, current=None):
            pass

        def getSizeX(self, current=None):
            pass

        def setSizeX(self, theSizeX, current=None):
            pass

        def getSizeY(self, current=None):
            pass

        def setSizeY(self, theSizeY, current=None):
            pass

        def getRef(self, current=None):
            pass

        def setRef(self, theRef, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_omero.model._t_Thumbnail)

        __repr__ = __str__

    _M_omero.model.ThumbnailPrx = Ice.createTempClass()
    class ThumbnailPrx(_M_omero.model.IObjectPrx):

        def getVersion(self, _ctx=None):
            return _M_omero.model.Thumbnail._op_getVersion.invoke(self, ((), _ctx))

        def begin_getVersion(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_getVersion.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getVersion(self, _r):
            return _M_omero.model.Thumbnail._op_getVersion.end(self, _r)

        def setVersion(self, theVersion, _ctx=None):
            return _M_omero.model.Thumbnail._op_setVersion.invoke(self, ((theVersion, ), _ctx))

        def begin_setVersion(self, theVersion, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_setVersion.begin(self, ((theVersion, ), _response, _ex, _sent, _ctx))

        def end_setVersion(self, _r):
            return _M_omero.model.Thumbnail._op_setVersion.end(self, _r)

        def getPixels(self, _ctx=None):
            return _M_omero.model.Thumbnail._op_getPixels.invoke(self, ((), _ctx))

        def begin_getPixels(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_getPixels.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getPixels(self, _r):
            return _M_omero.model.Thumbnail._op_getPixels.end(self, _r)

        def setPixels(self, thePixels, _ctx=None):
            return _M_omero.model.Thumbnail._op_setPixels.invoke(self, ((thePixels, ), _ctx))

        def begin_setPixels(self, thePixels, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_setPixels.begin(self, ((thePixels, ), _response, _ex, _sent, _ctx))

        def end_setPixels(self, _r):
            return _M_omero.model.Thumbnail._op_setPixels.end(self, _r)

        def getMimeType(self, _ctx=None):
            return _M_omero.model.Thumbnail._op_getMimeType.invoke(self, ((), _ctx))

        def begin_getMimeType(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_getMimeType.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getMimeType(self, _r):
            return _M_omero.model.Thumbnail._op_getMimeType.end(self, _r)

        def setMimeType(self, theMimeType, _ctx=None):
            return _M_omero.model.Thumbnail._op_setMimeType.invoke(self, ((theMimeType, ), _ctx))

        def begin_setMimeType(self, theMimeType, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_setMimeType.begin(self, ((theMimeType, ), _response, _ex, _sent, _ctx))

        def end_setMimeType(self, _r):
            return _M_omero.model.Thumbnail._op_setMimeType.end(self, _r)

        def getSizeX(self, _ctx=None):
            return _M_omero.model.Thumbnail._op_getSizeX.invoke(self, ((), _ctx))

        def begin_getSizeX(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_getSizeX.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getSizeX(self, _r):
            return _M_omero.model.Thumbnail._op_getSizeX.end(self, _r)

        def setSizeX(self, theSizeX, _ctx=None):
            return _M_omero.model.Thumbnail._op_setSizeX.invoke(self, ((theSizeX, ), _ctx))

        def begin_setSizeX(self, theSizeX, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_setSizeX.begin(self, ((theSizeX, ), _response, _ex, _sent, _ctx))

        def end_setSizeX(self, _r):
            return _M_omero.model.Thumbnail._op_setSizeX.end(self, _r)

        def getSizeY(self, _ctx=None):
            return _M_omero.model.Thumbnail._op_getSizeY.invoke(self, ((), _ctx))

        def begin_getSizeY(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_getSizeY.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getSizeY(self, _r):
            return _M_omero.model.Thumbnail._op_getSizeY.end(self, _r)

        def setSizeY(self, theSizeY, _ctx=None):
            return _M_omero.model.Thumbnail._op_setSizeY.invoke(self, ((theSizeY, ), _ctx))

        def begin_setSizeY(self, theSizeY, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_setSizeY.begin(self, ((theSizeY, ), _response, _ex, _sent, _ctx))

        def end_setSizeY(self, _r):
            return _M_omero.model.Thumbnail._op_setSizeY.end(self, _r)

        def getRef(self, _ctx=None):
            return _M_omero.model.Thumbnail._op_getRef.invoke(self, ((), _ctx))

        def begin_getRef(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_getRef.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getRef(self, _r):
            return _M_omero.model.Thumbnail._op_getRef.end(self, _r)

        def setRef(self, theRef, _ctx=None):
            return _M_omero.model.Thumbnail._op_setRef.invoke(self, ((theRef, ), _ctx))

        def begin_setRef(self, theRef, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.Thumbnail._op_setRef.begin(self, ((theRef, ), _response, _ex, _sent, _ctx))

        def end_setRef(self, _r):
            return _M_omero.model.Thumbnail._op_setRef.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.model.ThumbnailPrx.ice_checkedCast(proxy, '::omero::model::Thumbnail', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.model.ThumbnailPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.model._t_ThumbnailPrx = IcePy.defineProxy('::omero::model::Thumbnail', ThumbnailPrx)

    _M_omero.model._t_Thumbnail = IcePy.declareClass('::omero::model::Thumbnail')

    _M_omero.model._t_Thumbnail = IcePy.defineClass('::omero::model::Thumbnail', Thumbnail, -1, (), True, False, _M_omero.model._t_IObject, (), (
        ('_version', (), _M_omero._t_RInt, False, 0),
        ('_pixels', (), _M_omero.model._t_Pixels, False, 0),
        ('_mimeType', (), _M_omero._t_RString, False, 0),
        ('_sizeX', (), _M_omero._t_RInt, False, 0),
        ('_sizeY', (), _M_omero._t_RInt, False, 0),
        ('_ref', (), _M_omero._t_RString, False, 0)
    ))
    Thumbnail._ice_type = _M_omero.model._t_Thumbnail

    Thumbnail._op_getVersion = IcePy.Operation('getVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    Thumbnail._op_setVersion = IcePy.Operation('setVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    Thumbnail._op_getPixels = IcePy.Operation('getPixels', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero.model._t_Pixels, False, 0), ())
    Thumbnail._op_setPixels = IcePy.Operation('setPixels', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero.model._t_Pixels, False, 0),), (), None, ())
    Thumbnail._op_getMimeType = IcePy.Operation('getMimeType', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    Thumbnail._op_setMimeType = IcePy.Operation('setMimeType', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    Thumbnail._op_getSizeX = IcePy.Operation('getSizeX', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    Thumbnail._op_setSizeX = IcePy.Operation('setSizeX', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    Thumbnail._op_getSizeY = IcePy.Operation('getSizeY', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    Thumbnail._op_setSizeY = IcePy.Operation('setSizeY', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    Thumbnail._op_getRef = IcePy.Operation('getRef', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    Thumbnail._op_setRef = IcePy.Operation('setRef', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())

    _M_omero.model.Thumbnail = Thumbnail
    del Thumbnail

    _M_omero.model.ThumbnailPrx = ThumbnailPrx
    del ThumbnailPrx

# End of module omero.model

__name__ = 'omero'

# End of module omero