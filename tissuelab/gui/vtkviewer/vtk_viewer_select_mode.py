from tissuelab.gui.vtkviewer.designer._vtk_viewer_select_mode import Ui_vtk_viewer_select_mode, _translate
from tissuelab.gui.vtkviewer.vtkworldviewer import ImageBlending
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener
from openalea.oalab.world import World
import numpy as np


class VtkviewerSelectMode(QtGui.QWidget, Ui_vtk_viewer_select_mode, AbstractListener):

    launch_popup = QtCore.Signal(np.ndarray, np.ndarray, int)

    def __init__(self):
        QtGui.QWidget.__init__(self)
        AbstractListener.__init__(self)
        #Ui_vtk_viewer_select_mode.__init__(self)
        self.setupUi(self)

        self.world = World()
        self.world.register_listener(self)

        self.action_launch_button.hide()
        self.image1_label.hide()
        self.image2_label.hide()
        self.image1_cb.hide()
        self.image2_cb.hide()

        self.selected_mode_index = 0

        self.list_interactor_choice = ['visualisation', 'edition', 'blending']
        for choice in self.list_interactor_choice:
            self.cb_interactor_choice.addItem(choice)
        #self.cb_interactor_choice.addItem('visualisation')
        #self.cb_interactor_choice.addItem('edition')

        self.cb_interactor_choice.currentIndexChanged.connect(self.select_mode)
        self.action_launch_button.pressed.connect(self.button_pressed_launch_popup)

    def select_mode(self, index):
        #TODO : changer en cherchant les enfants.

        self.selected_mode_index = index

        if index == 1:
            self.action_launch_button.setToolTip(
                _translate("vtk_viewer_select_mode",
                           "Start the selected cell edition",
                           None))
            self.action_launch_button.setText(_translate("vtk_viewer_select_mode", "Edit Cell", None))
            self.action_launch_button.show()
            self.image1_label.setToolTip(_translate("vtk_viewer_select_mode", "choose your segmented matrix", None))
            self.image1_label.setText(
                _translate("vtk_viewer_select_mode",
                           "<html><head/><body><p>Segmented</p></body></html>",
                           None))
            self.image1_label.show()
            self.image1_cb.show()
            self.image2_label.setToolTip(_translate("vtk_viewer_select_mode", "choose your intensity matrix", None))
            self.image2_label.setText(
                _translate("vtk_viewer_select_mode",
                           "<html><head/><body><p>Intensity</p></body></html>",
                           None))
            self.image2_label.show()
            self.image2_cb.show()
        elif index == 2:
            self.action_launch_button.setToolTip(
                _translate("vtk_viewer_select_mode",
                           "Blend the two selected images",
                           None))
            self.action_launch_button.setText(_translate("vtk_viewer_select_mode", "Blend Images", None))
            self.action_launch_button.show()
            self.image1_label.setToolTip(_translate("vtk_viewer_select_mode", "choose your first image matrix", None))
            self.image1_label.setText(
                _translate("vtk_viewer_select_mode",
                           "<html><head/><body><p>Image 1</p></body></html>",
                           None))
            self.image1_label.show()
            self.image1_cb.show()
            self.image2_label.setToolTip(_translate("vtk_viewer_select_mode", "choose your second image matrix", None))
            self.image2_label.setText(
                _translate("vtk_viewer_select_mode",
                           "<html><head/><body><p>Image 2</p></body></html>",
                           None))
            self.image2_label.show()
            self.image2_cb.show()
        else:
            self.image1_label.hide()
            self.image1_cb.hide()
            self.image2_label.hide()
            self.image2_cb.hide()
            self.action_launch_button.hide()

    def button_pressed_launch_popup(self):
        if self.selected_mode_index == 1:
            name_segmented_matrix = self.image1_cb.currentText()
            name_intensity_matrix = self.image2_cb.currentText()
            segmented_matrix = self.GetMatrixFromName(name_segmented_matrix)
            intensity_matrix = self.GetMatrixFromName(name_intensity_matrix)
            label = get_label()
            self.launch_popup.emit(intensity_matrix, segmented_matrix, label)
        elif self.selected_mode_index == 2:
            name1 = str(self.image1_cb.currentText())
            name2 = str(self.image2_cb.currentText())
            blending = ImageBlending([self.world[name1], self.world[name2]])
            self.world.add(blending, name1 + "_" + name2 + "_blending")

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_sync':
            self.set_world(data)
        elif signal == 'wold_changed':
            self.set_world(data)
        elif signal == 'world_object_changed':
            world, old, new = data
            if old is None:
                self.image1_cb.addItem(new.name)
                self.image2_cb.addItem(new.name)
            elif isinstance(old.data, np.ndarray):
                if not isinstance(new.data, np.ndarray):
                    index = self.image1_cb.findText(old.name)
                    self.image1_cb.removeItem(index)
                    index = self.image2_cb.findText(old.name)
                    self.image2_cb.removeItem(index)
            elif isinstance(new.data, np.ndarray):
                if not isinstance(old.data, np.ndarray):
                    self.image1_cb.addItem(new.name)
                    self.image2_cb.addItem(new.name)
        elif signal == 'world_object_item_changed':
            world, obj, item, old, new = data
            obj_data = obj.data
            if item == 'name':
                if isinstance(obj_data, np.ndarray):
                    self.update_world_object_name(old, new)

            """elif new['name'] != old['name'] :
                self.update_world_object_name(old, new)"""

    def set_world(self, world):
        self.clear()
        for obj_name, world_object in world.items():
            object_data = world_object.data
            if isinstance(object_data, np.ndarray):
                self.image1_cb.addItem(obj_name)
                self.image2_cb.addItem(obj_name)

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

    def GetMatrixFromName(self, matrix_name):
        for obj_name, world_object in self.world.items():
            if obj_name == matrix_name:
                object_data = world_object.data
                return object_data


def get_label():
    label = 1256
    return label

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
