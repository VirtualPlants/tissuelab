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
# Generated from file `Constants.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy

# Start of module omero
_M_omero = Ice.openModule('omero')
__name__ = 'omero'

# Start of module omero.constants
_M_omero.constants = Ice.openModule('omero.constants')
__name__ = 'omero.constants'
_M_omero.constants.__doc__ = """
Most client-intended constants are provided in this module.
"""

_M_omero.constants.CLIENTUUID = "omero.client.uuid"

_M_omero.constants.SESSIONUUID = "omero.session.uuid"

_M_omero.constants.GCINTERVAL = 60

_M_omero.constants.GLACIER2PORT = 4064

_M_omero.constants.MESSAGESIZEMAX = 250000

_M_omero.constants.DEFAULTBATCHSIZE = 2000

_M_omero.constants.DEFAULTBLOCKSIZE = 5000000

_M_omero.constants.CLIENTTHREADPOOLSIZE = 5

_M_omero.constants.CONNECTTIMEOUT = 5000

_M_omero.constants.DEFAULTROUTER = "OMERO.Glacier2/router:ssl -p \100omero.port\100 -h \100omero.host\100" if _version_info_[0] < 3 else "OMERO.Glacier2/router:ssl -p \U00000040omero.port\U00000040 -h \U00000040omero.host\U00000040"

_M_omero.constants.ACMCLIENTHEARTBEAT = 2

_M_omero.constants.ACMCLIENTTIMEOUT = 60000

_M_omero.constants.ADMINSERVICE = "omero.api.IAdmin"

_M_omero.constants.ANALYSISSERVICE = "omero.api.IAnalysis"

_M_omero.constants.CONFIGSERVICE = "omero.api.IConfig"

_M_omero.constants.CONTAINERSERVICE = "omero.api.IContainer"

_M_omero.constants.EXPORTERSERVICE = "omero.api.Exporter"

_M_omero.constants.LDAPSERVICE = "omero.api.ILdap"

_M_omero.constants.PIXELSSERVICE = "omero.api.IPixels"

_M_omero.constants.PROJECTIONSERVICE = "omero.api.IProjection"

_M_omero.constants.QUERYSERVICE = "omero.api.IQuery"

_M_omero.constants.SESSIONSERVICE = "omero.api.ISession"

_M_omero.constants.SHARESERVICE = "omero.api.IShare"

_M_omero.constants.TIMELINESERVICE = "omero.api.ITimeline"

_M_omero.constants.TYPESSERVICE = "omero.api.ITypes"

_M_omero.constants.UPDATESERVICE = "omero.api.IUpdate"

_M_omero.constants.JOBHANDLE = "omero.api.JobHandle"

_M_omero.constants.RAWFILESTORE = "omero.api.RawFileStore"

_M_omero.constants.RAWPIXELSSTORE = "omero.api.RawPixelsStore"

_M_omero.constants.RENDERINGENGINE = "omero.api.RenderingEngine"

_M_omero.constants.ROISERVICE = "omero.api.IRoi"

_M_omero.constants.SCRIPTSERVICE = "omero.api.IScript"

_M_omero.constants.SEARCH = "omero.api.Search"

_M_omero.constants.THUMBNAILSTORE = "omero.api.ThumbnailStore"

_M_omero.constants.REPOSITORYINFO = "omero.api.IRepositoryInfo"

_M_omero.constants.RENDERINGSETTINGS = "omero.api.IRenderingSettings"

_M_omero.constants.METADATASERVICE = "omero.api.IMetadata"

_M_omero.constants.SHAREDRESOURCES = "omero.grid.SharedResources"

_M_omero.constants.USERNAME = "omero.user"

_M_omero.constants.PASSWORD = "omero.pass"

_M_omero.constants.GROUP = "omero.group"

_M_omero.constants.EVENT = "omero.event"

_M_omero.constants.AGENT = "omero.agent"

_M_omero.constants.IP = "omero.ip"

# Start of module omero.constants.cluster
_M_omero.constants.cluster = Ice.openModule('omero.constants.cluster')
__name__ = 'omero.constants.cluster'

_M_omero.constants.cluster.REDIRECT = "omero.cluster.redirect"

# End of module omero.constants.cluster

__name__ = 'omero.constants'

# Start of module omero.constants.annotation
_M_omero.constants.annotation = Ice.openModule('omero.constants.annotation')
__name__ = 'omero.constants.annotation'
_M_omero.constants.annotation.__doc__ = """
General constants used for annotations.
"""

