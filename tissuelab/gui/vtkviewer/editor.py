# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Alizon König <alizon.konig@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

import numpy as np
import vtk
from math import sqrt
from openalea.vpltk.qt import QtGui, QtCore
from tissuelab.gui.vtkviewer.qvtkrenderwindowinteractor import QVTKRenderWindowInteractor
from .vtk_utils import matrix_to_image_reader

#from openalea.image.serial.all import imsave
#from openalea.image.spatial_image import SpatialImage
from vtk import VTK_SIGNED_CHAR
from vtk import VTK_UNSIGNED_CHAR
from vtk import VTK_SHORT
from vtk import VTK_UNSIGNED_SHORT
from vtk import VTK_INT
from vtk import VTK_UNSIGNED_INT
from vtk import VTK_LONG
from vtk import VTK_UNSIGNED_LONG
from vtk import VTK_FLOAT
from vtk import VTK_DOUBLE

#TODO : recalculer la box de l'editor quand un point est deplace en dehors
#TODO : modifier le code pour le rendre plus expensif (laisser une place pour le choix de deplacement, de split, etc)
#TODO : rajouter une méthode de déplacement en fonction de l'intensité ????
#TODO : réparer bug qui fait crasher quand split puis fusion
# TODO : garder les mêmes réglages pour les matrices quand on fait apply
# (affichage coupe/volume, intensity/segmented, même tranche....


from openalea.vpltk.qt.designer import generate_pyfile_from_uifile, get_data


name = 'panel_control_editor'
src = get_data("tissuelab.gui.vtkviewer.designer", '%s.ui' % name)
dest = get_data("tissuelab.gui.vtkviewer.designer", "_%s.py" % name)
generate_pyfile_from_uifile(__name__, src=src, dest=dest)


from tissuelab.gui.vtkviewer.designer._panel_control_editor import Ui_panel_control_editor


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


class EditorWindow(QtGui.QWidget):

    """
    An EditorWindow is a class that defined the popup that open when you edit a cell.
    It contains a widget with control panel and a vtk viewer and link them together
    """

    segmentation_changed = QtCore.Signal(np.ndarray)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QtGui.QFrame()
        self.vl = QtGui.QGridLayout(self.frame)
        self.vl.setContentsMargins(0, 0, 0, 0)

        self.viewer = ViewerEditor()
        self.vl.addWidget(self.viewer, 0, 0, 10, 3)

        self.control = ControlsEditor()
        self.control.setMaximumHeight(120)
        self.vl.addWidget(self.control, 10, 0, 1, 2)

        self.viewer3D = ViewerEditor3D()
        self.viewer3D.setMaximumHeight(150)
        self.viewer3D.setMaximumWidth(200)
        self.vl.addWidget(self.viewer3D, 10, 2, 1, 1)

        expand(self)
        expand(self.frame)
        expand(self.viewer)

        layout.addWidget(self.frame)

        self.block_cut_plane = False
        self.block_propagation = False

        self.control.slider_propagation.setMinimum(1)
        self.control.slider_propagation.setMaximum(20)
        self.control.slider_propagation.setValue(5)
        self.control.sb_propagation.setMinimum(1)
        self.control.sb_propagation.setMaximum(20)
        self.control.sb_propagation.setValue(5)
        self.control.bp_z.setEnabled(False)
        self.control.bp_move.setEnabled(False)
        self.control.bp_fusion.setEnabled(False)
        self.control.bp_new_edit.setEnabled(False)

        self._create_connections()

    def _create_connections(self):
        self.control.bp_plus.pressed.connect(self.move_in_plane_plus)
        self.control.bp_moins.pressed.connect(self.move_in_plane_moins)
        self.control.bp_x.pressed.connect(self.switch_to_x_plan)
        self.control.bp_y.pressed.connect(self.switch_to_y_plan)
        self.control.bp_z.pressed.connect(self.switch_to_z_plan)
        self.control.slider_cut_plane.valueChanged.connect(self.move_in_plane)
        self.control.sb_cut_plane.valueChanged.connect(self.move_in_plane)
        self.control.bp_move.pressed.connect(self.set_mode_to_move)
        self.control.bp_select.pressed.connect(self.set_mode_to_select)
        self.control.bp_fusion.pressed.connect(self.fusion_consid_select_cells)
        self.control.bp_split.pressed.connect(self.split_considered_cell)
        self.control.slider_propagation.valueChanged.connect(self.set_propagation)
        self.control.sb_propagation.valueChanged.connect(self.set_propagation)
        self.control.bp_save.pressed.connect(self.apply_change_to_segmentation)
        self.control.bp_new_edit.pressed.connect(self.edit_new_cell)
        self.viewer.interactor.AddObserver("CellSelected", self.cell_selected)

    def resizeEvent(self, *args, **kwargs):
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)

    def set_data(self, intensity_mat, segmented_mat, label):
        """
        a method to pass the parameter needed by the viewer and his interactor
        """
        self.polydata = self.viewer.set_data(intensity_mat, segmented_mat, label)
        self.viewer3D.set_poly(self.polydata)
        self.set_slider_spinbox()
        self.show()

    def move_in_plane_plus(self):
        value = self.control.slider_cut_plane.sliderPosition()
        self.move_in_plane(value + 1)

    def move_in_plane_moins(self):
        value = self.control.slider_cut_plane.sliderPosition()
        self.move_in_plane(value - 1)

    def move_in_plane(self, value):
        """
        a method to connect the buttons, slider and spinbox to the fonction that move the plane along the axis
        """
        if not self.block_cut_plane:
            self.block_cut_plane = True
            self.control.sb_cut_plane.setValue(value)
            self.control.slider_cut_plane.setValue(value)
            self.viewer.move_in_plane(value)
            self.block_cut_plane = False
            self.viewer3D.set_plane(self.viewer.box, self.viewer.interactor.orientation, value)

    def switch_to_x_plan(self):
        """
        a method to connect the 'X' button to the change of axis
        """
        self.viewer.switch_to_x_plan()
        self.control.bp_x.setEnabled(False)
        self.control.bp_y.setEnabled(True)
        self.control.bp_z.setEnabled(True)
        self.set_slider_spinbox()

    def switch_to_y_plan(self):
        """
        a method to connect the 'Y' button to the change of axis
        """
        self.viewer.switch_to_y_plan()
        self.control.bp_y.setEnabled(False)
        self.control.bp_x.setEnabled(True)
        self.control.bp_z.setEnabled(True)
        self.set_slider_spinbox()

    def switch_to_z_plan(self):
        """
        a method to connect the 'Z' button to the change of axis
        """
        self.viewer.switch_to_z_plan()
        self.control.bp_z.setEnabled(False)
        self.control.bp_x.setEnabled(True)
        self.control.bp_y.setEnabled(True)
        self.set_slider_spinbox()

    def set_slider_spinbox(self):
        """
        a method to synchronize the slider and the spinbox dealing with the plane cut
        """
        cutplan = self.viewer.interactor.orientation
        value = self.viewer.plan[cutplan]
        self.block_cut_plane = True
        self.control.slider_cut_plane.setMinimum(self.viewer.box[cutplan * 2])
        self.control.slider_cut_plane.setMaximum(self.viewer.box[cutplan * 2 + 1])
        self.control.sb_cut_plane.setMinimum(self.viewer.box[cutplan * 2])
        self.control.sb_cut_plane.setMaximum(self.viewer.box[cutplan * 2 + 1])

        self.block_cut_plane = False
        self.control.slider_cut_plane.setSliderPosition(value)
        self.viewer3D.set_plane(self.viewer.box, cutplan, value)

    def set_mode(self, mode):
        self.viewer.interactor.mode = mode

    def set_mode_to_move(self):
        """
        a method to switch the mode to move : move allow the deplacement of the points of the cell
        """
        self.set_mode(0)
        self.control.bp_move.setEnabled(False)
        self.control.bp_select.setEnabled(True)
        #self.control.bp_fusion.setEnabled(False)

    def set_mode_to_select(self):
        """
        a method to switch the mode to select : select is used to select an other cell to fusion it or to remenber its id
        """
        self.set_mode(1)
        self.control.bp_select.setEnabled(False)
        #self.control.bp_fusion.setEnabled(True)
        self.control.bp_move.setEnabled(True)

    def fusion_consid_select_cells(self):
        """
        a method to connect the button 'fusion' to the 'fusion algo' of the interactor
        """
        self.polydata = self.viewer.fusion_consid_select_cells()
        self.viewer3D.clear()
        self.viewer3D.set_poly(self.polydata)
        self.set_slider_spinbox()
        self.viewer3D.render()

    def split_considered_cell(self):
        self.polydata = self.viewer.split_considered_cell()
        self.viewer3D.clear()
        self.viewer3D.set_poly(self.polydata)
        self.set_slider_spinbox()
        self.viewer3D.render()

    def set_propagation(self, value):
        """
        a method to connect the spinbox and slider to the propagation parameter
        """
        if not self.block_propagation:
            self.block_propagation = True
            self.control.sb_propagation.setValue(value)
            self.control.slider_propagation.setValue(value)
            self.viewer.set_propagation(value)
            self.block_propagation = False

    def apply_change_to_segmentation(self):
        """
        a method to connect save button to save fonction of viewer
        """
        array = self.viewer.apply_change_to_segmentation()
        self.segmentation_changed.emit(array)

    def cell_selected(self, obj, event):
        if self.viewer.interactor.selectedLabel == -1:
            self.control.bp_fusion.setEnabled(False)
            self.control.bp_new_edit.setEnabled(False)
        else:
            self.control.bp_fusion.setEnabled(True)
            self.control.bp_new_edit.setEnabled(True)

    def edit_new_cell(self):
        self.viewer.edit_new_cell()
        self.control.bp_fusion.setEnabled(False)
        self.control.bp_new_edit.setEnabled(False)


