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
# Generated from file `System.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy
import omero_RTypes_ice
import Ice_BuiltinSequences_ice

# Included module omero
_M_omero = Ice.openModule('omero')

# Included module omero.model
_M_omero.model = Ice.openModule('omero.model')

# Included module Ice
_M_Ice = Ice.openModule('Ice')

# Start of module omero
__name__ = 'omero'

# Start of module omero.sys
_M_omero.sys = Ice.openModule('omero.sys')
__name__ = 'omero.sys'

if '_t_LongList' not in _M_omero.sys.__dict__:
    _M_omero.sys._t_LongList = IcePy.defineSequence('::omero::sys::LongList', (), IcePy._t_long)

if '_t_IntList' not in _M_omero.sys.__dict__:
    _M_omero.sys._t_IntList = IcePy.defineSequence('::omero::sys::IntList', (), IcePy._t_int)

if '_t_CountMap' not in _M_omero.sys.__dict__:
    _M_omero.sys._t_CountMap = IcePy.defineDictionary('::omero::sys::CountMap', (), IcePy._t_long, IcePy._t_long)

if '_t_ParamMap' not in _M_omero.sys.__dict__:
    _M_omero.sys._t_ParamMap = IcePy.defineDictionary('::omero::sys::ParamMap', (), IcePy._t_string, _M_omero._t_RType)

if '_t_IdByteMap' not in _M_omero.sys.__dict__:
    _M_omero.sys._t_IdByteMap = IcePy.defineDictionary('::omero::sys::IdByteMap', (), IcePy._t_long, _M_Ice._t_ByteSeq)

