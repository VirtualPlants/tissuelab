from tissuelab.gui.vtkviewer.designer._vtk_viewer_select_mode import Ui_vtk_viewer_select_mode
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

        self.edit_launch_button.hide()
        self.txt_segmented.hide()
        self.txt_intensity.hide()
        self.cb_segmented.hide()
        self.cb_intensity.hide()
        
        self.list_interactor_choice = ['visualisation','edition']
        for choice in self.list_interactor_choice:
            self.cb_interactor_choice.addItem(choice)
        #self.cb_interactor_choice.addItem('visualisation')
        #self.cb_interactor_choice.addItem('edition')

        self.cb_interactor_choice.currentIndexChanged.connect(self.select_mode)
        self.edit_launch_button.pressed.connect(self.button_pressed_launch_popup)

    def select_mode(self, index):
        #TODO : changer en cherchant les enfants.
        if index == 1:
            self.edit_launch_button.show()
            self.txt_segmented.show()
            self.txt_intensity.show()
            self.cb_segmented.show()
            self.cb_intensity.show()
        else:
            self.edit_launch_button.hide()
            self.txt_segmented.hide()
            self.txt_intensity.hide()
            self.cb_segmented.hide()
            self.cb_intensity.hide()

    def button_pressed_launch_popup(self):
        name_segmented_matrix = self.cb_segmented.currentText()
        name_intensity_matrix = self.cb_intensity.currentText()
        segmented_matrix = self.GetMatrixFromName(name_segmented_matrix)
        intensity_matrix = self.GetMatrixFromName(name_intensity_matrix)
        label = get_label()
        self.launch_popup.emit(intensity_matrix, segmented_matrix, label)

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_sync':
            self.set_world(data)
        elif signal == 'wold_changed':
            self.set_world(data)
        elif signal == 'world_object_changed':
            world, old, new = data
            if old is None:
                self.cb_segmented.addItem(new.name)
                self.cb_intensity.addItem(new.name)
            elif isinstance(old.data, np.ndarray):
                if not isinstance(new.data, np.ndarray):
                    index = self.cb_segmented.findText(old.name)
                    self.cb_segmented.removeItem(index)
                    index = self.cb_intensity.findText(old.name)
                    self.cb_intensity.removeItem(index)
            elif isinstance(new.data, np.ndarray):
                if not isinstance(old.data, np.ndarray):
                    self.cb_segmented.addItem(new.name)
                    self.cb_intensity.addItem(new.name)
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
                self.cb_segmented.addItem(obj_name)
                self.cb_intensity.addItem(obj_name)

    def update_world_object_name(self, old, new):
        index = self.cb_segmented.findText(old.name)
        self.cb_segmented.setItemText(index, new.name)
        index = self.cb_intensity.findText(old.name)
        self.cb_intensity.setItemText(index, new.name)

    def clear(self):
        for i in xrange(self.cb_segmented.count()):
            self.cb_segmented.removeItem(0)
        for i in xrange(self.cb_intensity.count()):
            self.cb_intensity.removeItem(0)

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
