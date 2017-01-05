from Qt import QtCore, QtGui, QtWidgets

from tissuelab.gui.vtkviewer.editor import get_contours
from tissuelab.gui.vtkviewer.vtkworldviewer import ImageBlending
from tissuelab.gui.vtkviewer.designer._vtk_viewer_select_mode import Ui_vtk_viewer_select_mode

from openalea.core.observer import AbstractListener
from openalea.core.world import World
from openalea.vpltk.qt.designer import generate_pyfile_from_uifile

import numpy as np
import vtk


generate_pyfile_from_uifile(__name__)


class VtkviewerSelectMode(QtGui.QWidget, Ui_vtk_viewer_select_mode, AbstractListener):

    """
    Get Selector Data:
        - matrix_from_name(name) -> matrix (ndarray)
        - matrix_name(num) -> matrix name (str)

    Convenience Method:
        - matrix(num) -> matrix (ndarray)
    """

    launch_popup = QtCore.Signal(np.ndarray, np.ndarray, int)
    mode_changed = QtCore.Signal(int)
    matrix_changed = QtCore.Signal(int, np.ndarray)

    def __init__(self):
        QtGui.QWidget.__init__(self)
        AbstractListener.__init__(self)
        self.setupUi(self)

        self.world = World()
        self.world.register_listener(self)

        self.action_launch_button.setEnabled(False)

        self.action_launch_button.hide()
        self.synchro_cb.hide()
        self.image1_label.hide()
        self.image2_label.hide()
        self.image1_cb.hide()
        self.image2_cb.hide()
        self.polydata_label.hide()
        self.polydata_cb.hide()

        self.axis_cb.hide()
        self.axis_label.hide()
        # self.focus_cb.hide()
        self.slice_label.hide()
        self.slice_slider.hide()

        self.selected_mode_index = 0
        self._label = None
        self.point_image_synchronized = False

        self.list_interactor_choice = ['visualisation', 'edition', 'blending', 'point edition']
        for choice in self.list_interactor_choice:
            self.cb_interactor_choice.addItem(choice)
        self._create_connections()

    def _create_connections(self):
        self.cb_interactor_choice.currentIndexChanged.connect(self.select_mode)
        self.action_launch_button.pressed.connect(self.button_pressed_launch_popup)
        self.image1_cb.currentIndexChanged.connect(self.matrix1_changed)
        self.image2_cb.currentIndexChanged.connect(self.matrix2_changed)

        self.synchro_cb.stateChanged.connect(self.synchro_changed)
        self.axis_cb.currentIndexChanged.connect(self.synchro_changed)
        self.slice_slider.valueChanged.connect(self.synchro_changed)

    def select_mode(self, index):
        self.selected_mode_index = index

        if index == 1: # Edtion
            self.action_launch_button.setToolTip(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "Start the selected cell edition",
                                             None))
            self.action_launch_button.setText(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "Edit Cell",
                    None))
            self.action_launch_button.show()
            self.synchro_cb.hide()
            self.image1_label.setToolTip(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "choose your segmented matrix",
                    None))
            self.image1_label.setText(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "<html><head/><body><p>Segmented</p></body></html>",
                                             None))
            self.image1_label.show()
            self.image1_cb.show()
            self.image2_label.setToolTip(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "choose your intensity matrix",
                    None))
            self.image2_label.setText(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "<html><head/><body><p>Intensity</p></body></html>",
                                             None))
            self.image2_label.show()
            self.image2_cb.show()
            self.polydata_label.hide()
            self.polydata_cb.hide()

            self.axis_cb.hide()
            self.axis_label.hide()
            # self.focus_cb.hide()
            self.slice_label.hide()
            self.slice_slider.hide()

        elif index == 2: # Blending
            self.action_launch_button.setToolTip(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "Blend the two selected images",
                                             None))
            self.action_launch_button.setText(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "Blend Images",
                    None))
            self.action_launch_button.show()
            self.synchro_cb.hide()
            self.image1_label.setToolTip(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "choose your first image matrix",
                    None))
            self.image1_label.setText(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "<html><head/><body><p>Image 1</p></body></html>",
                                             None))
            self.image1_label.show()
            self.image1_cb.show()
            self.image2_label.setToolTip(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "choose your second image matrix",
                    None))
            self.image2_label.setText(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "<html><head/><body><p>Image 2</p></body></html>",
                                             None))
            self.image2_label.show()
            self.image2_cb.show()
            self.polydata_label.hide()
            self.polydata_cb.hide()

            self.axis_cb.hide()
            self.axis_label.hide()
            # self.focus_cb.hide()
            self.slice_label.hide()
            self.slice_slider.hide()

        elif index == 3: # Nuclei edition

            self.action_launch_button.hide()
            self.synchro_cb.show()
            self.image1_label.hide()
            self.image1_cb.hide()
            self.image2_label.setToolTip(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "choose the image on which to synchronize",
                    None))
            self.image2_label.setText(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "<html><head/><body><p>Sync. Image</p></body></html>",
                                             None))
            self.image2_label.show()
            self.image2_cb.show()
            self.polydata_label.setToolTip(
                QtGui.QApplication.translate(
                    "vtk_viewer_select_mode",
                    "choose your points",
                    None))
            self.polydata_label.setText(
                QtGui.QApplication.translate("vtk_viewer_select_mode",
                                             "<html><head/><body><p>Points</p></body></html>",
                                             None))
            self.polydata_label.show()
            self.polydata_cb.show()

            if self.synchro_cb.isChecked():
                self.axis_cb.show()
                self.axis_label.show()
                # self.focus_cb.show()
                self.slice_label.show()
                self.slice_slider.show()
            else:
                self.axis_cb.hide()
                self.axis_label.hide()
                # self.focus_cb.hide()
                self.slice_label.hide()
                self.slice_slider.hide()

        else: # Default (Visualisation)
            self.image1_label.hide()
            self.image1_cb.hide()
            self.image2_label.hide()
            self.image2_cb.hide()
            self.polydata_label.hide()
            self.polydata_cb.hide()
            self.synchro_cb.hide()
            self.action_launch_button.hide()

            self.axis_cb.hide()
            self.axis_label.hide()
            # self.focus_cb.hide()
            self.slice_label.hide()
            self.slice_slider.hide()

        self.enable_button()
        self.mode_changed.emit(index)

    def enable_button(self):
        if self.image1_cb.count() == 0:
            self.action_launch_button.setEnabled(False)
            return

        if self.selected_mode_index == 1:
            if self.get_label() is None:
                self.action_launch_button.setEnabled(False)
            else:
                self.action_launch_button.setEnabled(True)
        elif self.selected_mode_index == 3:
            if self.polydata_cb.count() == 0:
                self.synchro_cb.setEnabled(False)
            else:
                self.synchro_cb.setEnabled(True)
        else:
            self.action_launch_button.setEnabled(True)

    def matrix1_changed(self, index):
        if self.matrix_from_name(self.image1_cb.itemText(index)) is not None:
            self.matrix_changed.emit(0, self.matrix_from_name(self.image1_cb.itemText(index)))

    def matrix2_changed(self, index):
        if self.matrix_from_name(self.image2_cb.itemText(index)) is not None:
            self.matrix_changed.emit(1, self.matrix_from_name(self.image2_cb.itemText(index)))

    def button_pressed_launch_popup(self):
        if self.selected_mode_index == 1:
            name_segmented_matrix = self.image1_cb.currentText()
            name_intensity_matrix = self.image2_cb.currentText()
            segmented_matrix = self.matrix_from_name(name_segmented_matrix)
            intensity_matrix = self.matrix_from_name(name_intensity_matrix)
            label = self.get_label()
            self.launch_popup.emit(intensity_matrix, segmented_matrix, label)
        elif self.selected_mode_index == 2:
            name1 = str(self.image1_cb.currentText())
            name2 = str(self.image2_cb.currentText())
            blending = ImageBlending([self.world[name1], self.world[name2]])
            self.world.add(blending, name1 + "_" + name2 + "_blending")

    def synchro_changed(self):
        if self.selected_mode_index == 3:
            if self.synchro_cb.isChecked():
                self.axis_cb.show()
                self.axis_label.show()
                # self.focus_cb.show()
                self.slice_label.show()
                self.slice_slider.show()
                points_name = str(self.polydata_cb.currentText())
                image_name = str(self.image2_cb.currentText())
                self.cut_points(points_name,image_name)
            else:
                self.axis_cb.hide()
                self.axis_label.hide()
                # self.focus_cb.hide()
                self.slice_label.hide()
                self.slice_slider.hide()
                points_name = str(self.polydata_cb.currentText())
                self.world[points_name].set_attribute('x_slice',(-1,101))
                self.world[points_name].set_attribute('y_slice',(-1,101))
                self.world[points_name].set_attribute('z_slice',(-1,101))



    def cut_points(self, points_name, image_name):
        self.world[image_name].set_attribute('cut_planes',True)
        self.world[image_name].set_attribute('volume',False)
        # self.world[image_name].set_attribute('cut_planes_alpha',0.7)
        slice_width = int(self.slice_slider.value())
        if self.axis_cb.currentText() == 'X':
            x_level = self.world[image_name].get('x_plane_position')*self.world[image_name].get('resolution')[0]
            x_min = np.array(self.world[points_name].data.points.values())[:,0].min()
            x_max = np.array(self.world[points_name].data.points.values())[:,0].max()
            x_level = float(x_level-x_min)/(x_max-x_min)
            self.world[points_name].set_attribute('x_slice',(100*x_level-slice_width,100*x_level+slice_width))
            self.world[points_name].set_attribute('y_slice',(-1,101))
            self.world[points_name].set_attribute('z_slice',(-1,101))
        if self.axis_cb.currentText() == 'Y':
            y_level = self.world[image_name].get('y_plane_position')*self.world[image_name].get('resolution')[1]
            y_min = np.array(self.world[points_name].data.points.values())[:,1].min()
            y_max = np.array(self.world[points_name].data.points.values())[:,1].max()
            y_level = float(y_level-y_min)/(y_max-y_min)
            self.world[points_name].set_attribute('y_slice',(100*y_level-slice_width,100*y_level+slice_width))
            self.world[points_name].set_attribute('x_slice',(-1,101))
            self.world[points_name].set_attribute('z_slice',(-1,101))
        if self.axis_cb.currentText() == 'Z':
            z_level = self.world[image_name].get('z_plane_position')*self.world[image_name].get('resolution')[2]
            z_min = np.array(self.world[points_name].data.points.values())[:,2].min()
            z_max = np.array(self.world[points_name].data.points.values())[:,2].max()
            z_level = float(z_level-z_min)/(z_max-z_min)
            self.world[points_name].set_attribute('z_slice',(100*z_level-slice_width,100*z_level+slice_width))
            self.world[points_name].set_attribute('x_slice',(-1,101))
            self.world[points_name].set_attribute('y_slice',(-1,101))


    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_sync':
            self.set_world(data)
        elif signal == 'wold_changed':
            self.set_world(data)
        elif signal == 'world_object_changed':
            world, old, new = data
            if old is None:
                if isinstance(new.data, np.ndarray):
                    if new.name not in [self.image1_cb.itemText(i) for i in xrange(self.image1_cb.count())]:
                        self.image1_cb.addItem(new.name)
                    if new.name not in [self.image2_cb.itemText(i) for i in xrange(self.image2_cb.count())]:
                        self.image2_cb.addItem(new.name)
                elif "TriangularMesh" in str(new.data.__class__):
                    if new.name not in [self.polydata_cb.itemText(i) for i in xrange(self.polydata_cb.count())]:
                        self.polydata_cb.addItem(new.name)
            elif isinstance(old.data, np.ndarray):
                if not isinstance(new.data, np.ndarray):
                    index = self.image1_cb.findText(old.name)
                    self.image1_cb.removeItem(index)
                    index = self.image2_cb.findText(old.name)
                    self.image2_cb.removeItem(index)
                elif isinstance(new.data, np.ndarray):
                    if self.matrix_name(0) == old.name:
                        self.matrix_changed.emit(0, new.data)
                    elif self.matrix_name(1) == old.name:
                        self.matrix_changed.emit(1, new.data)
            elif isinstance(new.data, np.ndarray):
                if not isinstance(old.data, np.ndarray):
                    self.image1_cb.addItem(new.name)
                    self.image2_cb.addItem(new.name)
            elif "TriangularMesh" in str(old.data.__class__):
                if not "TriangularMesh" in str(new.data.__class__):
                    index = self.polydata_cb.findText(old.name)
                    self.polydata_cb.removeItem(index)
            elif "TriangularMesh" in str(new.data.__class__):
                self.polydata_cb.addItem(new.name)

        elif signal == 'world_object_item_changed':
            world, obj, item, old, new = data
            obj_data = obj.data
            if item == 'name':
                if isinstance(obj_data, np.ndarray):
                    self.update_world_object_name(old, new)
            if item == 'attribute':
                if self.selected_mode_index == 3:
                    if self.synchro_cb.isChecked():
                        if self.polydata_cb.count() > 0:
                            if obj.name == str(self.image2_cb.currentText()):
                                if ((new['name'] == 'x_plane_position' and  self.axis_cb.currentText() == 'X') or
                                    (new['name'] == 'y_plane_position' and  self.axis_cb.currentText() == 'Y') or
                                    (new['name'] == 'z_plane_position' and  self.axis_cb.currentText() == 'Z')) :
                                    self.cut_points(str(self.polydata_cb.currentText()),str(self.image2_cb.currentText()))

        elif signal == 'world_object_removed':
            world, old = data
            if isinstance(old.data, np.ndarray):
                index = self.image1_cb.findText(old.name)
                self.image1_cb.removeItem(index)
                index = self.image2_cb.findText(old.name)
                self.image2_cb.removeItem(index)
            elif "TriangularMesh" in str(old.data.__class__):
                index = self.polydata_cb.findText(old.name)
                self.polydata_cb.removeItem(index)

            """elif new['name'] != old['name'] :
                self.update_world_object_name(old, new)"""
        self.enable_button()

    def set_world(self, world):
        self.clear()
        for obj_name, world_object in world.items():
            object_data = world_object.data
            if isinstance(object_data, np.ndarray):
                self.image1_cb.addItem(obj_name)
                self.image2_cb.addItem(obj_name)
            elif "TriangularMesh" in str(world_object.data.__class__):
                self.polydata_cb.addItem(obj_name)

    def update_world_object_name(self, old, new):
        index = self.image1_cb.findText(old.name)
        self.image1_cb.setItemText(index, new.name)
        index = self.image2_cb.findText(old.name)
        self.image2_cb.setItemText(index, new.name)

    def clear(self):
        for i in xrange(self.image1_cb.count()):
            self.image1_cb.removeItem(0)
        for i in xrange(self.image2_cb.count()):
            self.image2_cb.removeItem(0)
        for i in xrange(self.polydata_cb.count()):
            self.polydata_cb.removeItem(0)

    def set_label(self, label, res, pos):
        if self._label is not None:
            name = str(self._label)
            self.world.remove("cell_edit_" + name)
        self._label = label
        contour = get_contours(self.matrix(0), self._label)
        name2 = str(self._label)
        self.world.add(contour, name="cell_edit_" + name2, colormap='glasbey', position=pos, resolution=res)

        self.enable_button()

    def get_label(self):
        return self._label

    def matrix_from_name(self, matrix_name):
        for obj_name, world_object in self.world.items():
            if obj_name == matrix_name:
                object_data = world_object.data
                return object_data

    def matrix_name(self, num):
        if num == 0:
            return self.image1_cb.currentText()
        elif num == 1:
            return self.image2_cb.currentText()
        else:
            raise ValueError("No matrix for num=%d" % num)

    def matrix(self, num):
        return self.matrix_from_name(self.matrix_name(num))

