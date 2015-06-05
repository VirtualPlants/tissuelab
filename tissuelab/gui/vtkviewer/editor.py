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
from openalea.vpltk.qt import QtGui
from tissuelab.gui.vtkviewer.qvtkrenderwindowinteractor import QVTKRenderWindowInteractor
from vtk_utils import matrix_to_image_reader
from tissuelab.gui.vtkviewer.designer._panel_control_editor import Ui_panel_control_editor
#from openalea.image.serial.all import imread
#from openalea.image.spatial_image import SpatialImage
from time import time

def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

class EditorWindow(QtGui.QWidget):
    """
    An EditorWindow is a class that defined the popup that open when you edit a cell. 
    It contains a widget with control panel and a vtk viewer
    To initialize the vtkviewer, you need to run set_data
    """
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
               
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.frame = QtGui.QFrame()
        self.vl = QtGui.QVBoxLayout(self.frame)
        self.vl.setContentsMargins(0, 0, 0, 0)
        
        self.viewer = ViewerEditor()
        self.vl.addWidget(self.viewer)
        
        self.control = ControlsEditor()
        self.vl.addWidget(self.control)
        
        expand(self)
        expand(self.frame)
        expand(self.viewer)
        
        layout.addWidget(self.frame)
        
        self.block_cut_plane = False
        self.block_propagation = False
        
        self.control.slider_propagation.setMinimum(1)            
        self.control.slider_propagation.setMaximum(40) 
        self.control.slider_propagation.setValue(5)
        self.control.sb_propagation.setMinimum(1)           
        self.control.sb_propagation.setMaximum(40)
        self.control.sb_propagation.setValue(5)
        
        self.control.bp_z.setEnabled(False)
        self.control.bp_move.setEnabled(False)
        
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
        self.control.slider_propagation.valueChanged.connect(self.set_propagation)
        self.control.sb_propagation.valueChanged.connect(self.set_propagation)
        
        
    def resizeEvent(self, *args, **kwargs):
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)
        
    def set_data(self, intensity_mat, segmented_mat,label):
        self.viewer.set_data(intensity_mat, segmented_mat,label)
        self.set_slider_spinbox()
        self.show()
        
    def move_in_plane_plus(self):
        value = self.control.slider_cut_plane.sliderPosition()
        self.move_in_plane(value+1)
        
    def move_in_plane_moins(self):
        value = self.control.slider_cut_plane.sliderPosition()
        self.move_in_plane(value-1)
        
    def move_in_plane(self, value):
        if not self.block_cut_plane:
            self.block_cut_plane = True
            self.control.sb_cut_plane.setValue(value)
            self.control.slider_cut_plane.setValue(value)
            self.viewer.move_in_plane(value)
            self.block_cut_plane = False     
        
    def switch_to_x_plan(self):
        self.viewer.switch_to_x_plan()
        self.control.bp_x.setEnabled(False)
        self.control.bp_y.setEnabled(True)
        self.control.bp_z.setEnabled(True)
        self.set_slider_spinbox()
    
    def switch_to_y_plan(self):
        self.viewer.switch_to_y_plan()
        self.control.bp_y.setEnabled(False)
        self.control.bp_x.setEnabled(True)
        self.control.bp_z.setEnabled(True)
        self.set_slider_spinbox()
        
    def switch_to_z_plan(self):
        self.viewer.switch_to_z_plan()
        self.control.bp_z.setEnabled(False)
        self.control.bp_x.setEnabled(True)
        self.control.bp_y.setEnabled(True)
        self.set_slider_spinbox()

    def set_slider_spinbox(self):
        cutplan = self.viewer.interactor.orientation
        value = self.viewer.plan[cutplan]
        self.block_cut_plane = True
        self.control.slider_cut_plane.setMinimum(self.viewer.box[cutplan*2])            
        self.control.slider_cut_plane.setMaximum(self.viewer.box[cutplan*2+1]) 
        self.control.sb_cut_plane.setMinimum(self.viewer.box[cutplan*2])           
        self.control.sb_cut_plane.setMaximum(self.viewer.box[cutplan*2+1])
        self.block_cut_plane = False
        self.control.slider_cut_plane.setSliderPosition(value)
        
    def set_mode(self,mode):
        self.viewer.interactor.mode = mode
        
    def set_mode_to_move(self):
        self.set_mode(0)
        self.control.bp_move.setEnabled(False)
        self.control.bp_select.setEnabled(True)
        
    def set_mode_to_select(self):
        self.set_mode(1)
        self.control.bp_select.setEnabled(False)
        self.control.bp_move.setEnabled(True)
        
    def fusion_consid_select_cells(self):
        self.viewer.fusion_consid_select_cells()
        
    def set_propagation(self, value):
        if not self.block_propagation:
            self.block_propagation = True
            self.control.sb_propagation.setValue(value)
            self.control.slider_propagation.setValue(value)
            self.viewer.set_propagation(value)
            self.block_propagation = False 
        

