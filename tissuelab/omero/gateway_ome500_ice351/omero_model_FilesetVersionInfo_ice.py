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
# Generated from file `FilesetVersionInfo.ice'
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

if 'Details' not in _M_omero.model.__dict__:
    _M_omero.model._t_Details = IcePy.declareClass('::omero::model::Details')
    _M_omero.model._t_DetailsPrx = IcePy.declareProxy('::omero::model::Details')

if 'FilesetVersionInfo' not in _M_omero.model.__dict__:
    _M_omero.model.FilesetVersionInfo = Ice.createTempClass()
    class FilesetVersionInfo(_M_omero.model.IObject):
        def __init__(self, _id=None, _details=None, _loaded=False, _version=None, _bioformatsReader=None, _bioformatsVersion=None, _omeroVersion=None, _osArchitecture=None, _osName=None, _osVersion=None, _locale=None):
            if Ice.getType(self) == _M_omero.model.FilesetVersionInfo:
                raise RuntimeError('omero.model.FilesetVersionInfo is an abstract class')
            _M_omero.model.IObject.__init__(self, _id, _details, _loaded)
            self._version = _version
            self._bioformatsReader = _bioformatsReader
            self._bioformatsVersion = _bioformatsVersion
            self._omeroVersion = _omeroVersion
            self._osArchitecture = _osArchitecture
            self._osName = _osName
            self._osVersion = _osVersion
            self._locale = _locale

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::model::FilesetVersionInfo', '::omero::model::IObject')

        def ice_id(self, current=None):
            return '::omero::model::FilesetVersionInfo'

        def ice_staticId():
            return '::omero::model::FilesetVersionInfo'
        ice_staticId = staticmethod(ice_staticId)

        def getVersion(self, current=None):
            pass

        def setVersion(self, theVersion, current=None):
            pass

        def getBioformatsReader(self, current=None):
            pass

        def setBioformatsReader(self, theBioformatsReader, current=None):
            pass

        def getBioformatsVersion(self, current=None):
            pass

        def setBioformatsVersion(self, theBioformatsVersion, current=None):
            pass

        def getOmeroVersion(self, current=None):
            pass

        def setOmeroVersion(self, theOmeroVersion, current=None):
            pass

        def getOsArchitecture(self, current=None):
            pass

        def setOsArchitecture(self, theOsArchitecture, current=None):
            pass

        def getOsName(self, current=None):
            pass

        def setOsName(self, theOsName, current=None):
            pass

        def getOsVersion(self, current=None):
            pass

        def setOsVersion(self, theOsVersion, current=None):
            pass

        def getLocale(self, current=None):
            pass

        def setLocale(self, theLocale, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_omero.model._t_FilesetVersionInfo)

        __repr__ = __str__

    _M_omero.model.FilesetVersionInfoPrx = Ice.createTempClass()
    class FilesetVersionInfoPrx(_M_omero.model.IObjectPrx):

        def getVersion(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getVersion.invoke(self, ((), _ctx))

        def begin_getVersion(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getVersion.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getVersion.end(self, _r)

        def setVersion(self, theVersion, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setVersion.invoke(self, ((theVersion, ), _ctx))

        def begin_setVersion(self, theVersion, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setVersion.begin(self, ((theVersion, ), _response, _ex, _sent, _ctx))

        def end_setVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setVersion.end(self, _r)

        def getBioformatsReader(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getBioformatsReader.invoke(self, ((), _ctx))

        def begin_getBioformatsReader(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getBioformatsReader.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getBioformatsReader(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getBioformatsReader.end(self, _r)

        def setBioformatsReader(self, theBioformatsReader, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setBioformatsReader.invoke(self, ((theBioformatsReader, ), _ctx))

        def begin_setBioformatsReader(self, theBioformatsReader, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setBioformatsReader.begin(self, ((theBioformatsReader, ), _response, _ex, _sent, _ctx))

        def end_setBioformatsReader(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setBioformatsReader.end(self, _r)

        def getBioformatsVersion(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getBioformatsVersion.invoke(self, ((), _ctx))

        def begin_getBioformatsVersion(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getBioformatsVersion.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getBioformatsVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getBioformatsVersion.end(self, _r)

        def setBioformatsVersion(self, theBioformatsVersion, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setBioformatsVersion.invoke(self, ((theBioformatsVersion, ), _ctx))

        def begin_setBioformatsVersion(self, theBioformatsVersion, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setBioformatsVersion.begin(self, ((theBioformatsVersion, ), _response, _ex, _sent, _ctx))

        def end_setBioformatsVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setBioformatsVersion.end(self, _r)

        def getOmeroVersion(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOmeroVersion.invoke(self, ((), _ctx))

        def begin_getOmeroVersion(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOmeroVersion.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getOmeroVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getOmeroVersion.end(self, _r)

        def setOmeroVersion(self, theOmeroVersion, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOmeroVersion.invoke(self, ((theOmeroVersion, ), _ctx))

        def begin_setOmeroVersion(self, theOmeroVersion, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOmeroVersion.begin(self, ((theOmeroVersion, ), _response, _ex, _sent, _ctx))

        def end_setOmeroVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setOmeroVersion.end(self, _r)

        def getOsArchitecture(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOsArchitecture.invoke(self, ((), _ctx))

        def begin_getOsArchitecture(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOsArchitecture.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getOsArchitecture(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getOsArchitecture.end(self, _r)

        def setOsArchitecture(self, theOsArchitecture, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOsArchitecture.invoke(self, ((theOsArchitecture, ), _ctx))

        def begin_setOsArchitecture(self, theOsArchitecture, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOsArchitecture.begin(self, ((theOsArchitecture, ), _response, _ex, _sent, _ctx))

        def end_setOsArchitecture(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setOsArchitecture.end(self, _r)

        def getOsName(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOsName.invoke(self, ((), _ctx))

        def begin_getOsName(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOsName.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getOsName(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getOsName.end(self, _r)

        def setOsName(self, theOsName, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOsName.invoke(self, ((theOsName, ), _ctx))

        def begin_setOsName(self, theOsName, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOsName.begin(self, ((theOsName, ), _response, _ex, _sent, _ctx))

        def end_setOsName(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setOsName.end(self, _r)

        def getOsVersion(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOsVersion.invoke(self, ((), _ctx))

        def begin_getOsVersion(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getOsVersion.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getOsVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getOsVersion.end(self, _r)

        def setOsVersion(self, theOsVersion, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOsVersion.invoke(self, ((theOsVersion, ), _ctx))

        def begin_setOsVersion(self, theOsVersion, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setOsVersion.begin(self, ((theOsVersion, ), _response, _ex, _sent, _ctx))

        def end_setOsVersion(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setOsVersion.end(self, _r)

        def getLocale(self, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getLocale.invoke(self, ((), _ctx))

        def begin_getLocale(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_getLocale.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getLocale(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_getLocale.end(self, _r)

        def setLocale(self, theLocale, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setLocale.invoke(self, ((theLocale, ), _ctx))

        def begin_setLocale(self, theLocale, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfo._op_setLocale.begin(self, ((theLocale, ), _response, _ex, _sent, _ctx))

        def end_setLocale(self, _r):
            return _M_omero.model.FilesetVersionInfo._op_setLocale.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.model.FilesetVersionInfoPrx.ice_checkedCast(proxy, '::omero::model::FilesetVersionInfo', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.model.FilesetVersionInfoPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.model._t_FilesetVersionInfoPrx = IcePy.defineProxy('::omero::model::FilesetVersionInfo', FilesetVersionInfoPrx)

    _M_omero.model._t_FilesetVersionInfo = IcePy.declareClass('::omero::model::FilesetVersionInfo')

    _M_omero.model._t_FilesetVersionInfo = IcePy.defineClass('::omero::model::FilesetVersionInfo', FilesetVersionInfo, -1, (), True, False, _M_omero.model._t_IObject, (), (
        ('_version', (), _M_omero._t_RInt, False, 0),
        ('_bioformatsReader', (), _M_omero._t_RString, False, 0),
        ('_bioformatsVersion', (), _M_omero._t_RString, False, 0),
        ('_omeroVersion', (), _M_omero._t_RString, False, 0),
        ('_osArchitecture', (), _M_omero._t_RString, False, 0),
        ('_osName', (), _M_omero._t_RString, False, 0),
        ('_osVersion', (), _M_omero._t_RString, False, 0),
        ('_locale', (), _M_omero._t_RString, False, 0)
    ))
    FilesetVersionInfo._ice_type = _M_omero.model._t_FilesetVersionInfo

    FilesetVersionInfo._op_getVersion = IcePy.Operation('getVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    FilesetVersionInfo._op_setVersion = IcePy.Operation('setVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    FilesetVersionInfo._op_getBioformatsReader = IcePy.Operation('getBioformatsReader', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setBioformatsReader = IcePy.Operation('setBioformatsReader', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    FilesetVersionInfo._op_getBioformatsVersion = IcePy.Operation('getBioformatsVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setBioformatsVersion = IcePy.Operation('setBioformatsVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    FilesetVersionInfo._op_getOmeroVersion = IcePy.Operation('getOmeroVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setOmeroVersion = IcePy.Operation('setOmeroVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    FilesetVersionInfo._op_getOsArchitecture = IcePy.Operation('getOsArchitecture', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setOsArchitecture = IcePy.Operation('setOsArchitecture', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    FilesetVersionInfo._op_getOsName = IcePy.Operation('getOsName', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setOsName = IcePy.Operation('setOsName', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    FilesetVersionInfo._op_getOsVersion = IcePy.Operation('getOsVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setOsVersion = IcePy.Operation('setOsVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    FilesetVersionInfo._op_getLocale = IcePy.Operation('getLocale', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    FilesetVersionInfo._op_setLocale = IcePy.Operation('setLocale', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())

    _M_omero.model.FilesetVersionInfo = FilesetVersionInfo
    del FilesetVersionInfo

    _M_omero.model.FilesetVersionInfoPrx = FilesetVersionInfoPrx
    del FilesetVersionInfoPrx

# End of module omero.model

__name__ = 'omero'

# End of module omero