class ControlsEditor(QtGui.QWidget, Ui_panel_control_editor):

    """
    class that contains the ui of the Editor Controls Panel
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)


class ViewerEditor3D(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QtGui.QFrame()
        self.vl = QtGui.QVBoxLayout(self.frame)
        self.vl.setContentsMargins(0, 0, 0, 0)

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        expand(self)
        expand(self.frame)
        expand(self.vtkWidget)

        self.ren = vtk.vtkRenderer()  # vtk renderer
        self.vtkWidget.GetRenderWindow().SetSize(10, 10)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        layout.addWidget(self.frame)

        self.plane = vtk.vtkPlaneSource()
        mapper_plan = vtk.vtkPolyDataMapper()
        mapper_plan.ScalarVisibilityOff()
        mapper_plan.SetInputConnection(self.plane.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper_plan)
        self.ren.AddActor(actor)
        self.ren.ResetCamera()

        self.iren.Initialize()
        self.iren.Start()

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)

    def render(self):
        self.iren.Render()

    def clear(self):
        self.ren.RemoveActor(self.actor)

    def set_poly(self, polydata):
        mapper = vtk.vtkPolyDataMapper()
        mapper.ScalarVisibilityOff()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(0, 0, 1)
        self.ren.AddActor(self.actor)
        self.ren.ResetCamera()
        self.render()

    def set_plane(self, box, axis, position):
        origin = np.zeros(3)
        p1 = np.zeros(3)
        p2 = np.zeros(3)
        if axis == 0:
            x = 1
            y = 2
        elif axis == 1:
            x = 0
            y = 2
        else:
            x = 0
            y = 1
        origin[x] = box[2 * x] - 5
        p1[x] = box[2 * x] - 5
        p2[x] = box[2 * x + 1] + 5

        origin[y] = box[2 * y] - 5
        p1[y] = box[2 * y + 1] + 5
        p2[y] = box[2 * y] - 5

        origin[axis] = position
        p1[axis] = position
        p2[axis] = position
        self.plane.SetOrigin(origin)
        self.plane.SetPoint1(p1)
        self.plane.SetPoint2(p2)
        self.plane.Update()
        self.ren.ResetCamera()
        self.ren.Render()
        self.render()


class ViewerEditor(QtGui.QWidget):

    """
    class that implements the vtkviewer of the editor and pass information to the interactor
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QtGui.QFrame()
        self.vl = QtGui.QVBoxLayout(self.frame)
        self.vl.setContentsMargins(0, 0, 0, 0)

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        expand(self)
        expand(self.frame)
        expand(self.vtkWidget)

        self.ren = vtk.vtkRenderer()  # vtk renderer
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.picker = vtk.vtkPointPicker()
        self.picker.SetTolerance(0.005)
        self.picker.PickFromListOn()
        self.picker.InitializePickList()
        self.iren.SetPicker(self.picker)

        self.background_list = [0, 1]

        self.interactor = InteractorEditor2D()
        self.iren.SetInteractorStyle(self.interactor)
        self.interactor.SetCurrentRenderer(self.ren)

        layout.addWidget(self.frame)
        self.ren.ResetCamera()

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)

    def render(self):
        self.iren.Render()

    def set_segmented_matrix(self, segmented_mat):
        """
        give the segmented matrix to the one who need to know
        """
        self.segmented_matrix = segmented_mat
        self.interactor.matrix = self.segmented_matrix

    def set_intensity_matrix(self, intensity_mat):
        """
        give the intensity matrix to the one who need to know
        """
        self.intensity_matrix = intensity_mat
        bck = compute_image(self.intensity_matrix)
        self.interactor.background = bck
        self.picker.AddPickList(self.interactor.background)

    def set_label(self, lab):
        """
        compute the contour of the cell identify by label
        compute the neighboors and their contour
        """
        self.label = lab
        self.interactor.label = lab
        reader = matrix_to_image_reader('la', self.segmented_matrix, self.segmented_matrix.dtype)
        mat = reader.GetOutput()
        cellule = compute_points(mat, lab)
        box = cellule.GetBounds()
        plan = [int((box[i * 2] + box[i * 2 + 1]) / 2) for i in xrange(3)]
        labels = voisinage(self.segmented_matrix, cellule, lab, self.background_list)
        self.interactor.consideredCell = cellule
        self.plan = plan
        self.interactor.position = plan[2]
        self.interactor.background_list = self.background_list
        self.box = box
        self.interactor.polyList.clear()
        self.interactor.polyList = {labs: compute_points(mat, labs) for labs in labels}
        self.interactor.deletedLabel[:] = []
        return self.interactor.consideredCell

    def set_new_label(self, label):
        reader = matrix_to_image_reader('la', self.segmented_matrix, self.segmented_matrix.dtype)
        mat = reader.GetOutput()
        cellule = self.interactor.polyList[label]
        box = cellule.GetBounds()
        plan = [int((box[i * 2] + box[i * 2 + 1]) / 2) for i in xrange(3)]
        self.plan = plan
        self.interactor.position = plan[2]
        self.box = box
        labels = voisinage(self.segmented_matrix, cellule, label, self.background_list)
        for labs in labels:
            if labs == self.label:
                self.interactor.polyList[labs] = self.interactor.consideredCell
            elif labs not in self.interactor.polyList.keys():
                self.interactor.polyList[labs] = compute_points(mat, labs)
        self.label = label
        self.interactor.label = label
        self.interactor.consideredCell = cellule
        del self.interactor.polyList[label]
        for la in self.interactor.polyList.keys():
            if la not in labels:
                del self.interactor.polyList[la]
        self.interactor.deletedLabel[:] = []

    def set_data(self, intensity_mat, segmented_mat, label):
        self.set_segmented_matrix(segmented_mat)
        self.set_intensity_matrix(intensity_mat)
        polydata = self.set_label(label)
        self.iren.Initialize()
        self.iren.Start()
        self.interactor.refresh()
        return polydata

    def edit_new_cell(self):
        self.set_new_label(self.interactor.selectedLabel)
        self.interactor.refresh()

    def move_in_plane(self, value):
        self.interactor.position = value
        self.plan[self.interactor.orientation] = self.interactor.position
        self.interactor.refresh()

    def fusion_consid_select_cells(self):
        self.box = self.interactor.fusion_consid_select_cells()
        return self.interactor.consideredCell

    def split_considered_cell(self):
        self.box = self.interactor.split_considered_cell()
        return self.interactor.consideredCell

    def set_propagation(self, value):
        self.interactor.propagation = value

    def switch_to_x_plan(self):
        """
        method to reoriente the camera to face the yz plane
        actualise the orientation and position of the interactor
        """
        if (self.interactor.orientation == 2):
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0, 0, 1)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(180)
        elif (self.interactor.orientation == 1):
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-90)
        self.interactor.orientation = 0
        self.interactor.x = 1
        self.interactor.y = 2
        self.interactor.position = self.plan[self.interactor.orientation]
        self.interactor.refresh()

    def switch_to_y_plan(self):
        """
        method to reoriente the camera to face the xz plane
        actualise the orientation and position of the interactor
        """
        if (self.interactor.orientation == 2):
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(1, 0, 0)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0, 0, 1)
        elif (self.interactor.orientation == 0):
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
        self.interactor.orientation = 1
        self.interactor.x = 0
        self.interactor.y = 2
        self.interactor.position = self.plan[self.interactor.orientation]
        self.interactor.refresh()

    def switch_to_z_plan(self):
        """
        method to reoriente the camera to face the xy plane
        actualise the orientation and position of the interactor
        """
        if (self.interactor.orientation == 0):
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(1, 0, 0)
            #self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-60)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0, 0.5, 0)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
        elif (self.interactor.orientation == 1):
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(1, 0, 0)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0, 1, 0)
        self.interactor.orientation = 2
        self.interactor.x = 0
        self.interactor.y = 1
        self.interactor.position = self.plan[self.interactor.orientation]
        self.interactor.refresh()

    def apply_change_to_segmentation(self):
        """
        connect button save to the method that actually save things
        """
        array = self.interactor.apply_change_to_segmentation()
        return array


