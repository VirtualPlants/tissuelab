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


def define_lookuptable(image, colormap_points, colormap_name, i_min=None, i_max=None):
    if i_min is None:
        # i_min = image.min()
        i_min = np.percentile(image, 5)
    if i_max is None:
        # i_max = image.max()
        i_max = np.percentile(image, 95)
    # lut = vtk.vtkLookupTable()
    lut = vtk.vtkColorTransferFunction()
    # lut.DiscretizeOn()

    if colormap_name == 'glasbey':
        if i_max < 255:
            for i in xrange(256):
                lut.AddRGBPoint(i, * colormap_points.values()[int(i)])
        else:
            for i in np.unique(image):
                lut.AddRGBPoint(i, *colormap_points.values()[int(i) % 256])
    else:
        for value in colormap_points.keys():
            lut.AddRGBPoint(
                (1.0 - value) * i_min + value * i_max, *colormap_points[value])

    # lut.Build()
    return lut


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