if 'EventContext' not in _M_omero.sys.__dict__:
    _M_omero.sys.EventContext = Ice.createTempClass()
    class EventContext(Ice.Object):
        '''Maps the ome.system.EventContext interface. Represents the
information known by the server security system about the
current user login.'''
        def __init__(self, shareId=0, sessionId=0, sessionUuid='', userId=0, userName='', groupId=0, groupName='', isAdmin=False, eventId=0, eventType='', memberOfGroups=None, leaderOfGroups=None, groupPermissions=None):
            self.shareId = shareId
            self.sessionId = sessionId
            self.sessionUuid = sessionUuid
            self.userId = userId
            self.userName = userName
            self.groupId = groupId
            self.groupName = groupName
            self.isAdmin = isAdmin
            self.eventId = eventId
            self.eventType = eventType
            self.memberOfGroups = memberOfGroups
            self.leaderOfGroups = leaderOfGroups
            self.groupPermissions = groupPermissions

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::sys::EventContext')

        def ice_id(self, current=None):
            return '::omero::sys::EventContext'

        def ice_staticId():
            return '::omero::sys::EventContext'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_omero.sys._t_EventContext)

        __repr__ = __str__

    _M_omero.sys.EventContextPrx = Ice.createTempClass()
    class EventContextPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.sys.EventContextPrx.ice_checkedCast(proxy, '::omero::sys::EventContext', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.sys.EventContextPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.sys._t_EventContextPrx = IcePy.defineProxy('::omero::sys::EventContext', EventContextPrx)

    _M_omero.sys._t_EventContext = IcePy.declareClass('::omero::sys::EventContext')

    _M_omero.sys._t_EventContext = IcePy.defineClass('::omero::sys::EventContext', EventContext, -1, (), False, False, None, (), (
        ('shareId', (), IcePy._t_long, False, 0),
        ('sessionId', (), IcePy._t_long, False, 0),
        ('sessionUuid', (), IcePy._t_string, False, 0),
        ('userId', (), IcePy._t_long, False, 0),
        ('userName', (), IcePy._t_string, False, 0),
        ('groupId', (), IcePy._t_long, False, 0),
        ('groupName', (), IcePy._t_string, False, 0),
        ('isAdmin', (), IcePy._t_bool, False, 0),
        ('eventId', (), IcePy._t_long, False, 0),
        ('eventType', (), IcePy._t_string, False, 0),
        ('memberOfGroups', (), _M_omero.sys._t_LongList, False, 0),
        ('leaderOfGroups', (), _M_omero.sys._t_LongList, False, 0),
        ('groupPermissions', (), _M_omero.model._t_Permissions, False, 0)
    ))
    EventContext._ice_type = _M_omero.sys._t_EventContext

    _M_omero.sys.EventContext = EventContext
    del EventContext

    _M_omero.sys.EventContextPrx = EventContextPrx
    del EventContextPrx

if 'Filter' not in _M_omero.sys.__dict__:
    _M_omero.sys.Filter = Ice.createTempClass()
    class Filter(Ice.Object):
        '''Provides common filters which MAY be applied to a
query. Check the documentation for the particular
method for more information on how these values will
be interpreted as well as default values if they
are missing. In general they are intended to mean:

unique        := similar to SQL's "DISTINCT" keyword

ownerId       := (some) objects queried should belong
to this user

groupId       := (some) objects queried should belong
to this group

preferOwner   := true implies if if ownerId and groupId
are both defined, use only ownerId

offset/limit  := represent a page which should be loaded
Note: servers may choose to impose a
maximum limit.

start/endTime := (some) objects queried shoud have been
created and/or modified within time span.'''
        def __init__(self, unique=None, ownerId=None, groupId=None, offset=None, limit=None, startTime=None, endTime=None):
            self.unique = unique
            self.ownerId = ownerId
            self.groupId = groupId
            self.offset = offset
            self.limit = limit
            self.startTime = startTime
            self.endTime = endTime

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::sys::Filter')

        def ice_id(self, current=None):
            return '::omero::sys::Filter'

        def ice_staticId():
            return '::omero::sys::Filter'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_omero.sys._t_Filter)

        __repr__ = __str__

    _M_omero.sys.FilterPrx = Ice.createTempClass()
    class FilterPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.sys.FilterPrx.ice_checkedCast(proxy, '::omero::sys::Filter', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.sys.FilterPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.sys._t_FilterPrx = IcePy.defineProxy('::omero::sys::Filter', FilterPrx)

    _M_omero.sys._t_Filter = IcePy.declareClass('::omero::sys::Filter')

    _M_omero.sys._t_Filter = IcePy.defineClass('::omero::sys::Filter', Filter, -1, (), False, False, None, (), (
        ('unique', (), _M_omero._t_RBool, False, 0),
        ('ownerId', (), _M_omero._t_RLong, False, 0),
        ('groupId', (), _M_omero._t_RLong, False, 0),
        ('offset', (), _M_omero._t_RInt, False, 0),
        ('limit', (), _M_omero._t_RInt, False, 0),
        ('startTime', (), _M_omero._t_RTime, False, 0),
        ('endTime', (), _M_omero._t_RTime, False, 0)
    ))
    Filter._ice_type = _M_omero.sys._t_Filter

    _M_omero.sys.Filter = Filter
    del Filter

    _M_omero.sys.FilterPrx = FilterPrx
    del FilterPrx

if 'Options' not in _M_omero.sys.__dict__:
    _M_omero.sys.Options = Ice.createTempClass()
    class Options(Ice.Object):
        '''Similar to Filter, provides common options which MAY be
applied on a given method. Check each interface's
documentation for more details.

leaves        := whether or not graph leaves (usually images)
should be loaded

orphan        := whether or not orphaned objects (e.g. datasets
not in a project) should be loaded

acquisition...:= whether or not acquisitionData (objectives, etc.)
should be loaded'''
        def __init__(self, leaves=None, orphan=None, acquisitionData=None):
            self.leaves = leaves
            self.orphan = orphan
            self.acquisitionData = acquisitionData

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::sys::Options')

        def ice_id(self, current=None):
            return '::omero::sys::Options'

        def ice_staticId():
            return '::omero::sys::Options'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_omero.sys._t_Options)

        __repr__ = __str__

    _M_omero.sys.OptionsPrx = Ice.createTempClass()
    class OptionsPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.sys.OptionsPrx.ice_checkedCast(proxy, '::omero::sys::Options', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.sys.OptionsPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.sys._t_OptionsPrx = IcePy.defineProxy('::omero::sys::Options', OptionsPrx)

    _M_omero.sys._t_Options = IcePy.declareClass('::omero::sys::Options')

    _M_omero.sys._t_Options = IcePy.defineClass('::omero::sys::Options', Options, -1, (), False, False, None, (), (
        ('leaves', (), _M_omero._t_RBool, False, 0),
        ('orphan', (), _M_omero._t_RBool, False, 0),
        ('acquisitionData', (), _M_omero._t_RBool, False, 0)
    ))
    Options._ice_type = _M_omero.sys._t_Options

    _M_omero.sys.Options = Options
    del Options

    _M_omero.sys.OptionsPrx = OptionsPrx
    del OptionsPrx

if 'Parameters' not in _M_omero.sys.__dict__:
    _M_omero.sys.Parameters = Ice.createTempClass()
    class Parameters(Ice.Object):
        '''Holder for all the parameters which can be taken to a query.'''
        def __init__(self, map=None, theFilter=None, theOptions=None):
            self.map = map
            self.theFilter = theFilter
            self.theOptions = theOptions

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::sys::Parameters')

        def ice_id(self, current=None):
            return '::omero::sys::Parameters'

        def ice_staticId():
            return '::omero::sys::Parameters'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_omero.sys._t_Parameters)

        __repr__ = __str__

    _M_omero.sys.ParametersPrx = Ice.createTempClass()
    class ParametersPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.sys.ParametersPrx.ice_checkedCast(proxy, '::omero::sys::Parameters', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.sys.ParametersPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.sys._t_ParametersPrx = IcePy.defineProxy('::omero::sys::Parameters', ParametersPrx)

    _M_omero.sys._t_Parameters = IcePy.declareClass('::omero::sys::Parameters')

    _M_omero.sys._t_Parameters = IcePy.defineClass('::omero::sys::Parameters', Parameters, -1, (), False, False, None, (), (
        ('map', (), _M_omero.sys._t_ParamMap, False, 0),
        ('theFilter', (), _M_omero.sys._t_Filter, False, 0),
        ('theOptions', (), _M_omero.sys._t_Options, False, 0)
    ))
    Parameters._ice_type = _M_omero.sys._t_Parameters

    _M_omero.sys.Parameters = Parameters
    del Parameters

    _M_omero.sys.ParametersPrx = ParametersPrx
    del ParametersPrx

if 'Principal' not in _M_omero.sys.__dict__:
    _M_omero.sys.Principal = Ice.createTempClass()
    class Principal(Ice.Object):
        '''Principal used for login, etc.'''
        def __init__(self, name='', group='', eventType='', umask=None):
            self.name = name
            self.group = group
            self.eventType = eventType
            self.umask = umask

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::sys::Principal')

        def ice_id(self, current=None):
            return '::omero::sys::Principal'

        def ice_staticId():
            return '::omero::sys::Principal'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_omero.sys._t_Principal)

        __repr__ = __str__

    _M_omero.sys.PrincipalPrx = Ice.createTempClass()
    class PrincipalPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.sys.PrincipalPrx.ice_checkedCast(proxy, '::omero::sys::Principal', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.sys.PrincipalPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.sys._t_PrincipalPrx = IcePy.defineProxy('::omero::sys::Principal', PrincipalPrx)

    _M_omero.sys._t_Principal = IcePy.declareClass('::omero::sys::Principal')

    _M_omero.sys._t_Principal = IcePy.defineClass('::omero::sys::Principal', Principal, -1, (), False, False, None, (), (
        ('name', (), IcePy._t_string, False, 0),
        ('group', (), IcePy._t_string, False, 0),
        ('eventType', (), IcePy._t_string, False, 0),
        ('umask', (), _M_omero.model._t_Permissions, False, 0)
    ))
    Principal._ice_type = _M_omero.sys._t_Principal

    _M_omero.sys.Principal = Principal
    del Principal

    _M_omero.sys.PrincipalPrx = PrincipalPrx
    del PrincipalPrx

if 'Roles' not in _M_omero.sys.__dict__:
    _M_omero.sys.Roles = Ice.createTempClass()
    class Roles(Ice.Object):
        '''Server-constants used for determining particular groups and
users.'''
        def __init__(self, rootId=0, rootName='', systemGroupId=0, systemGroupName='', userGroupId=0, userGroupName='', guestId=0, guestName='', guestGroupId=0, guestGroupName=''):
            self.rootId = rootId
            self.rootName = rootName
            self.systemGroupId = systemGroupId
            self.systemGroupName = systemGroupName
            self.userGroupId = userGroupId
            self.userGroupName = userGroupName
            self.guestId = guestId
            self.guestName = guestName
            self.guestGroupId = guestGroupId
            self.guestGroupName = guestGroupName

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::sys::Roles')

        def ice_id(self, current=None):
            return '::omero::sys::Roles'

        def ice_staticId():
            return '::omero::sys::Roles'
        ice_staticId = staticmethod(ice_staticId)

        def __str__(self):
            return IcePy.stringify(self, _M_omero.sys._t_Roles)

        __repr__ = __str__

    _M_omero.sys.RolesPrx = Ice.createTempClass()
    class RolesPrx(Ice.ObjectPrx):

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.sys.RolesPrx.ice_checkedCast(proxy, '::omero::sys::Roles', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.sys.RolesPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_omero.sys._t_RolesPrx = IcePy.defineProxy('::omero::sys::Roles', RolesPrx)

    _M_omero.sys._t_Roles = IcePy.defineClass('::omero::sys::Roles', Roles, -1, (), False, False, None, (), (
        ('rootId', (), IcePy._t_long, False, 0),
        ('rootName', (), IcePy._t_string, False, 0),
        ('systemGroupId', (), IcePy._t_long, False, 0),
        ('systemGroupName', (), IcePy._t_string, False, 0),
        ('userGroupId', (), IcePy._t_long, False, 0),
        ('userGroupName', (), IcePy._t_string, False, 0),
        ('guestId', (), IcePy._t_long, False, 0),
        ('guestName', (), IcePy._t_string, False, 0),
        ('guestGroupId', (), IcePy._t_long, False, 0),
        ('guestGroupName', (), IcePy._t_string, False, 0)
    ))
    Roles._ice_type = _M_omero.sys._t_Roles

    _M_omero.sys.Roles = Roles
    del Roles

    _M_omero.sys.RolesPrx = RolesPrx
    del RolesPrx

# End of module omero.sys

__name__ = 'omero'

# End of module omero