def voisinage(matrix, contour, label, background_list):
    """
    take as input a segmented matrix, a polydata and a label
    return a list of id corresponding to the neighboors of the polydata in the matrix
    """
    labels = list()
    for i in xrange(contour.GetNumberOfPoints()):
        coord = contour.GetPoint(i)
        xmin = int(coord[0] - 1)
        xmax = int(coord[0] + 1)
        ymin = int(coord[1] - 1)
        ymax = int(coord[1] + 1)
        zmin = int(coord[2] - 1)
        zmax = int(coord[2] + 1)
        x = int(coord[0])
        y = int(coord[1])
        z = int(coord[2])
        voisins = [(xmin, y, z), (x, ymin, z), (x, y, zmin), (xmax, y, z), (x, ymax, z), (x, y, zmax)]
        for voisin in voisins:
            lab = matrix[voisin[0], voisin[1], voisin[2]]
            if lab != label and not lab in labels:
                labels.append(lab)
        for bck in background_list:
            if bck in labels:
                labels.remove(bck)
    return labels


def cutplane(poly, orientation, position):
    """
    take as input a polydata, an axis (orientation) and the position along the axis (position)
    return the intersection of the polydata and the plane created by the axis and position
    """
    origine = np.zeros(3)
    origine[orientation] = position
    normal = np.zeros(3)
    normal[orientation] = 1

    plane = vtk.vtkPlane()
    plane.SetOrigin(origine)
    plane.SetNormal(normal)
    cutter = vtk.vtkCutter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        cutter.SetInput(poly)
    else:
        cutter.SetInputData(poly)
    cutter.SetCutFunction(plane)
    cutter.Update()
    return cutter


def get_contours(matrix, label):
    """
    take as input a segmented matrix and an id and return the contour of the polydata associated
    """
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)
    return compute_points(reader.GetOutput(), label)


def get_contours_with_scale(matrix, label, resolution):
    """
    take as input a segmented matrix and an id and return the contour of the polydata associated
    with the resolution passed in argument
    """
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)
    reader.SetDataSpacing(resolution)
    return compute_points(reader.GetOutput(), label)


def compute_points(matrix, label):
    contour = vtk.vtkDiscreteMarchingCubes()
    if vtk.VTK_MAJOR_VERSION <= 5:
        contour.SetInput(matrix)
    else:
        contour.SetInputData(matrix)
    contour.ComputeScalarsOn()
    contour.ComputeGradientsOn()
    contour.SetValue(0, label)
    contour.Update()
    return contour.GetOutput()


def get_contours2(matrix, label):
    """
    take as input a segmented matrix and a list of ids and return the contour of the polydata associated
    """
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)
    return compute_points2(reader.GetOutput(), label)


