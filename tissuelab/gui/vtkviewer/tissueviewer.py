# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
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


from openalea.oalab.gui.utils import qicon

from openalea.vpltk.qt import QtGui
from openalea.core.service.ipython import interpreter as get_interpreter

from tissuelab.gui.vtkviewer.vtkworldviewer import VtkWorldViewer


class TissueViewer(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.vtk = VtkWorldViewer()  # embedded into the VtkViewerWidget
        layout.addWidget(self.vtk)

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_viewer'] = self
        self.interpreter.locals['viewer'] = self.vtk

        self._create_actions()
        self._create_connections()

    def _create_actions(self):
        self.action_auto_focus = QtGui.QAction(
            QtGui.QIcon(":/images/resources/resetzoom.png"), 'Auto focus', self)
        self.action_save_screenshot = QtGui.QAction(
            qicon("Crystal_Clear_app_camera.png"), 'Screenshot', self)

    def _create_connections(self):
        self.action_auto_focus.triggered.connect(self.vtk.auto_focus)
        self.action_save_screenshot.triggered.connect(self.save_screenshot)

    def toolbar_actions(self):
        return [
            self.action_auto_focus,
            self.action_save_screenshot
        ]

    def save_screenshot(self):
        from openalea.vpltk.qt.compat import getsavefilename
        filename, filters = getsavefilename(self, "Image filename")
        if filename:
            self.vtk.save_screenshot(filename)
