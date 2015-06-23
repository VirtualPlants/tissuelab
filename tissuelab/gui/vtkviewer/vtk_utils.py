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
import numpy as np


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
    TODO: use a dict to match vtk array types to np types 
    (or existing vtk/np function?)
    """

    if polydata.GetCellData().GetNumberOfComponents() > 0:
        if isinstance(polydata.GetCellData().GetArray(0), vtk.vtkIntArray):
            cell_data = np.frombuffer(polydata.GetCellData().GetArray(0), np.uint16)
        if isinstance(polydata.GetCellData().GetArray(0), vtk.vtkLongArray):
            cell_data = np.frombuffer(polydata.GetCellData().GetArray(0), np.uint32)
        elif isinstance(polydata.GetCellData().GetArray(0), vtk.vtkFloatArray):
            cell_data = np.frombuffer(polydata.GetCellData().GetArray(0), np.float32)
        elif isinstance(polydata.GetCellData().GetArray(0), vtk.vtkDoubleArray):
            cell_data = np.frombuffer(polydata.GetCellData().GetArray(0), np.float64)
        else:
            cell_data = np.arange(1)
    elif polydata.GetPointData().GetNumberOfComponents() > 0:
        if isinstance(polydata.GetPointData().GetArray(0), vtk.vtkIntArray):
            cell_data = np.frombuffer(polydata.GetPointData().GetArray(0), np.uint16)
        elif isinstance(polydata.GetPointData().GetArray(0), vtk.vtkLongArray):
            cell_data = np.frombuffer(polydata.GetPointData().GetArray(0), np.uint32)
        elif isinstance(polydata.GetPointData().GetArray(0), vtk.vtkFloatArray):
            cell_data = np.frombuffer(polydata.GetPointData().GetArray(0), np.float32)
        elif isinstance(polydata.GetPointData().GetArray(0), vtk.vtkDoubleArray):
            cell_data = np.frombuffer(polydata.GetPointData().GetArray(0), np.float64)
        else:
            cell_data = np.arange(1)
    else:
        cell_data = np.arange(1)
    return cell_data


def matrix_to_image_reader(name, data_matrix, datatype=np.uint16, decimate=1):
    nx, ny, nz = data_matrix.shape
    data_string = data_matrix.tostring('F')

    reader = vtk.vtkImageImport()
    reader.CopyImportVoidPointer(data_string, len(data_string))
    if datatype == np.uint8:
        reader.SetDataScalarTypeToUnsignedChar()
    else:
        reader.SetDataScalarTypeToUnsignedShort()
    reader.SetNumberOfScalarComponents(1)
    reader.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
    reader.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)

    return reader


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
    import vtk
    import numpy as np

    # sub_polydata = vtk.vtkPolyData()
    # sub_polydata.DeepCopy(vtk_polydata)

    # if sub_polydata.GetNumberOfCells() > 0:
    #     sub_polydata.GetPolys().InitTraversal()
    #     idList = vtk.vtkIdList();
    #     for i in xrange(sub_polydata.GetNumberOfPolys()):
    #         sub_polydata.GetPolys().GetNextCell(idList)
    #         triangle_points = np.array([sub_polydata.GetPoints().GetPoint(idList.GetId(k)) for k in xrange(3)])
    #         print triangle_points," : ",(1-2*inside_out)*clipping_function.EvaluateFunction(triangle_points.mean(axis=0))
    #         if (1-2*inside_out)*clipping_function.EvaluateFunction(triangle_points.mean(axis=0)) <= value:
    #             sub_polydata.DeleteCell(i)
    #     sub_polydata.RemoveDeletedCells()

    # elif sub_polydata.GetNumberOfPoints() > 0:
    #     new_points = vtk.vtkPoints()
    #     for i in xrange(sub_polydata.GetNumberOfPoints()):
    #         point = np.array(sub_polydata.GetPoints().GetPoint(i))
    #         if (1-2*inside_out)*clipping_function.EvaluateFunction(point) > value:
    #             new_points.InsertPoint(i,point)
    #     sub_polydata.SetPoints(new_points)

    if point_polydata:
        polydata_extractor = vtk.vtkExtractGeometry()
    else:
        polydata_extractor = vtk.vtkExtractPolyDataGeometry()
    polydata_extractor.SetInput(vtk_polydata)
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
    polydata_clipper.SetInput(vtk_polydata)
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
    import vtk
    import numpy as np

    if vtk_polydata.GetNumberOfPoints() > 0:
        polydata_points = np.array([vtk_polydata.GetPoints().GetPoint(p) for p in xrange(vtk_polydata.GetNumberOfPoints())])
        polydata_extent = np.transpose([polydata_points.min(axis=0), polydata_points.max(axis=0)])
    else:
        polydata_extent = np.zeros((3, 2), int)
    return polydata_extent
