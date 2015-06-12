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


import weakref
from openalea.oalab.gui.utils import qicon

from openalea.vpltk.qt import QtGui
from openalea.core.service.ipython import interpreter as get_interpreter

from tissuelab.gui.vtkviewer.vtkworldviewer import VtkWorldViewer

from tissuelab.gui.vtkviewer.vtk_viewer_select_mode import VtkviewerSelectMode
from tissuelab.gui.vtkviewer.editor import SelectCellInteractorStyle


class TissueViewer(QtGui.QWidget):

    MODE_VISUALISATION = 0
    MODE_EDITION = 1
    MODE_BLENDING = 2

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.vtk = VtkWorldViewer()  # embedded into the VtkViewerWidget
        layout.addWidget(self.vtk)

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_viewer'] = self
        self.interpreter.locals['viewer'] = self.vtk

        self._mode = self.MODE_VISUALISATION
        self.mode_selector = VtkviewerSelectMode()
        self._editor = None

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
        self.mode_selector.launch_popup.connect(self.launch_popup)
        self.mode_selector.mode_changed.connect(self.change_mode)
        self.mode_selector.matrix_changed.connect(self.matrix_changed)

    def toolbar_actions(self):
        return [
            self.action_auto_focus,
            self.action_save_screenshot,
        ]

    def local_toolbar_actions(self):
        return self.toolbar_actions() + [self.mode_selector]

    def matrix_changed(self, num, matrix):
        if self._mode == self.MODE_EDITION and num == 0:
            self.vtk.interactor_style.data = matrix

    def label_selected(self, obj, event):
        self.mode_selector.set_label(self.vtk.interactor_style.selected_label())

    def change_mode(self, mode=MODE_VISUALISATION):
        self._mode = mode
        if mode == self.MODE_VISUALISATION:
            self.vtk.set_interactor_style()
        elif mode == self.MODE_EDITION:
            interactor_style = SelectCellInteractorStyle()
            interactor_style.data = self.mode_selector.matrix(0)
            self.vtk.set_interactor_style(interactor_style)
            interactor_style.AddObserver("LabelSelectedEvent", self.label_selected)
        elif mode == self.MODE_BLENDING:
            self.vtk.set_interactor_style()
        else:
            raise NotImplementedError('Edit mode %d is not implemented' % mode)

    def launch_popup(self, matrix1, matrix2, label):
        if self._editor is None:
            from tissuelab.gui.vtkviewer.editor import EditorWindow
            self._editor = EditorWindow()
        self._editor.set_data(matrix1, matrix2, label)
        self._editor.show()

    def save_screenshot(self):
        from openalea.vpltk.qt.compat import getsavefilename
        filters = "PNG Images (*.png);;Tiff Images (*.tiff);; JPEG Images (*.jpg)"
        filename, filters = getsavefilename(self, "Image filename", filters=filters)
        if filename:
            self.vtk.save_screenshot(filename)