def compute_points2(matrix, label):
    contour = vtk.vtkDiscreteMarchingCubes()
    if vtk.VTK_MAJOR_VERSION <= 5:
        contour.SetInput(matrix)
    else:
        contour.SetInputData(matrix)
    contour.ComputeScalarsOff()
    contour.ComputeGradientsOff()
    for i, lab in enumerate(label):
        contour.SetValue(i, lab)
    contour.Update()
    return contour.GetOutput()


def compute_image(matrix):
    """
    take a matrix in input and return the vtkImageActor associated
    """
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)

    box = reader.GetDataExtent()
    lut = define_LUT(matrix)
    colors = vtk.vtkImageMapToColors()
    colors.SetInputConnection(reader.GetOutputPort())
    colors.SetLookupTable(lut)

    imgactor = vtk.vtkImageActor()
    if vtk.VTK_MAJOR_VERSION <= 5:
        imgactor.SetInput(colors.GetOutput())
    else:
        colors.Update()
        imgactor.SetInputData(colors.GetOutput())
    #imgactor.SetInputConnection(colors.GetOutputPort())
    imgactor.SetOpacity(0.2)
    imgactor.SetDisplayExtent(
        int(box[0]),
        int(box[1]),
        int(box[2]),
        int(box[3]),
        int((box[4] + box[5]) / 2),
        int((box[4] + box[5]) / 2))
    return imgactor


def define_LUT(image):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(image.max() + 1)
    lut.SetNumberOfColors(image.max() + 1)
    lut.SetRange(image.min(), image.max())
    lut.Build()
    return lut


def isnotInList(p, l):
    for i in l:
        if (i == p):
            return False
    return True


def is_shared_point(p1, poly1, poly2):
    """
    check if a point is shared by a other polydata, if yes, return its id in the second polydata
    """
    coord = poly1.GetPoint(p1)
    p2 = poly2.FindPoint(coord)
    coord2 = poly2.GetPoint(p2)
    if distance(coord, coord2) == 0:
        return p2
    else:
        return -1


def distance(p1, p2):
    """
    simple function that calculate the distance between two points
    """
    dist = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
    return dist


def intersection(box, boxx):
    """
    simple function to determine if two bounding box intersect each other
    """
    x = box[0] < boxx[1] and boxx[0] < box[1]
    y = box[2] < boxx[3] and boxx[2] < box[3]
    z = box[4] < boxx[5] and boxx[4] < box[5]
    return x and y and z


def delete_shared_borders_mieux(poly1, poly2):
    """
    better function to remove the shared bounderies between two polydata
    """
    for i in xrange(poly2.GetNumberOfCells()):
        idPoints = vtk.vtkIdList()
        poly2.GetCellPoints(i, idPoints)
        frontiere = True
        for j in xrange(idPoints.GetNumberOfIds()):
            if is_shared_point(idPoints.GetId(j), poly2, poly1) == -1:
                frontiere = False
                break
        if frontiere:
            poly2.DeleteCell(i)
    poly2.RemoveDeletedCells()
    poly2.Modified()

    for i in xrange(poly1.GetNumberOfCells()):
        idPoints = vtk.vtkIdList()
        poly1.GetCellPoints(i, idPoints)
        frontiere = True
        for j in xrange(idPoints.GetNumberOfIds()):
            if is_shared_point(idPoints.GetId(j), poly1, poly2) == -1:
                frontiere = False
                break
        if frontiere:
            poly1.DeleteCell(i)
    poly1.RemoveDeletedCells()
    poly1.Modified()


def is_poly_in_plan(poly, orientation, position):
    """
    simple function to determine if a plane intersect a polydata
    """
    box = poly.GetBounds()
    return box[orientation * 2] < position and box[orientation * 2 + 1] > position


def find_point_next(poly, point0, point1):
    """
    find point in next in the polydata
    require a polydata with lines/vertices cell only and point link to two lines and eventually one vertice
    """
    consid_cell = vtk.vtkIdList()
    plist1 = vtk.vtkIdList()
    plist2 = vtk.vtkIdList()
    poly.GetPointCells(point0, consid_cell)
    if consid_cell.GetNumberOfIds() == 2:
        poly.GetCellPoints(consid_cell.GetId(0), plist1)
        poly.GetCellPoints(consid_cell.GetId(1), plist2)
        if plist1.GetNumberOfIds() == 2 and plist2.GetNumberOfIds() == 2:
            if plist1.GetId(0) == point0:
                point2a = plist1.GetId(1)
            else:
                point2a = plist1.GetId(0)

            if plist2.GetId(0) == point0:
                point2b = plist2.GetId(1)
            else:
                point2b = plist2.GetId(0)

            if point2a == point1:
                return point2b
            else:
                return point2a
        else:
            return -1
    else:
        return -1