class ControlsEditor(QtGui.QWidget,Ui_panel_control_editor):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

class ViewerEditor(QtGui.QWidget):

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

        self.picker = vtk.vtkCellPicker()
        self.picker.SetTolerance(0.005)
        self.picker.PickFromListOn()
        self.picker.InitializePickList()
        self.iren.SetPicker(self.picker)
        
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
        
    def set_segmented_matrix(self,segmented_mat):
        self.segmented_matrix = segmented_mat
        self.interactor.matrix = self.segmented_matrix
        
    def set_intensity_matrix(self,intensity_mat):
        self.intensity_matrix = intensity_mat
        bck = compute_image(self.intensity_matrix)
        self.interactor.background = bck
        self.picker.AddPickList(self.interactor.background)
        
    def set_label(self,lab):
        self.label = lab
        self.interactor.label = lab
        reader = matrix_to_image_reader('la', self.segmented_matrix, self.segmented_matrix.dtype)
        mat = reader.GetOutput()
        cellule = compute_points(mat, lab)
        box = np.zeros(6)
        cellule.GetBounds(box)
        plan = [int((box[i*2] + box[i*2+1]) / 2) for i in xrange(3)]
        labels = voisinage(self.segmented_matrix, cellule, lab)
        self.interactor.consideredCell = cellule
        self.plan = plan
        self.interactor.position = plan[2]
        self.box = box
        self.interactor.polyList.clear()
        self.interactor.polyList = {labs:compute_points(mat,labs) for labs in labels}
    
    def set_data(self, intensity_mat, segmented_mat,label):
        self.set_segmented_matrix(segmented_mat)
        self.set_intensity_matrix(intensity_mat)
        self.set_label(label)
        self.interactor.refresh() 
    
    def move_in_plane(self, value):
        self.interactor.position = value
        self.plan[self.interactor.orientation] = self.interactor.position
        self.interactor.refresh()
    
    def fusion_consid_select_cells(self):
        self.interactor.fusion_consid_select_cells()
        
    def set_propagation(self,value):
        self.interactor.propagation = value
            
    def switch_to_x_plan(self):
        if (self.interactor.orientation == 2):
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0,0,1)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(180)
        elif (self.interactor.orientation == 1):
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-90)
        self.interactor.orientation = 0
        self.interactor.x = 1
        self.interactor.y = 2
        self.interactor.position = self.plan[self.interactor.orientation]
        self.interactor.refresh()       
    
    def switch_to_y_plan(self):
        if (self.interactor.orientation == 2):
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(1,0,0)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0,0,1)
        elif (self.interactor.orientation == 0):
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
        self.interactor.orientation = 1
        self.interactor.x = 0
        self.interactor.y = 2
        self.interactor.position = self.plan[self.interactor.orientation]
        self.interactor.refresh()
            
    def switch_to_z_plan(self):
        if (self.interactor.orientation == 0):
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(1,0,0)
            #self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-60)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0,0.5,0)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(90)
        elif (self.interactor.orientation == 1):
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(1,0,0)
            self.interactor.GetCurrentRenderer().GetActiveCamera().Azimuth(-90)
            self.interactor.GetCurrentRenderer().GetActiveCamera().SetViewUp(0,1,0)
        self.interactor.orientation = 2
        self.interactor.x = 0
        self.interactor.y = 1
        self.interactor.position = self.plan[self.interactor.orientation]
        self.interactor.refresh()

