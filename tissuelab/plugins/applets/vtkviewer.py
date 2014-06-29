
from openalea.oalab.plugins.applets import PluginApplet

class VtkViewer(PluginApplet):

    name = 'VtkViewer'
    alias = '3D Viewer'

    def __call__(self, mainwindow):
        from tissuelab.gui.vtkviewer import VtkViewerWidget

        self._applet = self.new(self.name, VtkViewerWidget)
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
#         self._fill_menu(mainwindow, self._applet)
#         mainwindow.menu_classic['Project'].addMenu(self._applet.menu_available_projects)
