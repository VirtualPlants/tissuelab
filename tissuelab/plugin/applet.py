from openalea.oalab.plugins.applets import PluginApplet


class LineageViewer(PluginApplet):

    name = 'LineageViewer'
    alias = 'Lineage Viewer'
    icon = 'icon_lineageviewer.png'

    def __call__(self):
        from tissuelab.gui.lineage import LineageViewer
        return LineageViewer


class OmeroClient(PluginApplet):

    name = 'OmeroClient'
    alias = 'Omero DB'
    icon = 'icon_omero.png'

    def __call__(self):
        from tissuelab.omero.client import OmeroClient
        return OmeroClient


class TissueViewer(PluginApplet):

    name = 'TissueViewer'
    alias = '3D Viewer'
    icon = 'icon_vtkviewer.png'

    def __call__(self):
        from tissuelab.gui.vtkviewer.tissueviewer import TissueViewer
        return TissueViewer


class VtkControlPanel(PluginApplet):

    name = 'VtkControlPanel'
    alias = '3D Viewer controls'
    icon = 'icon_vtkcontrolpanel.png'

    def __call__(self):
        from tissuelab.gui.vtkviewer.vtkcontrolpanel import VtkControlPanel
        return VtkControlPanel
