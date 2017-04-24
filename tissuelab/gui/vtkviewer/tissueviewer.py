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

from openalea.core.service.ipython import interpreter as get_interpreter
from openalea.oalab.service.drag_and_drop import add_drop_callback
from openalea.oalab.utils import qicon
from openalea.vpltk.qt import QtGui
from tissuelab.gui.vtkviewer.editor import SelectCellInteractorStyle
from tissuelab.gui.vtkviewer.vtk_viewer_select_mode import VtkviewerSelectMode
from tissuelab.gui.vtkviewer.vtkworldviewer import VtkWorldViewer
from tissuelab.gui.vtkviewer.point_editor import SelectPointInteractorStyle


class TissueViewer(QtGui.QWidget):

    MODE_VISUALISATION = 0
    MODE_EDITION = 1
    MODE_BLENDING = 2
    MODE_POINT_EDITION = 3

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

        add_drop_callback(self, 'IImage', self.drop_image)

    def _create_actions(self):
        self.action_auto_focus = QtGui.QAction(qicon("paraview/pqResetCamera32.png"), 'Auto focus', self)
        self.action_save_screenshot = QtGui.QAction(qicon("Crystal_Clear_app_camera.png"), 'Screenshot', self)

        self._reset_view_actions = []
        for direction in list('xyz'):
            for sign, vtk_sign, symbol in (['positive', 'plus', '+'], ['negative', 'minus', '-']):
                icon = 'paraview/pq%s%s32.png' % (direction.upper(), vtk_sign.capitalize())
                reset_func_name = 'reset_%s_%s' % (direction, sign)
                action = QtGui.QAction(qicon(icon), 'Set view %s%s' % (symbol, direction.upper()), self)
                reset_func = getattr(self.vtk, reset_func_name)
                action.triggered.connect(reset_func)
                #self._reset_view_actions['action_%s' % reset_func_name] = action
                self._reset_view_actions.append(action)

        self.action_parallel_projection = QtGui.QAction(qicon("paraview/pqRotate32.png"), 'Parallel Projection', self)
        self.action_parallel_projection.setCheckable(True)
        self.action_parallel_projection.toggled.connect(self.vtk.set_parallel_projection)

    def _create_connections(self):
        self.action_auto_focus.triggered.connect(self.vtk.auto_focus)
        self.action_save_screenshot.triggered.connect(self.save_screenshot)
        self.mode_selector.launch_popup.connect(self.launch_popup)
        self.mode_selector.mode_changed.connect(self.change_mode)
        self.mode_selector.matrix_changed.connect(self.matrix_changed)

    def toolbars(self):
        toolbar = QtGui.QToolBar("Tissue Viewer")
        toolbar.addActions([
            self.action_save_screenshot,
            self.action_auto_focus,
            self.action_parallel_projection,
        ])
        toolbar.addActions(self._reset_view_actions)
        return [toolbar]

    def toolbar_actions(self):
        return [
            self.action_save_screenshot,
            self.action_auto_focus,
            self.action_parallel_projection,
        ] + self._reset_view_actions

    def local_toolbar_actions(self):
        return self.toolbar_actions() + [self.mode_selector]

    def matrix_changed(self, num, matrix):
        if self._mode == self.MODE_EDITION and num == 0:
            self.vtk.interactor_style.data = matrix

    def label_selected(self, obj, event):
        self.mode_selector.set_label(
            self.vtk.interactor_style.selected_label(),
            self.vtk.interactor_style.voxelsize,
            self.vtk.interactor_style.position)

    def change_mode(self, mode=MODE_VISUALISATION):
        if self._mode != mode:
            if self._mode == self.MODE_POINT_EDITION:
                self.vtk.world.remove('selected_cell')
                self.vtk.world.remove('axes')
                self.vtk.world.remove("selected_axis")
        if mode == self.MODE_VISUALISATION:
            self.vtk.set_interactor_style()
        elif mode == self.MODE_EDITION:
            interactor_style = SelectCellInteractorStyle()
            name = self.mode_selector.matrix_name(0)
            interactor_style.data = self.vtk.world[name].data
            for attribute in self.vtk.world[name].attributes:
                if attribute['name'] == 'voxelsize':
                    interactor_style.voxelsize = attribute['value']
                elif attribute['name'] == 'position':
                    interactor_style.position = attribute['value']
            interactor_style.AddObserver("LabelSelectedEvent", self.label_selected)
            self.vtk.set_interactor_style(interactor_style)
        elif mode == self.MODE_BLENDING:
            self.vtk.set_interactor_style()
        elif mode == self.MODE_POINT_EDITION:
            points_name = self.mode_selector.polydata_cb.currentText()
            image_name = self.mode_selector.image2_cb.currentText()
            interactor_style = SelectPointInteractorStyle(points_name=points_name, image_name=image_name)
            self.vtk.set_interactor_style(interactor_style)
        else:
            raise NotImplementedError('Edit mode %d is not implemented' % mode)
        self._mode = mode

    def launch_popup(self, matrix1, matrix2, label):
        if self._editor is None:
            from tissuelab.gui.vtkviewer.editor import EditorWindow
            self._editor = EditorWindow()
            self._editor.segmentation_changed.connect(self.apply_change_to_segmentation)
        #voxelsize = self.vtk.interactor_style.voxelsize
        self._editor.set_data(matrix1, matrix2, label)
        self._editor.show()

    def apply_change_to_segmentation(self, matrix):
        #self.vtk.world.__setitem__(self.mode_selector.matrix_name(0), matrix)
        namee = self.mode_selector.matrix_name(0)
        res = self.vtk.interactor_style.voxelsize
        pos = self.vtk.interactor_style.position

        self.vtk.world.remove(namee)
        self.vtk.world.add(matrix, name=namee, voxelsize=res, position=pos)
        self.mode_selector.set_label(self.vtk.interactor_style.selected_label(), res, pos)

    def save_screenshot(self):
        from openalea.vpltk.qt.compat import getsavefilename
        filters = "PNG Images (*.png);;Tiff Images (*.tiff);; JPEG Images (*.jpg)"
        filename, filters = getsavefilename(self, "Image filename", filters=filters)
        if filename:
            self.vtk.save_screenshot(filename)

    def drop_image(self, spatial_image, **kwds):
        self.vtk.world.add(spatial_image, name=kwds.pop('name', None))
        self.vtk.auto_focus()
