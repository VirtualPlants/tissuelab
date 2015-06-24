# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Bâty <guillaume.baty@inria.fr>
#       File contributor(s): Guillaume Bâty <guillaume.baty@inria.fr>
#                            Alizon König <alizon.konig@inria.fr>
#                            Guillaume Cerutti <guillaume.cerutti@inria.fr>
#                            Pierre Fernique <pierre.fernique@inria.fr>
#                            Sophie Ribes <sophie.ribes@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

__all__ = [
    'blend_funct',
    'define_lookuptable',
    'matrix_to_image_reader',
]

import vtk
from vtk.util import numpy_support
import numpy as np
from vtk.util.numpy_support import get_numpy_array_type


"""
========
VTK TIPS
========

VTK 5->6
========

if vtk.VTK_MAJOR_VERSION <= 5:
    image.SetNumberOfScalarComponents(1)
    image.SetScalarTypeToDouble()
else:
    image.AllocateScalars(VTK_DOUBLE, 1)

vtkImageImport to vtkActor
==========================

imageImport.Update()
if vtk.VTK_MAJOR_VERSION <= 5:
    actor.SetInput(imageImport.GetOutput())
else:
    actor.SetInputData(imageImport.GetOutput())
"""


def define_lookuptable(data, colormap_points, colormap_name, intensity_range=None):
    if intensity_range is None:
        i_min = i_max = None
    else:
        i_min, i_max = intensity_range

    if i_min is None:
        i_min = np.percentile(data, 5)
    if i_max is None:
        i_max = np.percentile(data, 95)
    lut = vtk.vtkColorTransferFunction()

    if colormap_name == 'glasbey':
        if i_max < 255:
            for i in xrange(256):
                lut.AddRGBPoint(i, * colormap_points.values()[i])
        else:

            from time import time
            start_time = time()
            points = np.unique(data)
            end_time = time()
            print "Unique time : ", end_time - start_time, " s"

            start_time = time()
            for i in points:
                lut.AddRGBPoint(i, *colormap_points.values()[int(i) % 256])
            end_time = time()
            print "RGBPoint time : ", end_time - start_time, " s"
    else:
        for value in colormap_points.keys():
            lut.AddRGBPoint(
                (1.0 - value) * i_min + value * i_max, *colormap_points[value])
    return lut


def get_polydata_cell_data(polydata):
    """
    """
    if polydata.GetCellData().GetNumberOfComponents() > 0:
        array = polydata.GetCellData().GetArray(0)
    elif polydata.GetPointData().GetNumberOfComponents() > 0:
        array = polydata.GetPointData().GetArray(0)
    else:
        return np.arange(1)

    try:
        cell_data = np.frombuffer(array, get_numpy_array_type(array.GetDataType()))
    except KeyError:
        cell_data = np.arange(1)

    return cell_data


def matrix_to_image_reader(name, data_matrix, datatype=np.uint16, decimate=1):
    nx, ny, nz = data_matrix.shape
    datatype = data_matrix.dtype

    reader = vtk.vtkImageImport()
    #reader.SetImportVoidPointer(data_matrix) # No copy but index order changed
    data_string = data_matrix.tostring('F')
    reader.CopyImportVoidPointer(data_string, len(data_string))

    reader.SetNumberOfScalarComponents(1)

    if datatype == np.uint8:
        reader.SetDataScalarTypeToUnsignedChar()
    else:
        reader.SetDataScalarTypeToUnsignedShort()
    if vtk.VTK_MAJOR_VERSION <= 5:
        pass
    else:
        reader.GetOutput().AllocateScalars(numpy_support.get_vtk_array_type(datatype), 1)

    box = np.zeros(6)
    reader.GetOutput().GetBounds(box)

    x_min = 0
    x_max = nx - 1

    y_min = 0
    y_max = ny - 1

    z_min = 0
    z_max = nz - 1

    #reader.SetDataOrigin(0, 0, 0)
    reader.SetWholeExtent(x_min, x_max, y_min, y_max, z_min, z_max)
    reader.SetDataExtentToWholeExtent()
    reader.Modified()
    reader.UpdateInformation()
    reader.Update()

    return reader

