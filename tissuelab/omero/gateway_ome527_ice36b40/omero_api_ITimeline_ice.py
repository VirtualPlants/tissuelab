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
# Generated from file `ITimeline.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy
import omero_ModelF_ice
import omero_ServicesF_ice
import omero_System_ice
import omero_Collections_ice

# Included module omero
_M_omero = Ice.openModule('omero')

# Included module omero.model
_M_omero.model = Ice.openModule('omero.model')

# Included module Ice
_M_Ice = Ice.openModule('Ice')

# Included module Glacier2
_M_Glacier2 = Ice.openModule('Glacier2')

# Included module omero.sys
_M_omero.sys = Ice.openModule('omero.sys')

# Included module omero.api
_M_omero.api = Ice.openModule('omero.api')

# Included module omero.grid
_M_omero.grid = Ice.openModule('omero.grid')

# Start of module omero
__name__ = 'omero'

# Start of module omero.api
__name__ = 'omero.api'

if 'ITimeline' not in _M_omero.api.__dict__:
    _M_omero.api.ITimeline = Ice.createTempClass()
    class ITimeline(_M_omero.api.ServiceInterface):
        """
        Service for the querying of OMERO metadata based on creation and modification
        time. Currently supported types for querying include:
        - "Annotation"
        - "Dataset"
        - "Image"
        - "Project"
        - "RenderingDef"
        Return maps:
        -----------
        The map return values will be indexed by the short type name above:
        ""Project", ""Image"", ... All keys which are passed in the StringSet
        argument will be included in the returned map, even if they have no
        values. A default value of 0 or the empty list \[] will be used.
        The only exception to this rule is that the null or empty StringSet
        implies all valid keys.
        Parameters:
        ----------
        All methods take a omero::sys::Parameters object and will apply the filter
        object for paging through the data in order to prevent loading too
        many objects. If the parameters argument is null or no paging is activated,
        then the default will be: OFFSET=0, LIMIT=50. Filter.ownerId and
        Filter.groupId will also be AND'ed to the query if either value is present.
        If both are null, then the current user id will be used. To retrieve for
        all users, use ownerId == rlong(-1) and groupId == null.
        Merging:
        -------
        The methods which take a StringSet and a Parameters object, also have
        a ""bool merge"" argument. This argument defines whether or not the LIMIT
        applies to each object independently (\["a","b"] @ 100 == 200) or merges
        the lists together chronologically (\["a","b"] @ 100 merged == 100).
        Time used:
        =========
        Except for Image, IObject.details.updateEvent is used in all cases for
        determining most recent events. Images are compared via
        Image.acquisitionDate which is unlike the other properties is modifiable
        by the user.
        A typical invocation might look like (in Python):
        timeline = sf.getTimelineService()
        params = ParametersI().page(0,100)
        types = \["Project","Dataset"])
        map = timeline.getByPeriod(types, params, False)
        At this point, map will not contain more than 200 objects.
        This service is defined only in Blitz and so no javadoc is available
        in the ome.api package.
        TODOS: binning, stateful caching, ...
        """
        def __init__(self):
            if Ice.getType(self) == _M_omero.api.ITimeline:
                raise RuntimeError('omero.api.ITimeline is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::omero::api::ITimeline', '::omero::api::ServiceInterface')

        def ice_id(self, current=None):
            return '::omero::api::ITimeline'

        def ice_staticId():
            return '::omero::api::ITimeline'
        ice_staticId = staticmethod(ice_staticId)

        def getMostRecentAnnotationLinks_async(self, _cb, parentTypes, childTypes, namespaces, p, current=None):
            """
            Return the last LIMIT annotation __Links__ whose parent (IAnnotated)
            matches one of the parentTypes, whose child (Annotation) matches one
            of the childTypes (limit of one for the moment), and who namespace
            matches via ILIKE.
            The parents and children will be unloaded. The link will have
            its creation/update events loaded.
            If Parameters.theFilter.ownerId or groupId are set, they will be
            AND'ed to the query to filter results.
            Merges by default based on parentType.
            Arguments:
            _cb -- The asynchronous callback object.
            parentTypes -- 
            childTypes -- 
            namespaces -- 
            p -- 
            current -- The Current object for the invocation.
            """
            pass

        def getMostRecentShareCommentLinks_async(self, _cb, p, current=None):
            """
            Return the last LIMIT comment annotation links attached to a share by
            __others__.
            Note: Currently the storage of these objects is not optimal
            and so this method may change.
            Arguments:
            _cb -- The asynchronous callback object.
            p -- 
            current -- The Current object for the invocation.
            """
            pass

        def getMostRecentObjects_async(self, _cb, types, p, merge, current=None):
            """
            Returns the last LIMIT objects of TYPES as ordered by
            creation/modification times in the Event table.
            Arguments:
            _cb -- The asynchronous callback object.
            types -- 
            p -- 
            merge -- 
            current -- The Current object for the invocation.
            """
            pass

        def getByPeriod_async(self, _cb, types, start, end, p, merge, current=None):
            """
            Returns the given LIMIT objects of TYPES as ordered by
            creation/modification times in the Event table, but
            within the given time window.
            Arguments:
            _cb -- The asynchronous callback object.
            types -- 
            start -- 
            end -- 
            p -- 
            merge -- 
            current -- The Current object for the invocation.
            """
            pass

        def countByPeriod_async(self, _cb, types, start, end, p, current=None):
            """
            Queries the same information as getByPeriod, but only returns the counts
            for the given objects.
            Arguments:
            _cb -- The asynchronous callback object.
            types -- 
            start -- 
            end -- 
            p -- 
            current -- The Current object for the invocation.
            """
            pass

        def getEventLogsByPeriod_async(self, _cb, start, end, p, current=None):
            """
            Returns the EventLog table objects which are queried to produce the counts above.
            Note the concept of ""period inclusion"" mentioned above.
            WORKAROUND WARNING: this method returns non-managed EventLogs (i.e.
            eventLog.getId() == null) for "Image acquisitions".
            Arguments:
            _cb -- The asynchronous callback object.
            start -- 
            end -- 
            p -- 
            current -- The Current object for the invocation.
            """
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_omero.api._t_ITimeline)

        __repr__ = __str__

    _M_omero.api.ITimelinePrx = Ice.createTempClass()
    class ITimelinePrx(_M_omero.api.ServiceInterfacePrx):

        """
        Return the last LIMIT annotation __Links__ whose parent (IAnnotated)
        matches one of the parentTypes, whose child (Annotation) matches one
        of the childTypes (limit of one for the moment), and who namespace
        matches via ILIKE.
        The parents and children will be unloaded. The link will have
        its creation/update events loaded.
        If Parameters.theFilter.ownerId or groupId are set, they will be
        AND'ed to the query to filter results.
        Merges by default based on parentType.
        Arguments:
        parentTypes -- 
        childTypes -- 
        namespaces -- 
        p -- 
        _ctx -- The request context for the invocation.
        """
        def getMostRecentAnnotationLinks(self, parentTypes, childTypes, namespaces, p, _ctx=None):
            return _M_omero.api.ITimeline._op_getMostRecentAnnotationLinks.invoke(self, ((parentTypes, childTypes, namespaces, p), _ctx))

        """
        Return the last LIMIT annotation __Links__ whose parent (IAnnotated)
        matches one of the parentTypes, whose child (Annotation) matches one
        of the childTypes (limit of one for the moment), and who namespace
        matches via ILIKE.
        The parents and children will be unloaded. The link will have
        its creation/update events loaded.
        If Parameters.theFilter.ownerId or groupId are set, they will be
        AND'ed to the query to filter results.
        Merges by default based on parentType.
        Arguments:
        parentTypes -- 
        childTypes -- 
        namespaces -- 
        p -- 
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation.
        """
        def begin_getMostRecentAnnotationLinks(self, parentTypes, childTypes, namespaces, p, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.api.ITimeline._op_getMostRecentAnnotationLinks.begin(self, ((parentTypes, childTypes, namespaces, p), _response, _ex, _sent, _ctx))

        """
        Return the last LIMIT annotation __Links__ whose parent (IAnnotated)
        matches one of the parentTypes, whose child (Annotation) matches one
        of the childTypes (limit of one for the moment), and who namespace
        matches via ILIKE.
        The parents and children will be unloaded. The link will have
        its creation/update events loaded.
        If Parameters.theFilter.ownerId or groupId are set, they will be
        AND'ed to the query to filter results.
        Merges by default based on parentType.
        Arguments:
        parentTypes -- 
        childTypes -- 
        namespaces -- 
        p -- 
        """
        def end_getMostRecentAnnotationLinks(self, _r):
            return _M_omero.api.ITimeline._op_getMostRecentAnnotationLinks.end(self, _r)

        """
        Return the last LIMIT comment annotation links attached to a share by
        __others__.
        Note: Currently the storage of these objects is not optimal
        and so this method may change.
        Arguments:
        p -- 
        _ctx -- The request context for the invocation.
        """
        def getMostRecentShareCommentLinks(self, p, _ctx=None):
            return _M_omero.api.ITimeline._op_getMostRecentShareCommentLinks.invoke(self, ((p, ), _ctx))

        """
        Return the last LIMIT comment annotation links attached to a share by
        __others__.
        Note: Currently the storage of these objects is not optimal
        and so this method may change.
        Arguments:
        p -- 
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation.
        """
        def begin_getMostRecentShareCommentLinks(self, p, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.api.ITimeline._op_getMostRecentShareCommentLinks.begin(self, ((p, ), _response, _ex, _sent, _ctx))

        """
        Return the last LIMIT comment annotation links attached to a share by
        __others__.
        Note: Currently the storage of these objects is not optimal
        and so this method may change.
        Arguments:
        p -- 
        """
        def end_getMostRecentShareCommentLinks(self, _r):
            return _M_omero.api.ITimeline._op_getMostRecentShareCommentLinks.end(self, _r)

        """
        Returns the last LIMIT objects of TYPES as ordered by
        creation/modification times in the Event table.
        Arguments:
        types -- 
        p -- 
        merge -- 
        _ctx -- The request context for the invocation.
        """
        def getMostRecentObjects(self, types, p, merge, _ctx=None):
            return _M_omero.api.ITimeline._op_getMostRecentObjects.invoke(self, ((types, p, merge), _ctx))

        """
        Returns the last LIMIT objects of TYPES as ordered by
        creation/modification times in the Event table.
        Arguments:
        types -- 
        p -- 
        merge -- 
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation.
        """
        def begin_getMostRecentObjects(self, types, p, merge, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.api.ITimeline._op_getMostRecentObjects.begin(self, ((types, p, merge), _response, _ex, _sent, _ctx))

        """
        Returns the last LIMIT objects of TYPES as ordered by
        creation/modification times in the Event table.
        Arguments:
        types -- 
        p -- 
        merge -- 
        """
        def end_getMostRecentObjects(self, _r):
            return _M_omero.api.ITimeline._op_getMostRecentObjects.end(self, _r)

        """
        Returns the given LIMIT objects of TYPES as ordered by
        creation/modification times in the Event table, but
        within the given time window.
        Arguments:
        types -- 
        start -- 
        end -- 
        p -- 
        merge -- 
        _ctx -- The request context for the invocation.
        """
        def getByPeriod(self, types, start, end, p, merge, _ctx=None):
            return _M_omero.api.ITimeline._op_getByPeriod.invoke(self, ((types, start, end, p, merge), _ctx))

        """
        Returns the given LIMIT objects of TYPES as ordered by
        creation/modification times in the Event table, but
        within the given time window.
        Arguments:
        types -- 
        start -- 
        end -- 
        p -- 
        merge -- 
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation.
        """
        def begin_getByPeriod(self, types, start, end, p, merge, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.api.ITimeline._op_getByPeriod.begin(self, ((types, start, end, p, merge), _response, _ex, _sent, _ctx))

        """
        Returns the given LIMIT objects of TYPES as ordered by
        creation/modification times in the Event table, but
        within the given time window.
        Arguments:
        types -- 
        start -- 
        end -- 
        p -- 
        merge -- 
        """
        def end_getByPeriod(self, _r):
            return _M_omero.api.ITimeline._op_getByPeriod.end(self, _r)

        """
        Queries the same information as getByPeriod, but only returns the counts
        for the given objects.
        Arguments:
        types -- 
        start -- 
        end -- 
        p -- 
        _ctx -- The request context for the invocation.
        """
        def countByPeriod(self, types, start, end, p, _ctx=None):
            return _M_omero.api.ITimeline._op_countByPeriod.invoke(self, ((types, start, end, p), _ctx))

        """
        Queries the same information as getByPeriod, but only returns the counts
        for the given objects.
        Arguments:
        types -- 
        start -- 
        end -- 
        p -- 
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation.
        """
        def begin_countByPeriod(self, types, start, end, p, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.api.ITimeline._op_countByPeriod.begin(self, ((types, start, end, p), _response, _ex, _sent, _ctx))

        """
        Queries the same information as getByPeriod, but only returns the counts
        for the given objects.
        Arguments:
        types -- 
        start -- 
        end -- 
        p -- 
        """
        def end_countByPeriod(self, _r):
            return _M_omero.api.ITimeline._op_countByPeriod.end(self, _r)

        """
        Returns the EventLog table objects which are queried to produce the counts above.
        Note the concept of ""period inclusion"" mentioned above.
        WORKAROUND WARNING: this method returns non-managed EventLogs (i.e.
        eventLog.getId() == null) for "Image acquisitions".
        Arguments:
        start -- 
        end -- 
        p -- 
        _ctx -- The request context for the invocation.
        """
        def getEventLogsByPeriod(self, start, end, p, _ctx=None):
            return _M_omero.api.ITimeline._op_getEventLogsByPeriod.invoke(self, ((start, end, p), _ctx))

        """
        Returns the EventLog table objects which are queried to produce the counts above.
        Note the concept of ""period inclusion"" mentioned above.
        WORKAROUND WARNING: this method returns non-managed EventLogs (i.e.
        eventLog.getId() == null) for "Image acquisitions".
        Arguments:
        start -- 
        end -- 
        p -- 
        _response -- The asynchronous response callback.
        _ex -- The asynchronous exception callback.
        _sent -- The asynchronous sent callback.
        _ctx -- The request context for the invocation.
        Returns: An asynchronous result object for the invocation.
        """
        def begin_getEventLogsByPeriod(self, start, end, p, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_omero.api.ITimeline._op_getEventLogsByPeriod.begin(self, ((start, end, p), _response, _ex, _sent, _ctx))

        """
        Returns the EventLog table objects which are queried to produce the counts above.
        Note the concept of ""period inclusion"" mentioned above.
        WORKAROUND WARNING: this method returns non-managed EventLogs (i.e.
        eventLog.getId() == null) for "Image acquisitions".
        Arguments:
        start -- 
        end -- 
        p -- 
        """
        def end_getEventLogsByPeriod(self, _r):
            return _M_omero.api.ITimeline._op_getEventLogsByPeriod.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_omero.api.ITimelinePrx.ice_checkedCast(proxy, '::omero::api::ITimeline', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_omero.api.ITimelinePrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::omero::api::ITimeline'
        ice_staticId = staticmethod(ice_staticId)

    _M_omero.api._t_ITimelinePrx = IcePy.defineProxy('::omero::api::ITimeline', ITimelinePrx)

    _M_omero.api._t_ITimeline = IcePy.defineClass('::omero::api::ITimeline', ITimeline, -1, (), True, False, None, (_M_omero.api._t_ServiceInterface,), ())
    ITimeline._ice_type = _M_omero.api._t_ITimeline

    ITimeline._op_getMostRecentAnnotationLinks = IcePy.Operation('getMostRecentAnnotationLinks', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (((), _M_omero.api._t_StringSet, False, 0), ((), _M_omero.api._t_StringSet, False, 0), ((), _M_omero.api._t_StringSet, False, 0), ((), _M_omero.sys._t_Parameters, False, 0)), (), ((), _M_omero.api._t_IObjectList, False, 0), (_M_omero._t_ServerError,))
    ITimeline._op_getMostRecentShareCommentLinks = IcePy.Operation('getMostRecentShareCommentLinks', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (((), _M_omero.sys._t_Parameters, False, 0),), (), ((), _M_omero.api._t_IObjectList, False, 0), (_M_omero._t_ServerError,))
    ITimeline._op_getMostRecentObjects = IcePy.Operation('getMostRecentObjects', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (((), _M_omero.api._t_StringSet, False, 0), ((), _M_omero.sys._t_Parameters, False, 0), ((), IcePy._t_bool, False, 0)), (), ((), _M_omero.api._t_IObjectListMap, False, 0), (_M_omero._t_ServerError,))
    ITimeline._op_getByPeriod = IcePy.Operation('getByPeriod', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (((), _M_omero.api._t_StringSet, False, 0), ((), _M_omero._t_RTime, False, 0), ((), _M_omero._t_RTime, False, 0), ((), _M_omero.sys._t_Parameters, False, 0), ((), IcePy._t_bool, False, 0)), (), ((), _M_omero.api._t_IObjectListMap, False, 0), (_M_omero._t_ServerError,))
    ITimeline._op_countByPeriod = IcePy.Operation('countByPeriod', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (((), _M_omero.api._t_StringSet, False, 0), ((), _M_omero._t_RTime, False, 0), ((), _M_omero._t_RTime, False, 0), ((), _M_omero.sys._t_Parameters, False, 0)), (), ((), _M_omero.api._t_StringLongMap, False, 0), (_M_omero._t_ServerError,))
    ITimeline._op_getEventLogsByPeriod = IcePy.Operation('getEventLogsByPeriod', Ice.OperationMode.Idempotent, Ice.OperationMode.Idempotent, True, None, (), (((), _M_omero._t_RTime, False, 0), ((), _M_omero._t_RTime, False, 0), ((), _M_omero.sys._t_Parameters, False, 0)), (), ((), _M_omero.api._t_EventLogList, False, 0), (_M_omero._t_ServerError,))

    _M_omero.api.ITimeline = ITimeline
    del ITimeline

    _M_omero.api.ITimelinePrx = ITimelinePrx
    del ITimelinePrx

# End of module omero.api

__name__ = 'omero'

# End of module omero
