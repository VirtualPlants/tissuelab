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


omero = {'team': u'OME', 'website': u'https://www.openmicroscopy.org', 'icon': u'icon_omero.png'}
vtk = {'team': u'VTK', 'website': u'http://www.vtk.org/'}

from openalea.core.plugin import PluginDef
from openalea.core.authors import akonig, dbarbeau, gbaty, gcerutti, sribes


@PluginDef
class LineageViewer(object):

    name = 'LineageViewer'
    label = 'Lineage Viewer'
    icon = 'icon_lineageviewer.png'

    authors = [dbarbeau, gbaty]
    tags = ['2d']

    def __call__(self):
        from tissuelab.gui.lineage import LineageViewer
        return LineageViewer


@PluginDef
class OmeroClient(object):

    name = 'OmeroClient'
    label = 'Omero DB'
    icon = 'icon_omero.png'
    tags = ['omero', 'tissue', 'database']
    authors = [gbaty]

    def __call__(self):
        from tissuelab.omero.client import OmeroClient
        return OmeroClient

@PluginDef
class TissueViewer(object):

    name = 'TissueViewer'
    label = '3D Viewer'
    icon = 'icon_vtkviewer.png'
    authors = [akonig, gcerutti, gbaty, sribes]
    tags = ['tissue', 'vtk', 'viewer', '3d']

    def __call__(self):
        from tissuelab.gui.vtkviewer.tissueviewer import TissueViewer
        return TissueViewer


@PluginDef
class VtkControlPanel(object):

    name = 'VtkControlPanel'
    label = '3D Viewer controls'
    icon = 'icon_vtkcontrolpanel.png'
    authors = [gbaty, gcerutti]
    tags = ['deprecated', 'vtk', 'panel']

    def __call__(self):
        from tissuelab.gui.vtkviewer.vtkcontrolpanel import VtkControlPanel
        return VtkControlPanel
