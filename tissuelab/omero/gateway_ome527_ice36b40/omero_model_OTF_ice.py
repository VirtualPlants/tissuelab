# -*- coding: utf-8 -*-
# **********************************************************************
#
# Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
#
# Ice version 3.6.3
#
# <auto-generated>
#
# Generated from file `OTF.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy
import omero_model_IObject_ice
import omero_RTypes_ice
import omero_model_RTypes_ice
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

if 'PixelsType' not in _M_omero.model.__dict__:
    _M_omero.model._t_PixelsType = IcePy.declareClass('::omero::model::PixelsType')
    _M_omero.model._t_PixelsTypePrx = IcePy.declareProxy('::omero::model::PixelsType')

if 'FilterSet' not in _M_omero.model.__dict__:
    _M_omero.model._t_FilterSet = IcePy.declareClass('::omero::model::FilterSet')
    _M_omero.model._t_FilterSetPrx = IcePy.declareProxy('::omero::model::FilterSet')

if 'Objective' not in _M_omero.model.__dict__:
    _M_omero.model._t_Objective = IcePy.declareClass('::omero::model::Objective')
    _M_omero.model._t_ObjectivePrx = IcePy.declareProxy('::omero::model::Objective')

if 'Instrument' not in _M_omero.model.__dict__:
    _M_omero.model._t_Instrument = IcePy.declareClass('::omero::model::Instrument')
    _M_omero.model._t_InstrumentPrx = IcePy.declareProxy('::omero::model::Instrument')

if 'Details' not in _M_omero.model.__dict__:
    _M_omero.model._t_Details = IcePy.declareClass('::omero::model::Details')
    _M_omero.model._t_DetailsPrx = IcePy.declareProxy('::omero::model::Details')

