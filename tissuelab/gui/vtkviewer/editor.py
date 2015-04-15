# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

import numpy as np
import vtk

from vtkviewer import matrix_to_image_reader


def compute_points(name, matrix, label):
    reader = matrix_to_image_reader(name, matrix, matrix.dtype)
    nx, ny, nz = matrix.shape
    considered_cells = [label]

    contour = vtk.vtkDiscreteMarchingCubes()
    contour.SetInput(reader.GetOutput())
    contour.ComputeScalarsOn()
    contour.ComputeGradientsOn()
    for i,lab in enumerate(considered_cells):
        contour.SetValue(i,lab)
    contour.Update()  
    
    #decimate   
    decimate = vtk.vtkDecimatePro()
    decimate.SetInputConnection(contour.GetOutputPort())
    decimate.SetTargetReduction(0.5)
    decimate.Update()
    
    #smoother    
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(decimate.GetOutputPort())
    smoother.BoundarySmoothingOff()
    smoother.FeatureEdgeSmoothingOff()
    smoother.SetFeatureAngle(120.0)
    smoother.SetPassBand(0.001)
    smoother.SetNumberOfIterations(15)
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn()
    smoother.Update()

    """marching_cubes = smoother.GetOutput()
    points=vtk.vtkPoints()
    vertices=vtk.vtkCellArray()

    for p in xrange(marching_cubes.GetPoints().GetNumberOfPoints()):
        u=points.InsertNextPoint(marching_cubes.GetPoints().GetPoint(p))
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(u)
  
    polyPoints=vtk.vtkPolyData()
    polyPoints.SetPoints(points)
    polyPoints.SetVerts(vertices) 
    return polyPoints"""
    
    dec = smoother.GetOutput()
    mat = np.zeros((nx,ny,nz),dtype=np.int)
    coord = np.zeros(3)
    for p in xrange(dec.GetPoints().GetNumberOfPoints()):
        dec.GetPoints().GetPoint(p,coord)
        mat[int(coord[0])][int(coord[1])][int(coord[2])] = 255
        
    pts = np.transpose(np.where(mat>1))
    
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    lines = vtk.vtkCellArray()
    lines.Allocate(100)
    
    for p in range(pts.shape[0]):
        u = points.InsertNextPoint(pts[p])
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(u)
        
    polyPoints=vtk.vtkPolyData()
    polyPoints.SetPoints(points)
    polyPoints.SetVerts(vertices)
    polyPoints.SetLines(lines)
    
    return polyPoints
    
class SelectCell (vtk.vtkInteractorStyleTrackballCamera):
        
    def __init__(self,parent=None):
        self.AddObserver("MiddleButtonPressEvent",self.MiddleButtonPressEvent)
        self.selectedPoint1 = -1
        self.data = np.arange(1)
        self.pointsData = vtk.vtkPolyData()
        self.pointsMapper = vtk.vtkDataSetMapper()
        self.pointsMapper.SetInput(self.pointsData)
        self.pointsActor = vtk.vtkActor()
        self.pointsActor.SetMapper(self.pointsMapper)
        self.pointsActor.GetProperty().SetPointSize(1)
        self.pointsActor.GetProperty().SetOpacity(1)
        self.pointsActor.GetProperty().SetColor(0.8,0,0.4)
    
    def MiddleButtonPressEvent(self,obj,event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer())
        points = self.GetInteractor().GetPicker().GetPickedPositions()
        coord = np.zeros(3)
        points.GetPoint(0,coord)
        if (self.GetInteractor().GetPicker().GetPointId()!=-1):
            self.selectedPoint1 = self.GetInteractor().GetPicker().GetPointId()
            label = self.data[int(coord[0])][int(coord[1])][int(coord[2])]
            print label    
            if (label>1):
                self.pointsData.ShallowCopy(compute_points('label', self.data, label))
                self.GetCurrentRenderer().AddActor(self.pointsActor)
                self.GetCurrentRenderer().Render()
                self.GetCurrentRenderer().GetRenderWindow().Render()
        else : 
            self.selectedPoint1 = -1
            
            