"""def voxelize(input_image, polydata):
  # input image : SpatialImage
  # polydata : type vtk.vtkPolyData
  bounds = polydata.GetBounds()
  spacing = input_image.voxelsize
 
  out_image = vtk.vtkImageData()
  out_image.SetSpacing(spacing[0], spacing[1], spacing[2])
  dims = np.zeros((3,), dtype = np.uint8)
  for i in range(0, 3):
    dims[i] = int(np.ceil((bounds[2*i +1] - bounds[2*i])/spacing[i]))
  out_image.SetDimensions(dims)
  out_image.SetExtent(0, dims[0] -1, 0, dims[1] -1, 0, dims[2] -1)
  origin = np.zeros((3,), dtype = np.float)
  origin[0] = bounds[0] + spacing[0]/2
  origin[1] = bounds[2] + spacing[1]/2
  origin[2] = bounds[4] + spacing[2]/2
  out_image.SetOrigin(origin)
  out_image.SetScalarTypeToUnsignedChar()
  out_image.AllocateScalars()
  foreground = 255
  background = 0
  counts = out_image.GetNumberOfPoints()
  for i in range(0,counts):
    out_image.GetPointData().GetScalars().SetTuple1(i, foreground)

  pol2stenc = vtk.vtkPolyDataToImageStencil()
  pol2stenc.SetInput(polydata)
  pol2stenc.SetOutputOrigin(origin)
  pol2stenc.SetOutputSpacing(spacing)
  pol2stenc.SetOutputWholeExtent(out_image.GetExtent())
  pol2stenc.Update()

  imgstenc = vtk.vtkImageStencil()
  imgstenc.SetInput(out_image)
  imgstenc.SetStencil(pol2stenc.GetOutput())
  imgstenc.ReverseStencilOff()
  imgstenc.SetBackgroundValue(background)
  imgstenc.Update()
 
  writer = vtk.vtkMetaImageWriter()
  writer.SetInput(imgstenc.GetOutput())
  writer.SetFileName("/home/sophie/Bureau/vtk_polydata_to_voxel/test.mha")
  writer.Write()
  return imgstenc     """   

def voisinage(matrix, contour, label):
    labels = list()
    for i in xrange(contour.GetNumberOfPoints()):
        coord = np.zeros(3)
        contour.GetPoint(i,coord)
        xmin = int(coord[0]-1)
        xmax = int(coord[0]+1)
        ymin = int(coord[1]-1)
        ymax = int(coord[1]+1)
        zmin = int(coord[2]-1)
        zmax = int(coord[2]+1)
        x = int(coord[0])
        y = int(coord[1])
        z = int(coord[2])
        voisins = [(xmin,y,z), (x,ymin,z), (x,y,zmin), (xmax,y,z), (x,ymax,z), (x,y,zmax)]
        for voisin in voisins:
            lab = matrix[voisin[0],voisin[1],voisin[2]]
            if lab != label and lab != 0 and lab != 0 and not lab in labels:
                labels.append(lab)
    return labels

def cutplane(poly,orientation,position):
    origine = np.zeros(3)
    origine[orientation] = position
    normal = np.zeros(3)
    normal[orientation] = 1
    
    plane = vtk.vtkPlane()
    plane.SetOrigin(origine)
    plane.SetNormal(normal)
    cutter = vtk.vtkCutter()
    cutter.SetInput(poly)
    cutter.SetCutFunction(plane)
    cutter.Update()
    return cutter.GetOutput()

def get_contours(matrix,label):
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)
    return compute_points(reader.GetOutput(),label)

def compute_points(matrix, label):   
    contour = vtk.vtkDiscreteMarchingCubes()
    contour.SetInput(matrix)
    contour.ComputeScalarsOn()
    contour.ComputeGradientsOn()
    contour.SetValue(0, label)
    contour.Update()
    return contour.GetOutput()
    
def get_contours2(matrix,label):
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)
    return compute_points2(reader.GetOutput(),label)
    
def compute_points2(matrix, label):    
    contour = vtk.vtkDiscreteMarchingCubes()
    contour.SetInput(matrix)
    contour.ComputeScalarsOff()
    contour.ComputeGradientsOff()
    for i,lab in enumerate(label):
        contour.SetValue(i, lab)
    contour.Update()
    return contour.GetOutput()
    