if __name__ == "__main__":
    import sys
    from tissuelab.gui.vtkviewer.editor import *
    from openalea.image.spatial_image import SpatialImage
    from openalea.image.serial.all import imread
    from tissuelab.gui.vtkviewer.editor import *

    #matint = imread('/Users/gcerutti/Developpement/openalea/vplants_branches/meshing/share/nuclei_images/olli01_lti6b_150421_sam01_t000/olli01_lti6b_150421_sam01_t000_seg_hmin_2.inr.gz')
    # matseg =
    # imread('/Users/gcerutti/Developpement/openalea/vplants_branches/meshing/share/nuclei_images/olli01_lti6b_150421_sam01_t000/olli01_lti6b_150421_sam01_t000_PIN.inr.gz')

    matseg = imread('/home/julien/.openalea/projects/temp/data/nonero.inr')
    matint = imread('/home/julien/.openalea/projects/temp/data/0hrs_plant_1-acylYFP.inr')
    #poly = get_contours(matseg,1256)

    world = World()
    world.add(matseg, name='seg')
    world.add(matint, name='int')
    #world.add(poly,name='poly')
    instance = QtGui.QApplication.instance()
    if instance is None:
        app = QtGui.QApplication(sys.argv)

    vtk_viewer_select_mode = VtkviewerSelectMode()
    vtk_viewer_select_mode.world = world
    vtk_viewer_select_mode.set_world(world)
    vtk_viewer_select_mode.show()
    viewer_editor = EditorWindow()
    vtk_viewer_select_mode.launch_popup.connect(viewer_editor.set_data)

    #world.add(matint,name='mat')
    #world.add(poly,name='seg')
    #world.add(matseg,name='poly')

    if instance is None:
        sys.exit(app.exec_())