class MovePoint (vtk.vtkInteractorStyle):

    data = vtk.vtkPolyData()

    def __init__(self,parent=None):
        self.AddObserver("MiddleButtonPressEvent",self.MiddleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent",self.MiddleButtonReleaseEvent)
        self.AddObserver("LeftButtonPressEvent",self.LeftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent",self.LeftButtonReleaseEvent)
        self.AddObserver("RightButtonPressEvent",self.RightButtonPressEvent)
        self.AddObserver("KeyPressEvent",self.KeyPressEvent)
        self.selectedPoint1 = -1
        self.selectedPoint2 = -1
        self.deletePoint = -1
        self.movePoint = vtk.vtkPoints()
        self.movePoint.InsertNextPoint(0,0,0)
        
        self.movePolyData = vtk.vtkPolyData()
        self.movePolyData.SetPoints(self.movePoint)
        
        self.moveVertexFilter = vtk.vtkVertexGlyphFilter()
        self.moveVertexFilter.SetInput(self.movePolyData)
        self.moveVertexFilter.Update()
        
        self.moveMapper = vtk.vtkPolyDataMapper()
        self.moveMapper.SetInput(self.moveVertexFilter.GetOutput())
        
        self.moveActor = vtk.vtkActor()
        self.moveActor.SetMapper(self.moveMapper)
        self.moveActor.GetProperty().SetPointSize(5)
        self.moveActor.GetProperty().SetColor(0,1,0)
        
        
    
    def LeftButtonPressEvent(self,obj,event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer())       
        self.selectedPoint1 = self.GetInteractor().GetPicker().GetPointId()
        print self.selectedPoint1
        if (self.selectedPoint1!=-1):
            p = np.zeros(3)
            self.data.GetPoint(self.selectedPoint1,p)
            self.moveActor.SetPosition(p)
            self.moveActor.VisibilityOn()
            self.GetCurrentRenderer().AddActor(self.moveActor)
            self.GetCurrentRenderer().Render()
            self.GetCurrentRenderer().GetRenderWindow().Render()
 
    def LeftButtonReleaseEvent(self,obj,event):
        if (self.selectedPoint1 != -1) :
            pos = self.GetInteractor().GetEventPosition()
            pw = np.arange(4)
            self.ComputeDisplayToWorld(self.GetCurrentRenderer(),pos[0],pos[1],0,pw)
            self.moveActor.SetPosition(pw[0],pw[1],pw[2])
            """pos = self.GetInteractor().GetEventPosition()
            self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer()) 
            points = self.GetInteractor().GetPicker().GetPickedPositions()
            coord = np.zeros(3)
            points.GetPoint(0,coord)   
            self.moveActor.SetPosition(coord)"""                
            self.data.GetPoints().SetPoint(self.selectedPoint1,self.moveActor.GetPosition())
            self.data.Modified()
            self.moveActor.VisibilityOff()
            self.GetCurrentRenderer().Render()
            self.GetCurrentRenderer().GetRenderWindow().Render()
        
    def RightButtonPressEvent(self,obj,event):
        pos = self.GetInteractor().GetEventPosition()
        pw = np.arange(4)
        self.ComputeDisplayToWorld(self.GetCurrentRenderer(),pos[0],pos[1],0,pw)
        u = self.data.GetPoints().InsertNextPoint(pw[0],pw[1],pw[2])
        self.data.GetVerts().InsertNextCell(1)
        self.data.GetVerts().InsertCellPoint(u)
        self.data.Modified()
        self.GetCurrentRenderer().Render()
        self.GetCurrentRenderer().GetRenderWindow().Render()
        
    def MiddleButtonPressEvent(self,obj,event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer())
        self.selectedPoint1 = self.GetInteractor().GetPicker().GetPointId()
        if (self.selectedPoint1 != -1):
            p = np.zeros(3)
            self.data.GetPoint(self.selectedPoint1,p)
            self.moveActor.SetPosition(p)
            self.moveActor.VisibilityOn()
            pw = np.arange(4)
            self.ComputeDisplayToWorld(self.GetCurrentRenderer(),pos[0],pos[1],0,pw)
            self.GetCurrentRenderer().AddActor(self.moveActor)
            self.GetCurrentRenderer().Render()
            self.GetCurrentRenderer().GetRenderWindow().Render()
             
    def MiddleButtonReleaseEvent(self,obj,event):
        pos = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer())
        self.selectedPoint2 = self.GetInteractor().GetPicker().GetPointId()
        if ((self.selectedPoint1 != -1 )&(self.selectedPoint2 != -1)):
            self.data.GetLines().InsertNextCell(2)
            self.data.GetLines().InsertCellPoint(self.selectedPoint1)
            self.data.GetLines().InsertCellPoint(self.selectedPoint2)
            self.data.Modified()
            self.GetCurrentRenderer().Render()
            self.GetCurrentRenderer().GetRenderWindow().Render()
            
    def KeyPressEvent(self,obj,event):  
        key=self.GetInteractor().GetKeyCode()
        print key      
        if (key == 's'):
            pos = self.GetInteractor().GetEventPosition()
            self.GetInteractor().GetPicker().Pick( pos[0], pos[1], 0, self.GetCurrentRenderer())
            self.deletePoint = self.GetInteractor().GetPicker().GetPointId()
            if (self.deletePoint != -1):
                cell = vtk.vtkIdList()
                self.data.GetPointCells(self.deletePoint,cell)
                for i in xrange(cell.GetNumberOfIds()) : 
                    self.data.DeleteCell(cell.GetId(i))
                self.data.RemoveDeletedCells()
                self.data.Modified()                    
                self.GetCurrentRenderer().Render()
                self.GetCurrentRenderer().GetRenderWindow().Render()
