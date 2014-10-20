from openalea.oalab.plugins.applets import PluginApplet


class LineageViewer(PluginApplet):

    name = 'LineageViewer'
    alias = 'Lineage Viewer'

    def __call__(self):
        from tissuelab.gui.lineage import LineageViewer
        return LineageViewer

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        mainwindow.add_applet(applet, self.alias, area='outputs')
        self._fill_menu(mainwindow, applet)


class OmeroClient(PluginApplet):

    name = 'OmeroClient'
    alias = 'Omero DB'

    def __call__(self):
        from tissuelab.omero.client import OmeroClient
        return OmeroClient

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        mainwindow.add_applet(applet, self.alias, area='inputs')
        self._fill_menu(mainwindow, applet)
        mainwindow.menu_classic['Project'].addMenu(applet.menu)


class VtkViewer(PluginApplet):

    name = 'VtkViewer'
    alias = '3D Viewer'

    def __call__(self):
        from tissuelab.gui.vtkviewer import VtkViewerWidget
        return VtkViewerWidget

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        mainwindow.add_applet(applet, self.alias, area='outputs')
        self._fill_menu(mainwindow, applet)