# Start of module omero.constants.annotation.file
_M_omero.constants.annotation.file = Ice.openModule('omero.constants.annotation.file')
__name__ = 'omero.constants.annotation.file'
_M_omero.constants.annotation.file.__doc__ = """
Constants used for file annotations.
"""

_M_omero.constants.annotation.file.ORIGINALMETADATAPREFIX = "/openmicroscopy.org/omero/image_files/"

_M_omero.constants.annotation.file.ORIGINALMETADATA = "original_metadata.txt"

# End of module omero.constants.annotation.file

__name__ = 'omero.constants.annotation'

# End of module omero.constants.annotation

__name__ = 'omero.constants'

# Start of module omero.constants.data
_M_omero.constants.data = Ice.openModule('omero.constants.data')
__name__ = 'omero.constants.data'
_M_omero.constants.data.__doc__ = """
Constants used for field defaults and similar
in the omero.model classes.
"""

_M_omero.constants.data.NONAMESET = "NO_NAME_SET"

# End of module omero.constants.data

__name__ = 'omero.constants'

# Start of module omero.constants.metadata
_M_omero.constants.metadata = Ice.openModule('omero.constants.metadata')
__name__ = 'omero.constants.metadata'
_M_omero.constants.metadata.__doc__ = """
Namespaces for the omero.api.IMetadata interface.
"""

_M_omero.constants.metadata.NSINSIGHTTAGSET = "openmicroscopy.org/omero/insight/tagset"

_M_omero.constants.metadata.NSINSIGHTRATING = "openmicroscopy.org/omero/insight/rating"

_M_omero.constants.metadata.NSMOVIE = "openmicroscopy.org/omero/movie"

_M_omero.constants.metadata.NSCLIENTMAPANNOTATION = "openmicroscopy.org/omero/client/mapAnnotation"

# End of module omero.constants.metadata

__name__ = 'omero.constants'

# Start of module omero.constants.namespaces
_M_omero.constants.namespaces = Ice.openModule('omero.constants.namespaces')
__name__ = 'omero.constants.namespaces'
_M_omero.constants.namespaces.__doc__ = """
General namespaces for StructuredAnnotations
"""

_M_omero.constants.namespaces.NSFSRENAME = "openmicroscopy.org/omero/fs/rename"

_M_omero.constants.namespaces.NSMEASUREMENT = "openmicroscopy.org/omero/measurement"

_M_omero.constants.namespaces.NSAUTOCLOSE = "openmicroscopy.org/omero/import/autoClose"

_M_omero.constants.namespaces.NSTARGETTEMPLATE = "openmicroscopy.org/omero/import/targetTemplate"

_M_omero.constants.namespaces.NSCOMPANIONFILE = "openmicroscopy.org/omero/import/companionFile"

_M_omero.constants.namespaces.NSLOGFILE = "openmicroscopy.org/omero/import/logFile"

_M_omero.constants.namespaces.NSFILETRANSFER = "openmicroscopy.org/omero/import/fileTransfer"

_M_omero.constants.namespaces.NSEXPERIMENTERPHOTO = "openmicroscopy.org/omero/experimenter/photo"

_M_omero.constants.namespaces.NSBULKANNOTATIONS = "openmicroscopy.org/omero/bulk_annotations"

_M_omero.constants.namespaces.NSOMETIFF = "openmicroscopy.org/omero/ome_tiff"

_M_omero.constants.namespaces.NSCREATED = "openmicroscopy.org/omero/scripts/results/created"

_M_omero.constants.namespaces.NSDOWNLOAD = "openmicroscopy.org/omero/scripts/results/download"

_M_omero.constants.namespaces.NSVIEW = "openmicroscopy.org/omero/scripts/results/view"

_M_omero.constants.namespaces.NSDYNAMIC = "openmicroscopy.org/omero/scripts/job/dynamic"

_M_omero.constants.namespaces.NSMODULO = "openmicroscopy.org/omero/dimension/modulo"

# End of module omero.constants.namespaces

__name__ = 'omero.constants'

# Start of module omero.constants.analysis
_M_omero.constants.analysis = Ice.openModule('omero.constants.analysis')
__name__ = 'omero.constants.analysis'
_M_omero.constants.analysis.__doc__ = """
Namespaces for analysis.
"""

# Start of module omero.constants.analysis.flim
_M_omero.constants.analysis.flim = Ice.openModule('omero.constants.analysis.flim')
__name__ = 'omero.constants.analysis.flim'
_M_omero.constants.analysis.flim.__doc__ = """
namespaces related to the FLIM analysis.
"""

_M_omero.constants.analysis.flim.NSFLIM = "openmicroscopy.org/omero/analysis/flim"

