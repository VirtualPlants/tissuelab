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

from openalea.core.plugin import PluginDef


@PluginDef
class LineageViewer(object):

    name = 'LineageViewer'
    alias = 'Lineage Viewer'
    icon = 'icon_lineageviewer.png'

    def __call__(self):
        from tissuelab.gui.lineage import LineageViewer
        return LineageViewer


@PluginDef
class OmeroClient(object):

    name = 'OmeroClient'
    alias = 'Omero DB'
    icon = 'icon_omero.png'

    def __call__(self):
        from tissuelab.omero.client import OmeroClient
        return OmeroClient


@PluginDef
class TissueViewer(object):

    name = 'TissueViewer'
    alias = '3D Viewer'
    icon = 'icon_vtkviewer.png'

    def __call__(self):
        from tissuelab.gui.vtkviewer.tissueviewer import TissueViewer
        return TissueViewer


@PluginDef
class VtkControlPanel(object):

    name = 'VtkControlPanel'
    alias = '3D Viewer controls'
    icon = 'icon_vtkcontrolpanel.png'

    def __call__(self):
        from tissuelab.gui.vtkviewer.vtkcontrolpanel import VtkControlPanel
        return VtkControlPanel