if 'OTF' not in _M_omero.model.__dict__:
    _M_omero.model.OTF = Ice.createTempClass()
    class OTF(_M_omero.model.IObject):
        def __init__(self, _id=None, _details=None, _loaded=False, _version=None, _sizeX=None, _sizeY=None, _opticalAxisAveraged=None, _pixelsType=None, _path=None, _filterSet=None, _objective=None, _instrument=None):
            if Ice.getType(self) == _M_omero.model.OTF:
                raise RuntimeError('omero.model.OTF is an abstract class')
            _M_omero.model.IObject.__init__(self, _id, _details, _loaded)
            self._version = _version
            self._sizeX = _sizeX
            self._sizeY = _sizeY
            self._opticalAxisAveraged = _opticalAxisAveraged
            self._pixelsType = _pixelsType
            self._path = _path
            self._filterSet = _filterSet
            self._objective = _objective
            self._instrument = _instrument

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::model::IObject', '::omero::model::OTF')

        def ice_id(self, current=None):
            return '::omero::model::OTF'

        def ice_staticId():
            return '::omero::model::OTF'
        ice_staticId = staticmethod(ice_staticId)

        def getVersion(self, current=None):
            pass

        def setVersion(self, theVersion, current=None):
            pass

        def getSizeX(self, current=None):
            pass

        def setSizeX(self, theSizeX, current=None):
            pass

        def getSizeY(self, current=None):
            pass

        def setSizeY(self, theSizeY, current=None):
            pass

        def getOpticalAxisAveraged(self, current=None):
            pass

        def setOpticalAxisAveraged(self, theOpticalAxisAveraged, current=None):
            pass

        def getPixelsType(self, current=None):
            pass

        def setPixelsType(self, thePixelsType, current=None):
            pass

        def getPath(self, current=None):
            pass

        def setPath(self, thePath, current=None):
            pass

        def getFilterSet(self, current=None):
            pass

        def setFilterSet(self, theFilterSet, current=None):
            pass

        def getObjective(self, current=None):
            pass

        def setObjective(self, theObjective, current=None):
            pass

        def getInstrument(self, current=None):
            pass

        def setInstrument(self, theInstrument, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_omero.model._t_OTF)

        __repr__ = __str__

    _M_omero.model.OTFPrx = Ice.createTempClass()
    class OTFPrx(_M_omero.model.IObjectPrx):

        def getVersion(self, _ctx=None):
            return _M_omero.model.OTF._op_getVersion.invoke(self, ((), _ctx))

        def begin_getVersion(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getVersion.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getVersion(self, _r):
            return _M_omero.model.OTF._op_getVersion.end(self, _r)

        def setVersion(self, theVersion, _ctx=None):
            return _M_omero.model.OTF._op_setVersion.invoke(self, ((theVersion, ), _ctx))

        def begin_setVersion(self, theVersion, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setVersion.begin(self, ((theVersion, ), _response, _ex, _sent, _ctx))

        def end_setVersion(self, _r):
            return _M_omero.model.OTF._op_setVersion.end(self, _r)

        def getSizeX(self, _ctx=None):
            return _M_omero.model.OTF._op_getSizeX.invoke(self, ((), _ctx))

        def begin_getSizeX(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getSizeX.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getSizeX(self, _r):
            return _M_omero.model.OTF._op_getSizeX.end(self, _r)

        def setSizeX(self, theSizeX, _ctx=None):
            return _M_omero.model.OTF._op_setSizeX.invoke(self, ((theSizeX, ), _ctx))

        def begin_setSizeX(self, theSizeX, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setSizeX.begin(self, ((theSizeX, ), _response, _ex, _sent, _ctx))

        def end_setSizeX(self, _r):
            return _M_omero.model.OTF._op_setSizeX.end(self, _r)

        def getSizeY(self, _ctx=None):
            return _M_omero.model.OTF._op_getSizeY.invoke(self, ((), _ctx))

        def begin_getSizeY(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getSizeY.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getSizeY(self, _r):
            return _M_omero.model.OTF._op_getSizeY.end(self, _r)

        def setSizeY(self, theSizeY, _ctx=None):
            return _M_omero.model.OTF._op_setSizeY.invoke(self, ((theSizeY, ), _ctx))

        def begin_setSizeY(self, theSizeY, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setSizeY.begin(self, ((theSizeY, ), _response, _ex, _sent, _ctx))

        def end_setSizeY(self, _r):
            return _M_omero.model.OTF._op_setSizeY.end(self, _r)

        def getOpticalAxisAveraged(self, _ctx=None):
            return _M_omero.model.OTF._op_getOpticalAxisAveraged.invoke(self, ((), _ctx))

        def begin_getOpticalAxisAveraged(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getOpticalAxisAveraged.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getOpticalAxisAveraged(self, _r):
            return _M_omero.model.OTF._op_getOpticalAxisAveraged.end(self, _r)

        def setOpticalAxisAveraged(self, theOpticalAxisAveraged, _ctx=None):
            return _M_omero.model.OTF._op_setOpticalAxisAveraged.invoke(self, ((theOpticalAxisAveraged, ), _ctx))

        def begin_setOpticalAxisAveraged(self, theOpticalAxisAveraged, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setOpticalAxisAveraged.begin(self, ((theOpticalAxisAveraged, ), _response, _ex, _sent, _ctx))

        def end_setOpticalAxisAveraged(self, _r):
            return _M_omero.model.OTF._op_setOpticalAxisAveraged.end(self, _r)

        def getPixelsType(self, _ctx=None):
            return _M_omero.model.OTF._op_getPixelsType.invoke(self, ((), _ctx))

        def begin_getPixelsType(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getPixelsType.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getPixelsType(self, _r):
            return _M_omero.model.OTF._op_getPixelsType.end(self, _r)

        def setPixelsType(self, thePixelsType, _ctx=None):
            return _M_omero.model.OTF._op_setPixelsType.invoke(self, ((thePixelsType, ), _ctx))

        def begin_setPixelsType(self, thePixelsType, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setPixelsType.begin(self, ((thePixelsType, ), _response, _ex, _sent, _ctx))

        def end_setPixelsType(self, _r):
            return _M_omero.model.OTF._op_setPixelsType.end(self, _r)

        def getPath(self, _ctx=None):
            return _M_omero.model.OTF._op_getPath.invoke(self, ((), _ctx))

        def begin_getPath(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getPath.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getPath(self, _r):
            return _M_omero.model.OTF._op_getPath.end(self, _r)

        def setPath(self, thePath, _ctx=None):
            return _M_omero.model.OTF._op_setPath.invoke(self, ((thePath, ), _ctx))

        def begin_setPath(self, thePath, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setPath.begin(self, ((thePath, ), _response, _ex, _sent, _ctx))

        def end_setPath(self, _r):
            return _M_omero.model.OTF._op_setPath.end(self, _r)

        def getFilterSet(self, _ctx=None):
            return _M_omero.model.OTF._op_getFilterSet.invoke(self, ((), _ctx))

        def begin_getFilterSet(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getFilterSet.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getFilterSet(self, _r):
            return _M_omero.model.OTF._op_getFilterSet.end(self, _r)

        def setFilterSet(self, theFilterSet, _ctx=None):
            return _M_omero.model.OTF._op_setFilterSet.invoke(self, ((theFilterSet, ), _ctx))

        def begin_setFilterSet(self, theFilterSet, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setFilterSet.begin(self, ((theFilterSet, ), _response, _ex, _sent, _ctx))

        def end_setFilterSet(self, _r):
            return _M_omero.model.OTF._op_setFilterSet.end(self, _r)

        def getObjective(self, _ctx=None):
            return _M_omero.model.OTF._op_getObjective.invoke(self, ((), _ctx))

        def begin_getObjective(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getObjective.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getObjective(self, _r):
            return _M_omero.model.OTF._op_getObjective.end(self, _r)

        def setObjective(self, theObjective, _ctx=None):
            return _M_omero.model.OTF._op_setObjective.invoke(self, ((theObjective, ), _ctx))

        def begin_setObjective(self, theObjective, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setObjective.begin(self, ((theObjective, ), _response, _ex, _sent, _ctx))

        def end_setObjective(self, _r):
            return _M_omero.model.OTF._op_setObjective.end(self, _r)

        def getInstrument(self, _ctx=None):
            return _M_omero.model.OTF._op_getInstrument.invoke(self, ((), _ctx))

        def begin_getInstrument(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_getInstrument.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getInstrument(self, _r):
            return _M_omero.model.OTF._op_getInstrument.end(self, _r)

        def setInstrument(self, theInstrument, _ctx=None):
            return _M_omero.model.OTF._op_setInstrument.invoke(self, ((theInstrument, ), _ctx))

        def begin_setInstrument(self, theInstrument, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.model.OTF._op_setInstrument.begin(self, ((theInstrument, ), _response, _ex, _sent, _ctx))

        def end_setInstrument(self, _r):
            return _M_omero.model.OTF._op_setInstrument.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.model.OTFPrx.ice_checkedCast(proxy, '::omero::model::OTF', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.model.OTFPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::omero::model::OTF'
        ice_staticId = staticmethod(ice_staticId)

    _M_omero.model._t_OTFPrx = IcePy.defineProxy('::omero::model::OTF', OTFPrx)

    _M_omero.model._t_OTF = IcePy.declareClass('::omero::model::OTF')

    _M_omero.model._t_OTF = IcePy.defineClass('::omero::model::OTF', OTF, -1, (), True, False, _M_omero.model._t_IObject, (), (
        ('_version', (), _M_omero._t_RInt, False, 0),
        ('_sizeX', (), _M_omero._t_RInt, False, 0),
        ('_sizeY', (), _M_omero._t_RInt, False, 0),
        ('_opticalAxisAveraged', (), _M_omero._t_RBool, False, 0),
        ('_pixelsType', (), _M_omero.model._t_PixelsType, False, 0),
        ('_path', (), _M_omero._t_RString, False, 0),
        ('_filterSet', (), _M_omero.model._t_FilterSet, False, 0),
        ('_objective', (), _M_omero.model._t_Objective, False, 0),
        ('_instrument', (), _M_omero.model._t_Instrument, False, 0)
    ))
    OTF._ice_type = _M_omero.model._t_OTF

    OTF._op_getVersion = IcePy.Operation('getVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    OTF._op_setVersion = IcePy.Operation('setVersion', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    OTF._op_getSizeX = IcePy.Operation('getSizeX', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    OTF._op_setSizeX = IcePy.Operation('setSizeX', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    OTF._op_getSizeY = IcePy.Operation('getSizeY', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RInt, False, 0), ())
    OTF._op_setSizeY = IcePy.Operation('setSizeY', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RInt, False, 0),), (), None, ())
    OTF._op_getOpticalAxisAveraged = IcePy.Operation('getOpticalAxisAveraged', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RBool, False, 0), ())
    OTF._op_setOpticalAxisAveraged = IcePy.Operation('setOpticalAxisAveraged', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RBool, False, 0),), (), None, ())
    OTF._op_getPixelsType = IcePy.Operation('getPixelsType', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero.model._t_PixelsType, False, 0), ())
    OTF._op_setPixelsType = IcePy.Operation('setPixelsType', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero.model._t_PixelsType, False, 0),), (), None, ())
    OTF._op_getPath = IcePy.Operation('getPath', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero._t_RString, False, 0), ())
    OTF._op_setPath = IcePy.Operation('setPath', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero._t_RString, False, 0),), (), None, ())
    OTF._op_getFilterSet = IcePy.Operation('getFilterSet', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero.model._t_FilterSet, False, 0), ())
    OTF._op_setFilterSet = IcePy.Operation('setFilterSet', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero.model._t_FilterSet, False, 0),), (), None, ())
    OTF._op_getObjective = IcePy.Operation('getObjective', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero.model._t_Objective, False, 0), ())
    OTF._op_setObjective = IcePy.Operation('setObjective', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero.model._t_Objective, False, 0),), (), None, ())
    OTF._op_getInstrument = IcePy.Operation('getInstrument', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (), (), ((), _M_omero.model._t_Instrument, False, 0), ())
    OTF._op_setInstrument = IcePy.Operation('setInstrument', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_omero.model._t_Instrument, False, 0),), (), None, ())

    _M_omero.model.OTF = OTF
    del OTF

    _M_omero.model.OTFPrx = OTFPrx
    del OTFPrx

# End of module omero.model

__name__ = 'omero'

# End of module omero