_M_omero.constants.analysis.flim.KEYWORDFLIMCELL = "Cell"

_M_omero.constants.analysis.flim.KEYWORDFLIMBACKGROUND = "Background"

# End of module omero.constants.analysis.flim

__name__ = 'omero.constants.analysis'

# End of module omero.constants.analysis

__name__ = 'omero.constants'

# Start of module omero.constants.jobs
_M_omero.constants.jobs = Ice.openModule('omero.constants.jobs')
__name__ = 'omero.constants.jobs'

_M_omero.constants.jobs.SUBMITTED = "Submitted"

_M_omero.constants.jobs.RESUBMITTED = "Resubmitted"

_M_omero.constants.jobs.QUEUED = "Queued"

_M_omero.constants.jobs.REQUEUED = "Requeued"

_M_omero.constants.jobs.RUNNING = "Running"

_M_omero.constants.jobs.ERRORX = "Error"

_M_omero.constants.jobs.WAITING = "Waiting"

_M_omero.constants.jobs.FINISHED = "Finished"

_M_omero.constants.jobs.CANCELLED = "Cancelled"

# End of module omero.constants.jobs

__name__ = 'omero.constants'

# Start of module omero.constants.permissions
_M_omero.constants.permissions = Ice.openModule('omero.constants.permissions')
__name__ = 'omero.constants.permissions'

_M_omero.constants.permissions.LINKRESTRICTION = 0

_M_omero.constants.permissions.EDITRESTRICTION = 1

_M_omero.constants.permissions.DELETERESTRICTION = 2

_M_omero.constants.permissions.ANNOTATERESTRICTION = 3

_M_omero.constants.permissions.BINARYACCESS = "RESTRICT-BINARY-ACCESS"

# End of module omero.constants.permissions

__name__ = 'omero.constants'

# Start of module omero.constants.projection
_M_omero.constants.projection = Ice.openModule('omero.constants.projection')
__name__ = 'omero.constants.projection'

_M_omero.constants.projection.MAXIMUMINTENSITYMETHODOLOGY = "MAXIMUM_INTENSITY_PROJECTION"

_M_omero.constants.projection.MEANINTENSITYMETHODOLOGY = "MEAN_INTENSITY_PROJECTION"

_M_omero.constants.projection.SUMINTENSITYMETHODOLOGY = "SUM_INTENSITY_PROJECTION"

if 'ProjectionType' not in _M_omero.constants.projection.__dict__:
    _M_omero.constants.projection.ProjectionType = Ice.createTempClass()
    class ProjectionType(Ice.EnumBase):
        """
        Used by the IProjection methods to declare which projection to perform.
        """

        def __init__(self, _n, _v):
            Ice.EnumBase.__init__(self, _n, _v)

        def valueOf(self, _n):
            if _n in self._enumerators:
                return self._enumerators[_n]
            return None
        valueOf = classmethod(valueOf)

    ProjectionType.MAXIMUMINTENSITY = ProjectionType("MAXIMUMINTENSITY", 0)
    ProjectionType.MEANINTENSITY = ProjectionType("MEANINTENSITY", 1)
    ProjectionType.SUMINTENSITY = ProjectionType("SUMINTENSITY", 2)
    ProjectionType._enumerators = { 0:ProjectionType.MAXIMUMINTENSITY, 1:ProjectionType.MEANINTENSITY, 2:ProjectionType.SUMINTENSITY }

    _M_omero.constants.projection._t_ProjectionType = IcePy.defineEnum('::omero::constants::projection::ProjectionType', ProjectionType, (), ProjectionType._enumerators)

    _M_omero.constants.projection.ProjectionType = ProjectionType
    del ProjectionType

# End of module omero.constants.projection

__name__ = 'omero.constants'

# Start of module omero.constants.topics
_M_omero.constants.topics = Ice.openModule('omero.constants.topics')
__name__ = 'omero.constants.topics'

_M_omero.constants.topics.PROCESSORACCEPTS = "/internal/ProcessorAccept"

_M_omero.constants.topics.HEARTBEAT = "/public/HeartBeat"

# End of module omero.constants.topics

__name__ = 'omero.constants'

# Start of module omero.constants.categories
_M_omero.constants.categories = Ice.openModule('omero.constants.categories')
__name__ = 'omero.constants.categories'

_M_omero.constants.categories.PROCESSORCALLBACK = "ProcessorCallback"

_M_omero.constants.categories.PROCESSCALLBACK = "ProcessCallback"

# End of module omero.constants.categories

__name__ = 'omero.constants'

# End of module omero.constants

__name__ = 'omero'

# End of module omero