def compute_image(matrix):
    reader = matrix_to_image_reader('la', matrix, matrix.dtype)
    box = reader.GetDataExtent()
    lut = define_LUT(matrix)
    colors = vtk.vtkImageMapToColors()
    colors.SetInputConnection(reader.GetOutputPort())
    colors.SetLookupTable(lut)
    imgactor = vtk.vtkImageActor()
    imgactor.SetInput(colors.GetOutput())
    imgactor.SetOpacity(0.2)
    imgactor.SetDisplayExtent(box[0], box[1], box[2], box[3], (box[4] + box[5])/ 2, (box[4] + box[5])/ 2)
    return imgactor
    
def define_LUT(image):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(image.max()+1)
    lut.SetNumberOfColors(image.max()+1)
    lut.SetRange(image.min(), image.max())
    lut.Build()
    return lut
    
def isnotInList(p,l):
    for i in l:
        if (i == p):
            return False
    return True
    
def is_shared_point(p1, poly1, poly2):
    coord = np.zeros(3)    
    poly1.GetPoint(p1,coord)
    p2 = poly2.FindPoint(coord)
    coord2 = np.zeros(3)
    poly2.GetPoint(p2,coord2)
    if distance(coord,coord2) == 0:
        return p2
    else :
        return -1
        
def distance(p1,p2):
    dist = sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
    return dist

def intersection(box, boxx):
    x = box[0] < boxx[1] and boxx[0] < box[1]
    y = box[2] < boxx[3] and boxx[2] < box[3]
    z = box[4] < boxx[5] and boxx[4] < box[5]
    return x and y and z

def delete_shared_borders_mieux(poly1,poly2):
    for i in xrange(poly2.GetNumberOfCells()):
        idPoints = vtk.vtkIdList()
        poly2.GetCellPoints(i,idPoints)
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
        poly1.GetCellPoints(i,idPoints)
        frontiere = True
        for j in xrange(idPoints.GetNumberOfIds()):                
            if is_shared_point(idPoints.GetId(j), poly1, poly2) == -1:
                frontiere = False
                break
        if frontiere: 
            poly1.DeleteCell(i)
    poly1.RemoveDeletedCells()
    poly1.Modified()

def delete_shared_borders_pas_top(poly1, poly2):          
    frontFusion = [i for i in xrange(poly2.GetNumberOfPoints()) if is_shared_point(i, poly2, poly1) != -1]
    frontConsid = [is_shared_point(i, poly2, poly1) for i in frontFusion]
            
    for p in frontFusion :
        idCell = vtk.vtkIdList()
        poly2.GetPointCells(p,idCell)
        for j in xrange(idCell.GetNumberOfIds()):
            pointId = vtk.vtkIdList()
            poly2.GetCellPoints(idCell.GetId(j),pointId)
            frontiere = True
            for k in xrange(pointId.GetNumberOfIds()):
                if is_shared_point(pointId.GetId(k), poly2, poly1) == -1:
                    frontiere = False
                    break
            if frontiere: 
                poly2.DeleteCell(idCell.GetId(j))
                poly2.RemoveDeletedCells()
                poly2.Modified()
                        
    for p in frontConsid :
        idCell = vtk.vtkIdList()
        poly1.GetPointCells(p,idCell)
        for j in xrange(idCell.GetNumberOfIds()):
            pointId = vtk.vtkIdList()
            poly1.GetCellPoints(idCell.GetId(j),pointId)
            frontiere = True
            for k in xrange(pointId.GetNumberOfIds()):
                if is_shared_point(pointId.GetId(k), poly1, poly2) == -1:
                    frontiere = False
                    break
            if frontiere: 
                poly1.DeleteCell(idCell.GetId(j))
                poly1.RemoveDeletedCells()
                poly1.Modified()

def is_poly_in_plan(poly, orientation, position):
    box = np.zeros(6)
    poly.GetBounds(box)
    return box[orientation*2] < position and box[orientation*2+1] > position
    