class SelectCellInteractorStyle (vtk.vtkInteractorStyleTrackballCamera):

    """
    class of interactor use to retrieve label of a cell in a cut_plane of a segmented matrix
    param : data : the segmented matrix
    """

    def __init__(self, parent=None):
        self.AddObserver("MiddleButtonPressEvent", self.MiddleButtonPressEvent)
        self.data = np.arange(1)
        self.resolution = [1, 1, 1]
        self.position = [0, 0, 0]

        self._ignored_labels = [0, 1]
        self._selected_label = None
        self.picker = vtk.vtkPointPicker()
        self.picker.SetTolerance(0.05)
        self.picker.PickFromListOn()

    def set_pick_list(self, imgactor):
        self.picker.AddPickList(imgactor)

    def ignore_labels(self, labels):
        self._ignored_labels = labels

    def selected_label(self):
        return self._selected_label

    def MiddleButtonPressEvent(self, obj, event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
        points = self.GetInteractor().GetPicker().GetPickedPositions()

        if points.GetNumberOfPoints() > 0:
            coord = points.GetPoint(0)
            if (self.GetInteractor().GetPicker().GetPointId() != -1):
                x = int((coord[0] / self.resolution[0] + self.position[0]))
                y = int((coord[1] / self.resolution[1] + self.position[1]))
                z = int((coord[2] / self.resolution[2] + self.position[2]))
                xm, ym, zm = self.data.shape
                if x < xm and y < ym and z < zm:
                    label = self.data[x, y, z]
                    # Background case
                    if label not in self._ignored_labels:
                        self._selected_label = label
                        self.InvokeEvent("LabelSelectedEvent")


class InteractorEditor(vtk.vtkInteractorStyle):

    """
    generic class of interactor to move points of a polydata on a plane
    param : poly : the polydata to edit
            plane : the plane limiting the deplacement
    """

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonReleaseEvent)
        self.selectedPoint = -1
        self.plane = None
        self.poly = None

    def set_plane(self, plan):
        if self.plane is not None:
            self.GetInteractor().GetPicker().DeletePickList(self.plane)
        self.plane = plan
        self.GetInteractor().GetPicker().AddPickList(plan)

    def LeftButtonPressEvent(self, obj, event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
        points = self.GetInteractor().GetPicker().GetPickedPositions()
        if points.GetNumberOfPoints() > 0:
            coord = np.zeros(3)
            points.GetPoint(0, coord)
            fp = self.poly.FindPoint(coord)
            co = np.zeros(3)
            self.poly.GetPoint(fp, co)
            if self.distance(co, coord) <= 1:
                self.selectedPoint = fp
            else:
                self.selectedPoint = -1

    def LeftButtonReleaseEvent(self, obj, event):
        if self.selectedPoint != -1:
            pos = self.GetInteractor().GetEventPosition()
            self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
            points = self.GetInteractor().GetPicker().GetPickedPositions()
            if points.GetNumberOfPoints() > 0:
                coord = np.zeros(3)
                points.GetPoint(0, coord)
                self.poly.GetPoints().SetPoint(self.selectedPoint, coord)
                self.poly.Modified()
                self.GetCurrentRenderer().ResetCamera()
                self.GetCurrentRenderer().Render()
                self.GetCurrentRenderer().GetRenderWindow().Render()

    def distance(self, p1, p2):
        dist = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
        return dist


class InteractorEditor2D (vtk.vtkInteractorStyle):

    """
    class of interactor used to move points of a polydata and to repercut the change to the polydatas adjacents
    move are in 3D but representation of the polydatas are in 2D
    param : consideredCell : polydata of the studied cell
            label : id of the studied cell
            polyList : dict for all neighboor : dict[label_neigh] = polydata_neigh
            background : imageactor of the intensity matrix
            matrix : matrix of the segmented image
            select_neighboor_mode : string to choose the method use to select the points to deplace
            select_move_mode : string to choose the method use to move the points
    """

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonReleaseEvent)
        self.AddObserver("MouseMoveEvent", self.MouseMoveEvent)
        self.AddObserver("KeyPressEvent", self.KeyPressEvent)

        self.consideredCell = vtk.vtkPolyData()
        self.polyList = dict()
        self.background = vtk.vtkImageActor()
        self.polyInPlan = list()
        self.matrix = []
        self.background_list = list()
        self.consid_cut = vtk.vtkPolyData()

        self.select_neighboor_mode = 'propagationSphere'
        self.select_move_mode = 'proportionality'

        self.x = 0
        self.y = 1
        self.orientation = 2
        self.position = 0
        self.mode = 0
        self.propagation = 5
        self.selectedPoint = -1
        self.selectedLabel = -1
        self.label = -1
        self.deletedLabel = list()
        self.consid_point = -1

        origine = np.zeros(3)
        origine[self.orientation] = self.position
        normal = np.zeros(3)
        normal[self.orientation] = 1

        self.plane = vtk.vtkPlane()
        self.plane.SetOrigin(origine)
        self.plane.SetNormal(normal)

        self.grab_mode = False

        self.sphere_propagation = vtk.vtkSphereSource()
        self.sphere_propagation.SetRadius(self.propagation)
        subdivision = vtk.vtkButterflySubdivisionFilter()
        subdivision.SetInputConnection(self.sphere_propagation.GetOutputPort())
        subdivision.SetNumberOfSubdivisions(2)

        spheremap = vtk.vtkPolyDataMapper()

        if vtk.VTK_MAJOR_VERSION <= 5:
            spheremap.SetInputConnection(subdivision.GetOutputPort())
        else:
            self.cutter_sphere = vtk.vtkCutter()
            self.cutter_sphere.SetInputConnection(subdivision.GetOutputPort())
            self.cutter_sphere.SetCutFunction(self.plane)
            spheremap.SetInputConnection(self.cutter_sphere.GetOutputPort())

        self.sphere_actor = vtk.vtkActor()
        self.sphere_actor.SetMapper(spheremap)
        self.sphere_actor.VisibilityOff()

        self.points_to_move = dict()

    def refresh(self):
        """
        method to refresh the renderer after a change
        """
        self.GetCurrentRenderer().RemoveAllViewProps()

        origine = np.zeros(3)
        origine[self.orientation] = self.position
        normal = np.zeros(3)
        normal[self.orientation] = 1
        self.plane.SetOrigin(origine)
        self.plane.SetNormal(normal)

        #self.cutter_sphere.Update()
        self.refresh_poly()
        self.refresh_background()
        #self.GetCurrentRenderer().AddActor(self.move_actor)
        self.GetCurrentRenderer().AddActor(self.sphere_actor)
        self.GetCurrentRenderer().ResetCamera()
        self.GetCurrentRenderer().Render()
        self.GetCurrentRenderer().GetRenderWindow().Render()

    def refresh_poly(self):
        """
        compute the poly that's on the plane and add the actor of their cutplane to the renderer
        """
        self.polyInPlan = [
            lab for lab,
            poly in self.polyList.items(
            ) if is_poly_in_plan(
                poly,
                self.orientation,
                self.position)]
        for lab in self.polyInPlan:
            cutter = vtk.vtkCutter()
            if vtk.VTK_MAJOR_VERSION <= 5:
                cutter.SetInput(self.polyList[lab])
            else:
                cutter.SetInputData(self.polyList[lab])
            cutter.SetCutFunction(self.plane)

            """cutter.Update()
            cutplan = cutter.GetOutput()
            verts = vtk.vtkCellArray()
            for i in xrange(cutplan.GetNumberOfPoints()):
                verts.InsertNextCell(1)
                verts.InsertCellPoint(i)
            cutplan.SetVerts(verts)"""

            newmap = vtk.vtkPolyDataMapper()
            newmap.SetInputConnection(cutter.GetOutputPort())

            newmap.ScalarVisibilityOff()
            newact = vtk.vtkActor()
            newact.SetMapper(newmap)
            newact.GetProperty().SetPointSize(3)
            if lab == self.selectedLabel:
                newact.GetProperty().SetColor(0, 1, 0)
            else:
                newact.GetProperty().SetColor(0, 0, 1)
            self.GetCurrentRenderer().AddActor(newact)
        cons = vtk.vtkCutter()
        if vtk.VTK_MAJOR_VERSION <= 5:
            cons.SetInput(self.consideredCell)
        else:
            cons.SetInputData(self.consideredCell)
        cons.SetCutFunction(self.plane)
        cons.Update()
        cut_point_line = cons.GetOutput()
        verts = vtk.vtkCellArray()
        for i in xrange(cut_point_line.GetNumberOfPoints()):
            verts.InsertNextCell(1)
            verts.InsertCellPoint(i)
        cut_point_line.SetVerts(verts)
        self.consid_cut = cut_point_line
        considmap = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            considmap.SetInput(self.consid_cut)
        else:
            considmap.SetInputData(self.consid_cut)

        considmap.ScalarVisibilityOff()
        considact = vtk.vtkActor()
        considact.SetMapper(considmap)
        considact.GetProperty().SetColor(1, 0, 0)
        considact.GetProperty().SetPointSize(3)
        self.GetCurrentRenderer().AddActor(considact)

    def refresh_background(self):
        """
        compute the new extent of the background
        """
        bounds = np.zeros(6, dtype=np.int)
        self.GetCurrentRenderer().ComputeVisiblePropBounds(bounds)
        for lim in bounds:
            lim = int(lim)
        bounds[self.orientation * 2] = self.position
        bounds[self.orientation * 2 + 1] = self.position
        self.background.SetDisplayExtent(bounds)
        self.background.Modified()
        self.GetCurrentRenderer().AddActor(self.background)

    def LeftButtonPressEvent(self, obj, event):
        """
        event triggered by pressing the left button of the mouse
        retrieve the coordinates of the cursor in the scene
        if mode is on move (=0) the interactor find the point cliqued
        elif mode is on select(=1) the interactor find the label of the cell cliqued
        """
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
        points = self.GetInteractor().GetPicker().GetPickedPositions()
        if points.GetNumberOfPoints() > 0:
            coord = points.GetPoint(0)
            if self.mode == 0:
                fp = self.consideredCell.FindPoint(coord)
                co = self.consideredCell.GetPoint(fp)
                if distance(co, coord) <= 1:
                    self.selectedPoint = fp
                    self.consid_point = self.consid_cut.FindPoint(coord)

                    self.find_point_to_move(coord)

                    """self.sphere_propagation.SetCenter(coord)
                    self.sphere_propagation.SetRadius(self.propagation)
                    self.sphere_propagation.Update()
                    self.sphere_actor.VisibilityOn()

                    selectEnclosed = vtk.vtkSelectEnclosedPoints()
                    if vtk.VTK_MAJOR_VERSION <= 5:
                        selectEnclosed.SetInput(self.consid_cut)
                    else:
                        selectEnclosed.SetInputData(self.consid_cut)
                    selectEnclosed.SetSurfaceConnection(self.sphere_propagation.GetOutputPort())
                    selectEnclosed.Update()

                    self.points_to_move.clear()

                    for i in xrange(self.consid_cut.GetNumberOfPoints()):
                        if selectEnclosed.IsInside(i):
                            coordi = self.consid_cut.GetPoint(i)
                            dist = distance(coord, coordi)
                            self.points_to_move[i] = dist / self.propagation"""

                    self.grab_mode = True

                    self.GetCurrentRenderer().Render()
                    self.GetCurrentRenderer().GetRenderWindow().Render()
                else:
                    self.selectedPoint = -1
                    self.consid_point = -1
            elif self.mode == 1:
                for label, poly in self.polyList.items():
                    points = vtk.vtkPoints()
                    points.InsertNextPoint(coord)
                    polypoint = vtk.vtkPolyData()
                    polypoint.SetPoints(points)
                    selectEnclosed = vtk.vtkSelectEnclosedPoints()
                    if vtk.VTK_MAJOR_VERSION <= 5:
                        selectEnclosed.SetInput(polypoint)
                        selectEnclosed.SetSurface(poly)
                    else:
                        selectEnclosed.SetInputData(polypoint)
                        selectEnclosed.SetSurfaceData(poly)
                    selectEnclosed.Update()
                    if selectEnclosed.IsInside(0):
                        self.selectedLabel = label
                        break
                    else:
                        self.selectedLabel = -1
                print self.selectedLabel
                self.InvokeEvent("CellSelected")
                self.refresh()

    # TODO : trouver une meilleure formule de deplacement que la proportionnalite

    def LeftButtonReleaseEvent(self, obj, event):
        """
        event triggered by the left button mouse released
        if mode is on move (=0) :
            the interactor retrieved the position of the cursor and move the selectedPoint to this location
            move all the point in a self.propagation radius depending of a proportionality equation in fonction of the distance
        elif nothing
        """
        if self.mode == 0:
            if (self.selectedPoint != -1):
                self.grab_mode = False
                pos = self.GetInteractor().GetEventPosition()
                self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
                pw = self.GetInteractor().GetPicker().GetPickPosition()

                self.move_point(pw)

                """oldcoord = self.consideredCell.GetPoint(self.selectedPoint)

                newcoord = np.zeros(3)
                newcoord[self.x] = pw[self.x]
                newcoord[self.y] = pw[self.y]
                newcoord[self.orientation] = self.position
                transx = (oldcoord[self.x] - newcoord[self.x])
                transy = (oldcoord[self.y] - newcoord[self.y])

                selectEnclosed = vtk.vtkSelectEnclosedPoints()
                if vtk.VTK_MAJOR_VERSION <= 5:
                    selectEnclosed.SetInput(self.consideredCell)
                    selectEnclosed.SetSurface(self.sphere_propagation.GetOutput())
                else:
                    selectEnclosed.SetInputData(self.consideredCell)
                    selectEnclosed.SetSurfaceData(self.sphere_propagation.GetOutput())
                selectEnclosed.Update()

                for i in xrange(self.consideredCell.GetNumberOfPoints()):
                    if selectEnclosed.IsInside(i):
                        coord = self.consideredCell.GetPoint(i)
                        dist = distance(oldcoord, coord)
                        new_coord = np.zeros(3)
                        new_coord[self.x] = coord[self.x] - (transx - transx * dist / self.propagation)
                        new_coord[self.y] = coord[self.y] - (transy - transy * dist / self.propagation)

                        new_coord[self.orientation] = coord[self.orientation]
                        self.consideredCell.GetPoints().SetPoint(i, new_coord)
                        self.consideredCell.Modified()

                for poly in self.polyList.values():
                    box = poly.GetBounds()
                    boxx = self.sphere_propagation.GetOutput().GetBounds()
                    if intersection(box, boxx):
                        selectEnclosed = vtk.vtkSelectEnclosedPoints()
                        if vtk.VTK_MAJOR_VERSION <= 5:
                            selectEnclosed.SetInput(poly)
                            selectEnclosed.SetSurface(self.sphere_propagation.GetOutput())
                        else:
                            selectEnclosed.SetInputData(poly)
                            selectEnclosed.SetSurfaceData(self.sphere_propagation.GetOutput())
                        selectEnclosed.Update()
                        for i in xrange(poly.GetNumberOfPoints()):
                            if selectEnclosed.IsInside(i):
                                coord = poly.GetPoint(i)
                                dist = distance(oldcoord, coord)
                                new_coord = np.zeros(3)
                                new_coord[self.x] = coord[self.x] - (transx - transx * dist / self.propagation)
                                new_coord[self.y] = coord[self.y] - (transy - transy * dist / self.propagation)

                                new_coord[self.orientation] = coord[self.orientation]
                                poly.GetPoints().SetPoint(i, new_coord)
                                poly.Modified()"""
                #self.list_action.append(['translation',newcoord,transx,transy])
                #self.move_actor.VisibilityOff()
                self.sphere_actor.VisibilityOff()
                self.refresh()

    def MouseMoveEvent(self, obj, event):
        if self.grab_mode:
            if (self.selectedPoint != -1):
                pos = self.GetInteractor().GetEventPosition()
                self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
                pw = self.GetInteractor().GetPicker().GetPickPosition()

                oldcoord = self.consid_cut.GetPoint(self.consid_point)

                newcoord = np.zeros(3)
                newcoord[self.x] = pw[self.x]
                newcoord[self.y] = pw[self.y]
                newcoord[self.orientation] = self.position
                transx = (oldcoord[self.x] - newcoord[self.x])
                transy = (oldcoord[self.y] - newcoord[self.y])

                for i, ratio in self.points_to_move.items():
                    coord = self.consid_cut.GetPoint(i)
                    new_coord = np.zeros(3)
                    new_coord[self.x] = coord[self.x] - (transx - transx * ratio)
                    new_coord[self.y] = coord[self.y] - (transy - transy * ratio)
                    new_coord[self.orientation] = coord[self.orientation]
                    self.consid_cut.GetPoints().SetPoint(i, new_coord)
                    self.consid_cut.Modified()

                self.GetCurrentRenderer().Render()
                self.GetCurrentRenderer().GetRenderWindow().Render()

    def KeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeyCode()
        if key == 'z':
            print "wip"

    def find_point_to_move(self, coord):
        if self.select_neighboor_mode == 'propagationSphere':
            self.sphere_propagation.SetCenter(coord)
            self.sphere_propagation.SetRadius(self.propagation)
            self.sphere_propagation.Update()
            self.sphere_actor.VisibilityOn()

            selectEnclosed = vtk.vtkSelectEnclosedPoints()
            if vtk.VTK_MAJOR_VERSION <= 5:
                selectEnclosed.SetInput(self.consid_cut)
            else:
                selectEnclosed.SetInputData(self.consid_cut)
            selectEnclosed.SetSurfaceConnection(self.sphere_propagation.GetOutputPort())
            selectEnclosed.Update()

            self.points_to_move.clear()

            for i in xrange(self.consid_cut.GetNumberOfPoints()):
                if selectEnclosed.IsInside(i):
                    coordi = self.consid_cut.GetPoint(i)
                    dist = distance(coord, coordi)
                    self.points_to_move[i] = dist / self.propagation

    def move_point(self, pw):
        if self.select_move_mode == 'proportionality':
            oldcoord = self.consideredCell.GetPoint(self.selectedPoint)

            newcoord = np.zeros(3)
            newcoord[self.x] = pw[self.x]
            newcoord[self.y] = pw[self.y]
            newcoord[self.orientation] = self.position
            transx = (oldcoord[self.x] - newcoord[self.x])
            transy = (oldcoord[self.y] - newcoord[self.y])
            selectEnclosed = vtk.vtkSelectEnclosedPoints()
            if vtk.VTK_MAJOR_VERSION <= 5:
                selectEnclosed.SetInput(self.consideredCell)
                selectEnclosed.SetSurface(self.sphere_propagation.GetOutput())
            else:
                selectEnclosed.SetInputData(self.consideredCell)
                selectEnclosed.SetSurfaceData(self.sphere_propagation.GetOutput())
            selectEnclosed.Update()

            for i in xrange(self.consideredCell.GetNumberOfPoints()):
                if selectEnclosed.IsInside(i):
                    coord = self.consideredCell.GetPoint(i)
                    dist = distance(oldcoord, coord)
                    new_coord = np.zeros(3)
                    new_coord[self.x] = coord[self.x] - (transx - transx * dist / self.propagation)
                    new_coord[self.y] = coord[self.y] - (transy - transy * dist / self.propagation)

                    new_coord[self.orientation] = coord[self.orientation]
                    self.consideredCell.GetPoints().SetPoint(i, new_coord)
                    self.consideredCell.Modified()

            for poly in self.polyList.values():
                box = poly.GetBounds()
                boxx = self.sphere_propagation.GetOutput().GetBounds()
                if intersection(box, boxx):
                    selectEnclosed = vtk.vtkSelectEnclosedPoints()
                    if vtk.VTK_MAJOR_VERSION <= 5:
                        selectEnclosed.SetInput(poly)
                        selectEnclosed.SetSurface(self.sphere_propagation.GetOutput())
                    else:
                        selectEnclosed.SetInputData(poly)
                        selectEnclosed.SetSurfaceData(self.sphere_propagation.GetOutput())
                    selectEnclosed.Update()
                    for i in xrange(poly.GetNumberOfPoints()):
                        if selectEnclosed.IsInside(i):
                            coord = poly.GetPoint(i)
                            dist = distance(oldcoord, coord)
                            new_coord = np.zeros(3)
                            new_coord[self.x] = coord[self.x] - (transx - transx * dist / self.propagation)
                            new_coord[self.y] = coord[self.y] - (transy - transy * dist / self.propagation)
                            new_coord[self.orientation] = coord[self.orientation]
                            poly.GetPoints().SetPoint(i, new_coord)
                            poly.Modified()

    def fusion_consid_select_cells(self):
        """
        append the consideredCell and the selectedLabel one together,
        remove the bounderies between them,
        and add the selectedLabel's neighboords to the polyList
        """
        #if self.mode == 1 and self.selectedLabel != -1 and self.selectedLabel not in self.deletedLabel:
        if self.selectedLabel != -1 and self.selectedLabel not in self.deletedLabel:
            fusionPoly = self.polyList[self.selectedLabel]
            delete_shared_borders_mieux(self.consideredCell, fusionPoly)
            labels = voisinage(self.matrix, fusionPoly, self.selectedLabel, self.background_list)
            if self.label in labels:
                labels.remove(self.label)
            for delLab in self.deletedLabel:
                if delLab in labels:
                    labels.remove(delLab)
            reader = matrix_to_image_reader('la', self.matrix, self.matrix.dtype)
            mat = reader.GetOutput()
            for labs in labels:
                if labs not in self.polyList:
                    self.polyList[labs] = compute_points(mat, labs)
            append = vtk.vtkAppendPolyData()
            if vtk.VTK_MAJOR_VERSION <= 5:
                append.AddInput(self.consideredCell)
                append.AddInput(fusionPoly)
            else:
                append.AddInputData(self.consideredCell)
                append.AddInputData(fusionPoly)
            append.Update()

            cleaning = vtk.vtkCleanPolyData()
            cleaning.SetInputConnection(append.GetOutputPort())
            cleaning.PointMergingOn()
            cleaning.SetTolerance(0.0)
            cleaning.Update()

            del self.consideredCell
            self.consideredCell = cleaning.GetOutput()
            del self.polyList[self.selectedLabel]
            self.deletedLabel.append(self.selectedLabel)
            self.selectedLabel = -1
            self.refresh()
            box = np.zeros(6)
            self.consideredCell.GetBounds(box)
            return box

    def split_considered_cell(self):

        clipper = vtk.vtkClipPolyData()
        if vtk.VTK_MAJOR_VERSION <= 5:
            origine = np.zeros(3)
            origine[self.orientation] = self.position
            normal = np.zeros(3)
            normal[self.orientation] = 1
            plane2 = vtk.vtkPlane()
            plane2.SetNormal(normal)
            plane2.SetOrigin(origine)

            clipper.SetInput(self.consideredCell)
            clipper.SetClipFunction(plane2)
        else:
            clipper.SetInputData(self.consideredCell)
            clipper.SetClipFunction(self.plane)

        clipper.GenerateClippedOutputOn()
        clipper.Update()

        feat = vtk.vtkFeatureEdges()
        feat.SetInputConnection(clipper.GetOutputPort())

        feat.BoundaryEdgesOn()
        feat.FeatureEdgesOff()
        feat.NonManifoldEdgesOff()
        feat.ManifoldEdgesOff()

        strip = vtk.vtkStripper()
        strip.SetInputConnection(feat.GetOutputPort())
        strip.Update()

        poly = vtk.vtkPolyData()
        poly.SetPoints(strip.GetOutput().GetPoints())
        poly.SetPolys(strip.GetOutput().GetLines())

        triangle = vtk.vtkTriangleFilter()
        if vtk.VTK_MAJOR_VERSION <= 5:
            triangle.SetInput(poly)
        else:
            triangle.SetInputData(poly)

        cleaning = vtk.vtkCleanPolyData()
        cleaning.SetInputConnection(triangle.GetOutputPort())
        cleaning.PointMergingOn()
        cleaning.SetTolerance(0.0)
        #cleaning.Update()

        subdivisionFilter = vtk.vtkLoopSubdivisionFilter()
        subdivisionFilter.SetNumberOfSubdivisions(3)
        subdivisionFilter.SetInputConnection(cleaning.GetOutputPort())
        #subdivisionFilter.Update()

        append0 = vtk.vtkAppendPolyData()
        append0.AddInputConnection(clipper.GetOutputPort(0))
        append0.AddInputConnection(subdivisionFilter.GetOutputPort())
        append0.Update()

        cleaning0 = vtk.vtkCleanPolyData()
        cleaning0.SetInputConnection(append0.GetOutputPort())
        cleaning0.PointMergingOn()
        cleaning0.SetTolerance(0.0)
        cleaning0.Update()

        append1 = vtk.vtkAppendPolyData()
        append1.AddInputConnection(clipper.GetOutputPort(1))
        append1.AddInputConnection(subdivisionFilter.GetOutputPort())
        append1.Update()

        cleaning1 = vtk.vtkCleanPolyData()
        cleaning1.SetInputConnection(append1.GetOutputPort())
        cleaning1.PointMergingOn()
        cleaning1.SetTolerance(0.0)
        cleaning1.Update()

        del self.consideredCell
        self.consideredCell = cleaning0.GetOutput()
        label_in_matrix = np.setdiff1d(self.matrix, [0])
        for i in xrange(2, 5000):
            if i not in label_in_matrix:
                new_label = i
                break
        print new_label
        self.polyList[new_label] = cleaning1.GetOutput()

        self.refresh()
        box = np.zeros(6)
        self.consideredCell.GetBounds(box)
        return box

    def apply_change_to_segmentation(self):

        reader = matrix_to_image_reader('la', self.matrix, self.matrix.dtype)
        img = reader.GetOutput()

        for lab, poly in self.polyList.items():
            pol2stenc = vtk.vtkPolyDataToImageStencil()
            pol2stenc.SetTolerance(0)
            if vtk.VTK_MAJOR_VERSION <= 5:
                pol2stenc.SetInput(poly)
            else:
                pol2stenc.SetInputData(poly)
            pol2stenc.Update()
            imgstenc = vtk.vtkImageStencil()
            if vtk.VTK_MAJOR_VERSION <= 5:
                imgstenc.SetInput(img)
                imgstenc.SetStencil(pol2stenc.GetOutput())
            else:
                imgstenc.SetInputData(img)
                imgstenc.SetStencilConnection(pol2stenc.GetOutputPort())
            imgstenc.ReverseStencilOn()
            imgstenc.SetBackgroundValue(lab)
            imgstenc.Update()
            img = imgstenc.GetOutput()

        pol2stenc = vtk.vtkPolyDataToImageStencil()
        pol2stenc.SetTolerance(0)

        if vtk.VTK_MAJOR_VERSION <= 5:
            pol2stenc.SetInput(self.consideredCell)
        else:
            pol2stenc.SetInputData(self.consideredCell)
        pol2stenc.Update()

        imgstenc = vtk.vtkImageStencil()
        if vtk.VTK_MAJOR_VERSION <= 5:
            imgstenc.SetInput(img)
            imgstenc.SetStencil(pol2stenc.GetOutput())
        else:
            imgstenc.SetInputData(img)
            imgstenc.SetStencilConnection(pol2stenc.GetOutputPort())
        imgstenc.ReverseStencilOn()
        imgstenc.SetBackgroundValue(self.label)
        imgstenc.Update()

        typee = img.GetScalarType()
        if typee == VTK_SIGNED_CHAR:
            ty = 'b'
        elif typee == VTK_UNSIGNED_CHAR:
            ty = 'B'
        elif typee == VTK_SHORT:
            ty = 'h'
        elif typee == VTK_UNSIGNED_SHORT:
            ty = 'H'
        elif typee == VTK_INT:
            ty = 'i'
        elif typee == VTK_UNSIGNED_INT:
            ty = 'I'
        elif typee == VTK_INT:
            ty = 'f'
        elif typee == VTK_DOUBLE:
            ty = 'd'

        export = vtk.vtkImageExport()
        export.SetInputConnection(imgstenc.GetOutputPort())

        if vtk.VTK_MAJOR_VERSION <= 5:
            extent = imgstenc.GetOutput().GetWholeExtent()
        else:
            extent = imgstenc.GetOutput().GetExtent()
        dim = (extent[5] - extent[4] + 1, extent[3] - extent[2] + 1, extent[1] - extent[0] + 1)
        array = np.zeros(dim, ty)
        export.Export(array)
        array = array.transpose()
        bounds = np.zeros(6)
        self.consideredCell.GetBounds(bounds)
        for x, arrayx in enumerate(array[int(bounds[0]):int(bounds[1]) + 1]):
            for y, arrayy in enumerate(arrayx[int(bounds[2]):int(bounds[3]) + 1]):
                for z, arrayz in enumerate(arrayy[int(bounds[4]):int(bounds[5]) + 1]):
                    if arrayz in self.deletedLabel:
                        array[int(bounds[0]) + x][int(bounds[2]) + y][int(bounds[4]) + z] = self.label
        return array

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ew = EditorWindow()
    ew.show()
    sys.exit(app.exec_())