def obj_extent(obj):
    if vtk.VTK_MAJOR_VERSION <= 5:
        box = obj.GetOutput().GetWholeExtent()
    else:
        box = obj.GetOutputInformation(0).Get(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT())
    return box

def blend_funct(data_matrix, data1, lookuptable1, data2, lookuptable2, orientation):
    nx, ny, nz = data_matrix.shape
    xMax = nx - 1
    yMax = ny - 1
    zMax = nz - 1

    p1Colors = vtk.vtkImageMapToColors()
    p1Colors.SetInputConnection(data1.GetOutputPort())
    p1Colors.SetLookupTable(lookuptable1)
    p2Colors = vtk.vtkImageMapToColors()
    p2Colors.SetInputConnection(data2.GetOutputPort())
    p2Colors.SetLookupTable(lookuptable2)
    blend = vtk.vtkImageBlend()
    blend.AddInput(p1Colors.GetOutput())
    blend.AddInput(p2Colors.GetOutput())
    blend.SetOpacity(0, 0.5)
    blend.SetOpacity(1, 0.5)
    imgactor = vtk.vtkImageActor()
    imgactor.SetInput(blend.GetOutput())
    if orientation == 1:
        imgactor.SetDisplayExtent(
            np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
    elif orientation == 2:
        imgactor.SetDisplayExtent(
            0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
    elif orientation == 3:
        imgactor.SetDisplayExtent(
            0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

    imgactor.SetOrigin(nx / 2., ny / 2., nz / 2.)
    imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)

    return imgactor, blend


def vtk_sub_polydata(vtk_polydata, clipping_function, value=0, point_polydata=False, inside_out=False):

    if point_polydata:
        polydata_extractor = vtk.vtkExtractGeometry()
    else:
        polydata_extractor = vtk.vtkExtractPolyDataGeometry()
    if vtk.VTK_MAJOR_VERSION <= 5:
        polydata_extractor.SetInput(vtk_polydata)
    else:
        polydata_extractor.SetInputData(vtk_polydata)
    polydata_extractor.SetImplicitFunction(clipping_function)
    if inside_out:
        polydata_extractor.ExtractInsideOn()
    else:
        polydata_extractor.ExtractInsideOff()
    polydata_extractor.Update()

    sub_polydata = vtk.vtkPolyData()
    sub_polydata.DeepCopy(polydata_extractor.GetOutput())

    return sub_polydata


def vtk_clipped_polydata(vtk_polydata, clipping_function, value=0, point_polydata=False, inside_out=False):

    if point_polydata:
        polydata_clipper = vtk.vtkClipDataSet()
    else:
        polydata_clipper = vtk.vtkClipPolyData()

    if vtk.VTK_MAJOR_VERSION <= 5:
        polydata_clipper.SetInput(vtk_polydata)
    else:
        polydata_clipper.SetInputData(vtk_polydata)

    polydata_clipper.SetClipFunction(clipping_function)
    polydata_clipper.SetValue(value)
    if inside_out:
        polydata_clipper.InsideOutOn()
    polydata_clipper.GenerateClippedOutputOn()
    polydata_clipper.Update()

    cut_polydata = vtk.vtkPolyData()
    cut_polydata.DeepCopy(polydata_clipper.GetOutput())

    return cut_polydata


def get_polydata_extent(vtk_polydata):

    if vtk_polydata.GetNumberOfPoints() > 0:
        polydata_points = np.array([vtk_polydata.GetPoints().GetPoint(p) for p in xrange(vtk_polydata.GetNumberOfPoints())])
        polydata_extent = np.transpose([polydata_points.min(axis=0), polydata_points.max(axis=0)])
    else:
        polydata_extent = np.zeros((3, 2), int)
    return polydata_extent