class SelectCell (vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("MiddleButtonPressEvent", self.MiddleButtonPressEvent)
        self.selectedPoint1 = -1
        self.data = np.arange(1)
        self.pointsData = vtk.vtkPolyData()
        self.pointsMapper = vtk.vtkDataSetMapper()
        self.pointsMapper.SetInput(self.pointsData)
        self.pointsActor = vtk.vtkActor()
        self.pointsActor.SetMapper(self.pointsMapper)
        self.pointsActor.GetProperty().SetPointSize(1)
        self.pointsActor.GetProperty().SetOpacity(1)
        self.pointsActor.GetProperty().SetColor(0.8, 0, 0.4)

    def MiddleButtonPressEvent(self, obj, event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
        points = self.GetInteractor().GetPicker().GetPickedPositions()
        coord = np.zeros(3)
        points.GetPoint(0, coord)
        if (self.GetInteractor().GetPicker().GetPointId() != -1):
            self.selectedPoint1 = self.GetInteractor().GetPicker().GetPointId()
            label = self.data[int(coord[0])][int(coord[1])][int(coord[2])]
            print label
            if (label > 1):
                reader = matrix_to_image_reader('la', self.data, self.data.dtype)
                dat = reader.GetOutput()
                self.pointsData.ShallowCopy(compute_points(dat, label))
                self.GetCurrentRenderer().AddActor(self.pointsActor)
                self.GetCurrentRenderer().Render()
                self.GetCurrentRenderer().GetRenderWindow().Render()
        else:
            self.selectedPoint1 = -1            
            
class InteractorEditor2D (vtk.vtkInteractorStyle):

    def __init__(self,parent=None):
        self.AddObserver("LeftButtonPressEvent",self.LeftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent",self.LeftButtonReleaseEvent)
        #self.AddObserver("MiddleButtonPressEvent", self.MiddleButtonPressEvent)
        #self.AddObserver("KeyPressEvent",self.KeyPressEvent)
        
        self.consideredCell = vtk.vtkPolyData()
        self.polyList = dict()
        self.background = vtk.vtkImageActor()
        self.polyInPlan = list()       
        self.matrix = []
        
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
           
    def refresh(self):
        self.GetCurrentRenderer().RemoveAllViewProps()
        self.refresh_poly()
        self.refresh_background()
        self.GetCurrentRenderer().ResetCamera()
        self.GetCurrentRenderer().Render()
        self.GetCurrentRenderer().GetRenderWindow().Render()       
        
    
    def refresh_poly(self):
        self.polyInPlan = [lab for lab, poly in self.polyList.items() if is_poly_in_plan(poly, self.orientation, self.position) ]
        for lab in self.polyInPlan :
            cutter = cutplane(self.polyList[lab],self.orientation,self.position)
            newmap = vtk.vtkPolyDataMapper()
            newmap.SetInput(cutter)
            newmap.ScalarVisibilityOff()
            newact = vtk.vtkActor()
            newact.SetMapper(newmap)
            if lab == self.selectedLabel :
                newact.GetProperty().SetColor(0,1,0)     
            else :
                newact.GetProperty().SetColor(0,0,1)      
            self.GetCurrentRenderer().AddActor(newact)           
        considcutter = cutplane(self.consideredCell,self.orientation,self.position)
        considmap = vtk.vtkPolyDataMapper()
        considmap.SetInput(considcutter)
        considmap.ScalarVisibilityOff()
        considact = vtk.vtkActor()
        considact.SetMapper(considmap)
        considact.GetProperty().SetColor(1,0,0)
        self.GetCurrentRenderer().AddActor(considact)
        
    def refresh_background(self):
        bounds = np.zeros(6)
        self.GetCurrentRenderer().ComputeVisiblePropBounds(bounds)
        for lim in bounds :
            lim = int(lim)
        bounds[self.orientation*2] = self.position
        bounds[self.orientation*2+1] = self.position
        self.background.SetDisplayExtent(bounds)
        self.background.Modified()
        self.GetCurrentRenderer().AddActor(self.background)
        
    
    def LeftButtonPressEvent(self,obj,event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
        points = self.GetInteractor().GetPicker().GetPickedPositions()
        coord = np.zeros(3)
        points.GetPoint(0, coord)
        if self.mode == 0:             
            fp = self.consideredCell.FindPoint(coord)
            co = np.zeros(3)
            self.consideredCell.GetPoint(fp,co)
            if distance(co,coord) <= 1:
                self.selectedPoint = fp               
            else :
                self.selectedPoint = -1
        elif self.mode == 1:
            self.selectedLabel = self.matrix[int(coord[0])][int(coord[1])][int(coord[2])]
            if self.selectedLabel in self.deletedLabel or self.selectedLabel == self.label or self.selectedLabel not in self.polyList:
                self.selectedLabel = -1
            print self.selectedLabel
            self.refresh()
    
    # TODO : trouver une meilleure formule de deplacement que la proportionnalite
                        
    def LeftButtonReleaseEvent(self,obj,event):
        if self.mode == 0:
            if (self.selectedPoint != -1) :
                pos = self.GetInteractor().GetEventPosition()
                self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer())
                pw = self.GetInteractor().GetPicker().GetPickPosition()            
                oldcoord = np.zeros(3) 
                self.consideredCell.GetPoint(self.selectedPoint,oldcoord)
                
                newcoord = np.zeros(3)
                newcoord[self.x] = pw[self.x]
                newcoord[self.y] = pw[self.y]
                newcoord[self.orientation] = self.position           
                transx = (oldcoord[self.x] - newcoord[self.x]) 
                transy = (oldcoord[self.y] - newcoord[self.y])
                
                sphere = vtk.vtkSphereSource()
                sphere.SetRadius(self.propagation)
                sphere.SetCenter(oldcoord)
                
                selectEnclosed = vtk.vtkSelectEnclosedPoints()
                selectEnclosed.SetInput(self.consideredCell)
                selectEnclosed.SetSurface(sphere.GetOutput())
                selectEnclosed.Update()
                                
                for i in xrange(self.consideredCell.GetNumberOfPoints()):
                    if selectEnclosed.IsInside(i):
                        coord = np.zeros(3)
                        self.consideredCell.GetPoint(i,coord)
                        dist = distance(oldcoord,coord)
                        coord[self.x] = coord[self.x] - (transx - transx*dist/self.propagation)
                        coord[self.y] = coord[self.y] - (transy - transy*dist/self.propagation)
                        self.consideredCell.GetPoints().SetPoint(i,coord)
                        self.consideredCell.Modified()
                
                for poly in self.polyList.values():       
                    box = np.zeros(6)
                    poly.GetBounds(box)                    
                    boxx = np.zeros(6)
                    sphere.GetOutput().GetBounds(boxx)                                        
                    if intersection(box,boxx):
                        selectEnclosed = vtk.vtkSelectEnclosedPoints()
                        selectEnclosed.SetInput(poly)
                        selectEnclosed.SetSurface(sphere.GetOutput())
                        selectEnclosed.Update()
                        for i in xrange(poly.GetNumberOfPoints()):
                            if selectEnclosed.IsInside(i):
                                coord = np.zeros(3)
                                poly.GetPoint(i,coord)
                                dist = distance(oldcoord,coord)
                                coord[self.x] = coord[self.x] - (transx - transx*dist/self.propagation)
                                coord[self.y] = coord[self.y] - (transy - transy*dist/self.propagation)
                                poly.GetPoints().SetPoint(i,coord)
                                poly.Modified()
                self.refresh()         
                self.GetCurrentRenderer().Render()
                self.GetCurrentRenderer().GetRenderWindow().Render()       
    
    def fusion_consid_select_cells(self):
        if self.mode == 1 and self.selectedLabel != -1 and self.selectedLabel not in self.deletedLabel:
            fusionPoly = self.polyList[self.selectedLabel]
            delete_shared_borders_mieux(self.consideredCell,fusionPoly)
            labels = voisinage(self.matrix, fusionPoly, self.selectedLabel)            
            if self.label in labels:
                labels.remove(self.label)
            for delLab in self.deletedLabel:
                if delLab in labels:
                    labels.remove(delLab)
            reader = matrix_to_image_reader('la', self.matrix, self.matrix.dtype)
            mat = reader.GetOutput()
            for labs in labels :
                if not self.polyList.has_key(labs):
                    self.polyList[labs] = compute_points(mat,labs)                   
            append = vtk.vtkAppendPolyData()
            append.AddInput(self.consideredCell)
            append.AddInput(fusionPoly)
            append.Update()
            
            cleaning = vtk.vtkCleanPolyData()
            cleaning.SetInput(append.GetOutput())
            cleaning.PointMergingOn()
            cleaning.SetTolerance(0.0)
            cleaning.Update()
            
            self.consideredCell = cleaning.GetOutput()
            del self.polyList[self.selectedLabel]
            self.deletedLabel.append(self.selectedLabel)
            self.selectedLabel = -1
            self.refresh()
                
                
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ew = EditorWindow()
    ew.show()
    sys.exit(app.exec_())
