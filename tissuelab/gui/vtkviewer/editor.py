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
from openalea.image.spatial_image import SpatialImage



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

    marching_cubes = smoother.GetOutput()
    points=vtk.vtkPoints()
    vertices=vtk.vtkCellArray()

    for p in xrange(marching_cubes.GetPoints().GetNumberOfPoints()):
        u=points.InsertNextPoint(marching_cubes.GetPoints().GetPoint(p))
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(u)
  
    polyPoints=vtk.vtkPolyData()
    polyPoints.SetPoints(points)
    polyPoints.SetVerts(vertices) 
    return polyPoints
