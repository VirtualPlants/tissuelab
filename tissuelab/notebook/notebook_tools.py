# -*- coding: utf-8 -*-
# -*- python -*-
#
#       Meshing
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       File contributor(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenaleaLab Website : http://virtualplants.github.io/
#
###############################################################################

import vtk
from IPython.display import Image
import numpy as np

from openalea.oalab.colormap.colormap_def import load_colormaps

def vtk_show(renderer, width=400, height=300):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
    renderWindow.Render()
     
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()
     
    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = str(buffer(writer.GetResult()))
    
    return Image(data)

def vtk_show_polydata(polydata, width=400, height=300, position=(0,0,-160), colormap_name='glasbey', **kwargs):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    from tissuelab.gui.vtkviewer.colormap_utils import colormap_from_file
    from tissuelab.gui.vtkviewer.vtk_utils import define_lookuptable, get_polydata_cell_data
    
    point_radius = kwargs.get('point_radius',1.0)

    if (polydata.GetNumberOfCells() == 0) and (polydata.GetNumberOfPoints() > 0):
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(point_radius)
        sphere.SetThetaResolution(12)
        sphere.SetPhiResolution(12)
        glyph = vtk.vtkGlyph3D()
        glyph.SetScaleModeToDataScalingOff()
        glyph.SetColorModeToColorByScalar()
        glyph.SetSource(sphere.GetOutput())
        glyph.SetInput(polydata)
        glyph.Update()
        polydata = glyph.GetOutput()

    # colormap = colormap_from_file("/Users/gcerutti/Developpement/openalea/oalab-tissue/tissuelab/share/data/colormaps/glasbey.lut",name="glasbey")
    colormap = load_colormaps()[colormap_name]
    
    irange = kwargs.get('intensity_range', None)

    cell_data = get_polydata_cell_data(polydata)
    lut = define_lookuptable(cell_data,colormap_points=colormap._color_points,colormap_name=colormap.name,intensity_range=irange)

    VtkMapper = vtk.vtkPolyDataMapper()
    VtkMapper.SetInputConnection(polydata.GetProducerPort())
    VtkMapper.SetLookupTable(lut)
    
    VtkActor = vtk.vtkActor()
    VtkActor.SetMapper(VtkMapper)

    VtkRenderer = vtk.vtkRenderer()
    VtkRenderer.SetBackground(1.0, 1.0, 1.0)
    VtkRenderer.AddActor(VtkActor)

    VtkRenderer.GetActiveCamera().SetPosition(*position)

    return vtk_show(VtkRenderer, width=width, height=height)


def vtk_show_image(image, width=400, height=300, position=(0,0,-160),resolution=(1.0,1.0,1.0),colormap_name='glasbey',**kwargs):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    from tissuelab.gui.vtkviewer.colormap_utils import colormap_from_file
    from tissuelab.gui.vtkviewer.vtk_utils import define_lookuptable, matrix_to_image_reader
    
    reader = matrix_to_image_reader("", image, image.dtype, decimate=1)
    
    compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(compositeFunction)
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    
    alpha = kwargs.get('alpha',1.0)
    bg_id = kwargs.get('bg_id', None)
    alphamap = kwargs.get('alphamap', 'constant')
    irange = kwargs.get('intensity_range', (image.min(), image.max()))
    
    colormap = load_colormaps()[colormap_name]
    # colormap = colormap_from_file("/Users/gcerutti/Developpement/openalea/oalab-tissue/tissuelab/share/data/colormaps/glasbey.lut",name="glasbey")
    lut = define_lookuptable(image,colormap_points=colormap._color_points,colormap_name=colormap.name,intensity_range=irange)
    
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(lut)
    
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    volume_property.SetScalarOpacity(alphaChannelFunc)
    
    alphaChannelFunc.RemoveAllPoints()
    
    if alphamap == "constant":
        alphaChannelFunc.ClampingOn()
        alphaChannelFunc.AddPoint(irange[0], alpha)
        alphaChannelFunc.AddPoint(irange[1], alpha)
        if bg_id is not None:
             alphaChannelFunc.AddPoint(bg_id - 1, alpha)
             alphaChannelFunc.AddPoint(bg_id, 0.0)
             alphaChannelFunc.AddPoint(bg_id + 1, alpha)
    elif alphamap == "linear":
        alphaChannelFunc.ClampingOn()
        alphaChannelFunc.AddPoint(irange[0], 0.0)
        alphaChannelFunc.AddPoint(irange[1], alpha)
            
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volume_property)
    
    image_center = np.array(image.shape)/2
    volume.SetOrigin(image_center[0], image_center[1], image_center[2])
    volume.SetPosition(-image_center[0], -image_center[1], -image_center[2])

    if hasattr(image,'resolution'):
        resolution = image.resolution
    volume.SetScale(resolution[0], resolution[1], resolution[2])

    VtkRenderer = vtk.vtkRenderer()
    VtkRenderer.SetBackground(1.0, 1.0, 1.0)
    VtkRenderer.AddViewProp(volume)

    VtkRenderer.GetActiveCamera().SetPosition(*position)

    return vtk_show(VtkRenderer, width=width, height=height)