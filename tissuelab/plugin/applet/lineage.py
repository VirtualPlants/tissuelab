
from openalea.oalab.plugins.applets import PluginApplet

class LineageViewer(PluginApplet):

    name = 'LineageViewer'
    alias = 'Lineage Viewer'

    def __call__(self, mainwindow):
        from tissuelab.gui.lineage import LineageViewer

        self._applet = self.new(self.name, LineageViewer)
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
#         self._fill_menu(mainwindow, self._applet)
#         mainwindow.menu_classic['Project'].addMenu(self._applet.menu_available_projects)
