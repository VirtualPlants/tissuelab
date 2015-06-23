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

import copy
import numpy as np
import vtk

import mimetypes

from openalea.vpltk.qt import QtGui
from openalea.core.interface import IBool, IInt, IFloat, ITuple, IEnumStr
from openalea.oalab.plugins.interface import IIntRange, IColormap
# Do not import world related module in this module, see vtkworldviewer instead!

from tissuelab.gui.vtkviewer.qvtkrenderwindowinteractor import QVTKRenderWindowInteractor
from tissuelab.gui.vtkviewer.colormap_def import load_colormaps
from tissuelab.gui.vtkviewer.vtk_utils import matrix_to_image_reader, define_lookuptable, get_polydata_cell_data, get_polydata_extent
from tissuelab.gui.vtkviewer.vtk_utils import vtk_clipped_polydata, vtk_sub_polydata


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

# Define constraints
cst_proba = dict(step=0.1, min=0, max=1)
cst_alphamap = dict(enum=['constant', 'linear'])
cst_width = dict(min=0, max=10)
cst_percent_range = dict(step=1, min=0, max=100)

attribute_definition = {}
attribute_definition['matrix'] = {}
attribute_definition['matrix']['matrix_colormap'] = dict(
    value=dict(name='grey', color_points=dict([(0, (0, 0, 0)), (1, (1, 1, 1))])), interface=IColormap, alias="Colormap")
attribute_definition['matrix']['volume_alpha'] = dict(value=1.0, interface=IFloat, constraints=cst_proba,
                                                      alias=u"Alpha (Volume)")
attribute_definition['matrix']['alphamap'] = dict(value='linear', interface=IEnumStr, constraints=cst_alphamap,
                                                  alias="Alpha Map")
attribute_definition['matrix']['bg_id'] = dict(value=1, interface=IInt, alias="Background Id")
attribute_definition['matrix']['intensity_range'] = dict(value=(0, 255), interface=IIntRange, alias="Intensity Range")
attribute_definition['matrix']['volume'] = dict(value=True, interface=IBool, alias="Display Volume")
attribute_definition['matrix']['cut_planes_alpha'] = dict(value=1.0, interface=IFloat, constraints=cst_proba,
                                                          alias=u"Alpha (Cut planes)")
attribute_definition['matrix']['blending_factor'] = dict(value=0.5, interface=IFloat, constraints=cst_proba,
                                                         alias=u"Blending factor")
attribute_definition['matrix']['resolution'] = dict(value=(1.0, 1.0, 1.0), interface=ITuple, alias=u"Resolution")
attribute_definition['matrix']['position'] = dict(value=(0.0, 0.0, 0.0), interface=ITuple, alias=u"Position")
for axis in ['x', 'y', 'z']:
    alias = u"Move " + axis + " plane"
    attribute_definition['matrix'][axis + "_plane_position"] = dict(value=0, interface=IInt, alias=alias)
attribute_definition['matrix']['cut_planes'] = dict(value=False, interface=IBool, alias=u"Display Cut planes")
attribute_definition['polydata'] = {}
attribute_definition['polydata']['polydata_colormap'] = dict(
    value=dict(name='grey', color_points=dict([(0, (0, 0, 0)), (1, (1, 1, 1))])), interface=IColormap, alias="Colormap")
attribute_definition['polydata']['polydata_alpha'] = dict(value=1.0, interface=IFloat, constraints=cst_proba,
                                                          alias=u"Alpha (Polydata)")
attribute_definition['polydata']['intensity_range'] = dict(
    value=(
        0,
        255),
    interface=IIntRange,
    alias="Intensity Range")
attribute_definition['polydata']['linewidth'] = dict(value=1, interface=IInt, alias="Linewidth", constraints=cst_width)
attribute_definition['polydata']['point_radius'] = dict(value=1.0, interface=IFloat, constraints=cst_width, alias=u"Point Size")
attribute_definition['polydata']['position'] = dict(value=(0.0, 0.0, 0.0), interface=ITuple, alias=u"Position")
attribute_definition['polydata']['display_polydata'] = dict(value=True, interface=IBool, alias=u"Display Polydata")
for axis in ['x', 'y', 'z']:
    alias = u"Move " + axis + " slice"
    attribute_definition['polydata'][axis + "_slice"] = dict(value=(0, 100), interface=IIntRange, constraints=cst_percent_range, alias=alias)
attribute_definition['polydata']['preserve_faces'] = dict(value=False, interface=IBool, alias=u"Preserve Faces")


colormaps = load_colormaps()


def attribute_meta(dtype, attr_name):
    return dict(interface=attribute_definition[dtype][attr_name]['interface'],
                alias=attribute_definition[dtype][attr_name]['alias'])


def attribute_args(dtype, attr_name, value=None, constraints=None):
    """
    Return an attribute {'value':..., 'name':...}
    """
    attribute = copy.deepcopy(attribute_definition[dtype][attr_name])
    attribute['name'] = attr_name
    if value is not None:
        attribute['value'] = value
    if constraints is not None:
        attribute['constraints'] = constraints
    return attribute


def default_value(dtype, attr_name, **kwargs):
    """
    Returns attribute in kwargs if defined else viewer's default
    """
    if isinstance(attr_name, basestring):
        attr_names = [attr_name]
    else:
        attr_names = attr_name

    for attr_name in attr_names:
        if attr_name in kwargs:
            return kwargs[attr_name]

    for attr_name in attr_names:
        if attr_name in attribute_definition[dtype]:
            return attribute_definition[dtype][attr_name]['value']

    raise NotImplementedError(attr_name)

image_writers = {
    'image/jpeg': vtk.vtkJPEGWriter,
    'image/png': vtk.vtkPNGWriter,
    'image/tiff': vtk.vtkTIFFWriter,
}


class VtkViewer(QtGui.QWidget):

    """
    Class providing a VtkViewer and convenience methods
      - to add actors, matrices (3d images), polydata,
      - to define and set colormaps
      - generate cut planes

    .. warning::

        Though this class can be embedded directly in a QWidget,
        it doesn't contain Qt features like buttons, toolbars or QAction.
        This class use only pure vtk features.

        For end-user features, please have a look to TissueViewer class.
    """

    DEFAULT_INTERACTOR_STYLE = vtk.vtkInteractorStyleTrackballCamera

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
        self.ren.SetBackground(1, 1, 1)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.default_interactor_style = self.DEFAULT_INTERACTOR_STYLE()
        self.set_interactor_style(self.default_interactor_style)

        #rajout picker
        self.picker = vtk.vtkPointPicker()
        self.picker.SetTolerance(0.005)
        self.iren.SetPicker(self.picker)
        #fin rajout

        layout.addWidget(self.frame)
        self.ren.ResetCamera()

        self.colormaps = colormaps

        # vtk objects (like vtk volumes, vtk actors...) sorted by name in a
        # dictionnary
        self.object_repr = {}
        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.polydata = {}
        self.property = {}
        self.vtkdata = {}
        self.blend = {}

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)

    ################################################
    # PURE VTK METHODS, NO MORE Qt AFTER THIS LINE #
    ################################################

    def display_volume(self, name=None, disp=True):
        self.clear_scene()
        self._display_volume(name, disp)
        self.compute()

    def display_cut_planes(self, name=None, disp=True):
        self.clear_scene()
        self._display_cut_planes(name, disp)
        self.compute()

    def display_polydata(self, name=None, disp=True):
        self.clear_scene()
        self._display_polydata(name, disp)
        self.compute()

    def _display_volume(self, name, disp=True):
        if name is None:
            for name in self.volume:
                self.volume_property[name]['disp'] = disp
        else:
            self.volume_property[name]['disp'] = disp

    def _display_cut_planes(self, name, disp=True):
        if name is None:
            for actor_name in self.actor:
                if '_cut_plane_' in actor_name:
                    self.property[actor_name]['disp'] = disp
        else:
            for actor_name in self.actor:
                if actor_name.startswith('%s_cut_plane_' % name):
                    self.property[actor_name]['disp'] = disp

    def _display_polydata(self, name, disp=True):
        if name is None:
            for actor_name in self.actor:
                if '_polydata' in actor_name:
                    self.property[actor_name]['disp'] = disp
        else:
            for actor_name in self.actor:
                if actor_name.startswith('%s_polydata' % name):
                    self.property[actor_name]['disp'] = disp

    def initialize(self):
        pass

    def clear_scene(self):
        for volume in self.volume.values():
            self.ren.RemoveVolume(volume)
        for actor in self.actor.values():
            self.ren.RemoveActor(actor)

    def clear(self):
        for name, volume in self.volume.items():
            self.ren.RemoveVolume(volume)
            del self.volume[name]
        for name, actor in self.actor.items():
            self.ren.RemoveActor(actor)
            del self.actor[name]

        self.object_repr = {}
        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.polydata = {}
        self.blend = {}
        self.vtkdata = {}

    def save_screenshot(self, filename):
        mimetype = mimetypes.guess_type(filename)[0]
        if mimetype not in image_writers:
            raise TypeError("No vtk writer found for type " + str(mimetype))
            return
        self.render()
        screenshooter = vtk.vtkWindowToImageFilter()
        screenshooter.SetInput(self.vtkWidget.GetRenderWindow())
        screenshooter.Update()
        writer = image_writers[mimetype]()
        writer.SetFileName(filename)
        writer.SetInput(screenshooter.GetOutput())
        writer.Write()

    def refresh(self):
        self.compute()

    def compute(self):
        for name, volume in self.volume.items():
            if self.volume_property[name]['disp']:
                self.ren.AddVolume(volume)
        for name, actor in self.actor.items():
            if self.property[name]['disp']:
                self.ren.AddActor(actor)

        self.iren.Initialize()
        self.iren.Start()
        self.render()

    def remove_matrix(self, name):
        for key in self.volume.keys():
            if key == name:
                self.ren.RemoveVolume(self.volume[key])
                del self.volume[key]
        for key in self.actor.keys():
            for orientation in [1, 2, 3]:
                if key == name + "_cut_plane_" + str(orientation):
                    self.ren.RemoveActor(self.actor[key])
                    del self.actor[key]
        for key in self.matrix.keys():
            if key == name:
                del self.matrix[key]
        for key in self.reader.keys():
            if key == name:
                del self.reader[key]
        for key in self.volume_property.keys():
            if key == name:
                del self.volume_property[key]
        for key in self.property.keys():
            for orientation in [1, 2, 3]:
                if key == name + "_cut_plane_" + str(orientation):
                    del self.property[key]
        for key in self.vtkdata.keys():
            for orientation in [1, 2, 3]:
                if key == name + "_cut_plane_colors_" + str(orientation):
                    del self.vtkdata[key]
        for key in self.object_repr.keys():
            if key == name:
                del self.object_repr[key]

    def remove_polydata(self, name):
        for key in self.actor.keys():
            if key == name + "_polydata":
                self.ren.RemoveActor(self.actor[key])
                del self.actor[key]
        for key in self.property.keys():
            if key == name + "_polydata":
                del self.property[key]
        for key in self.object_repr.keys():
            if key == name:
                del self.object_repr[key]

    def remove_blending(self, name):
        for key in self.actor.keys():
            for orientation in [1, 2, 3]:
                if key == name + "_cut_plane_" + str(orientation):
                    self.ren.RemoveActor(self.actor[key])
                    del self.actor[key]
        for key in self.matrix.keys():
            if key == name:
                del self.matrix[key]
        for key in self.blend.keys():
            if key == name:
                del self.blend[key]
        for key in self.property.keys():
            for orientation in [1, 2, 3]:
                if key == name + "_cut_plane_" + str(orientation):
                    del self.property[key]
        for key in self.object_repr.keys():
            if key == name:
                del self.object_repr[key]

    def remove_actor(self, name):
        for key in self.actor.keys():
            if key == name:
                self.ren.RemoveActor(self.actor[key])
                del self.actor[key]
        for key in self.property.keys():
            if key == name:
                del self.property[key]
        for key in self.object_repr.keys():
            if key == name:
                del self.object_repr[key]

    def auto_focus(self):
        self.ren.ResetCamera()

    def render(self):
        self.iren.Render()

    def add_actor(self, name, actor, **kwargs):
        if name in self.actor:
            old_actor = self.actor[name]
            self.ren.RemoveActor(old_actor)
            del old_actor
        self.actor[name] = actor
        self.property[name] = dict(disp=True)

    def add_polydata(self, name, polydata, **kwargs):
        dtype = 'polydata'
        position = tuple(default_value(dtype, 'position', **kwargs))
        alpha = default_value(dtype, ['polydata_alpha', 'alpha'], **kwargs)
        cmap = default_value(dtype, ['polydata_colormap', 'colormap'], **kwargs)
        irange = default_value(dtype, 'intensity_range', **kwargs)
        linewidth = default_value(dtype, 'linewidth', **kwargs)

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata)

        polydata_actor = vtk.vtkActor()
        polydata_actor.SetMapper(mapper)
        polydata_actor.GetProperty().SetPointSize(1)

        if position is not None:
            polydata_actor.SetOrigin(position[0], position[1], position[2])
            # imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)
            polydata_actor.SetPosition(-position[0], -position[1], -position[2])

        self.add_actor('%s_polydata' % (name), polydata_actor)

        x_slice = default_value(dtype, 'x_slice', **kwargs)
        y_slice = default_value(dtype, 'y_slice', **kwargs)
        z_slice = default_value(dtype, 'z_slice', **kwargs)
        preserve_faces = default_value(dtype, 'preserve_faces', **kwargs)
        point_radius = default_value(dtype, 'point_radius', **kwargs)

        self.slice_polydata(name, x_slice=x_slice, y_slice=y_slice, z_slice=z_slice, preserve_faces=preserve_faces, point_radius=point_radius)

        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)

        cell_data = get_polydata_cell_data(self.actor[name + '_polydata'].GetMapper().GetInput())
        if irange == attribute_definition[dtype]['intensity_range']:
            irange = (cell_data.min(), cell_data.max())

        self.set_polydata_lookuptable(name, colormap=cmap, alpha=alpha, intensity_range=irange)
        self.set_polydata_alpha(name, alpha=alpha)
        self.set_polydata_linewidth(name, linewidth=linewidth)

    def set_polydata_lookuptable(self, name, colormap, **kwargs):

        irange = kwargs.pop('intensity_range', None)

        cell_data = get_polydata_cell_data(self.actor[name + '_polydata'].GetMapper().GetInput())
        lut = define_lookuptable(
            cell_data,
            colormap_points=colormap['color_points'],
            colormap_name=colormap['name'],
            intensity_range=irange)
        self.actor[name + '_polydata'].GetMapper().SetLookupTable(lut)

    def set_polydata_alpha(self, name, **kwargs):
        alpha = kwargs.get('alpha', self.actor[name + '_polydata'].GetProperty().GetOpacity())
        self.actor[name + '_polydata'].GetProperty().SetOpacity(alpha)

    def set_polydata_linewidth(self, name, **kwargs):
        linewidth = kwargs.get('linewidth', 1)
        self.actor[name + '_polydata'].GetProperty().SetLineWidth(linewidth)

    def set_polydata_point_radius(self, name, **kwargs):
        dtype = 'polydata'
        point_radius = default_value(dtype, 'point_radius', **kwargs)
        # print "Glyph Radius : ",point_radius
        object_polydata = self.object_repr[name]
        displayed_polydata = self.polydata[name]

        if (object_polydata.GetNumberOfCells() == 0) and (object_polydata.GetNumberOfPoints() > 0):
            # print "Setting Glyph Radius : ",point_radius
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(point_radius)
            sphere.SetThetaResolution(12)
            sphere.SetPhiResolution(12)
            glyph = vtk.vtkGlyph3D()
            glyph.SetScaleModeToDataScalingOff()
            glyph.SetColorModeToColorByScalar()
            glyph.SetSource(sphere.GetOutput())
            glyph.SetInput(displayed_polydata)
            glyph.Update()
            polydata = glyph.GetOutput()
        else:
            polydata = displayed_polydata

        mapper = self.actor[name + '_polydata'].GetMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata)

    def slice_polydata(self, name, **kwargs):
        dtype = 'polydata'
        x_slice = default_value(dtype, 'x_slice', **kwargs)
        y_slice = default_value(dtype, 'y_slice', **kwargs)
        z_slice = default_value(dtype, 'z_slice', **kwargs)
        preserve_faces = default_value(dtype, 'preserve_faces', **kwargs)

        if preserve_faces:
            slicing_function = vtk_sub_polydata
        else:
            slicing_function = vtk_clipped_polydata

        object_polydata = self.object_repr[name]
        point_polydata = (object_polydata.GetNumberOfCells() == 0) and (object_polydata.GetNumberOfPoints() > 0)

        polydata_extent = get_polydata_extent(object_polydata)
        clipping_plane = vtk.vtkPlane()
        sliced_polydata = vtk.vtkPolyData()
        sliced_polydata.DeepCopy(object_polydata)

        plane_coords = np.array([x_slice[0] / 100., 0.5, 0.5])
        plane_center = (1 - plane_coords) * polydata_extent[:, 0] + plane_coords * polydata_extent[:, 1]
        clipping_plane.SetOrigin(plane_center)
        clipping_plane.SetNormal(1, 0, 0)
        polydata = slicing_function(sliced_polydata, clipping_plane, point_polydata=point_polydata)
        # self.actor[name + '_polydata'].GetMapper().SetInput(slicing_function(sliced_polydata,clipping_plane))

        sliced_polydata.DeepCopy(polydata)
        plane_coords = np.array([x_slice[1] / 100., 0.5, 0.5])
        plane_center = (1 - plane_coords) * polydata_extent[:, 0] + plane_coords * polydata_extent[:, 1]
        clipping_plane.SetOrigin(plane_center)
        clipping_plane.SetNormal(1, 0, 0)
        polydata = slicing_function(sliced_polydata, clipping_plane, point_polydata=point_polydata, inside_out=True)

        sliced_polydata.DeepCopy(polydata)
        plane_coords = np.array([0.5, y_slice[0] / 100., 0.5])
        plane_center = (1 - plane_coords) * polydata_extent[:, 0] + plane_coords * polydata_extent[:, 1]
        clipping_plane.SetOrigin(plane_center)
        clipping_plane.SetNormal(0, 1, 0)
        polydata = slicing_function(polydata, clipping_plane, point_polydata=point_polydata)

        plane_coords = np.array([0.5, y_slice[1] / 100., 0.5])
        plane_center = (1 - plane_coords) * polydata_extent[:, 0] + plane_coords * polydata_extent[:, 1]
        clipping_plane.SetOrigin(plane_center)
        clipping_plane.SetNormal(0, 1, 0)
        polydata = slicing_function(polydata, clipping_plane, point_polydata=point_polydata, inside_out=True)

        sliced_polydata.DeepCopy(polydata)
        plane_coords = np.array([0.5, 0.5, z_slice[0] / 100.])
        plane_center = (1 - plane_coords) * polydata_extent[:, 0] + plane_coords * polydata_extent[:, 1]
        clipping_plane.SetOrigin(plane_center)
        clipping_plane.SetNormal(0, 0, 1)
        polydata = slicing_function(polydata, clipping_plane, point_polydata=point_polydata)

        sliced_polydata.DeepCopy(polydata)
        plane_coords = np.array([0.5, 0.5, z_slice[1] / 100.])
        plane_center = (1 - plane_coords) * polydata_extent[:, 0] + plane_coords * polydata_extent[:, 1]
        clipping_plane.SetOrigin(plane_center)
        clipping_plane.SetNormal(0, 0, 1)
        polydata = slicing_function(polydata, clipping_plane, point_polydata=point_polydata, inside_out=True)

        sliced_polydata.DeepCopy(polydata)
        self.polydata[name] = sliced_polydata
        self.set_polydata_point_radius(name, **kwargs)

    def add_outline(self, name, data_matrix, **kwargs):
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, np.uint16, 1)
        nx, ny, nz = data_matrix.shape
        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(reader.GetOutputPort())
        outline_mapper = vtk.vtkPolyDataMapper()
        outline_mapper.SetInputConnection(outline.GetOutputPort())
        outline_actor = vtk.vtkActor()
        outline_actor.SetOrigin(nx / 2., ny / 2., nz / 2.)
        outline_actor.SetPosition(- nx / 2., -ny / 2., -nz / 2.)
        outline_actor.SetMapper(outline_mapper)
        outline_actor.GetProperty().SetColor(1, 1, 1)
        self.add_actor('%s_outline' % (name), outline_actor)

    def add_matrix_cut_planes(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        """
        """
        if name in self.matrix:
            data_matrix = self.matrix[name]
        else:
            self.matrix[name] = data_matrix
        dtype = 'matrix'
        cmap = default_value(dtype, ['matrix_colormap', 'colormap'], **kwargs)
        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)

        resolution = default_value(dtype, 'resolution', **kwargs)
        position = default_value(dtype, 'position', **kwargs)
        alpha = default_value(dtype, 'cut_planes_alpha', **kwargs)

        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)

        # bwLut = define_lookuptable(data_matrix, colormap=self.colormaps["grey"])
        # colorLut = define_lookuptable(data_matrix, colormap=self.colormaps["glasbey"])
        # lut = define_lookuptable(data_matrix, colormap=self.colormaps[cmap])

        lut = define_lookuptable(data_matrix, colormap_points=cmap['color_points'], colormap_name=cmap['name'])

        for orientation in [1, 2, 3]:
            nx, ny, nz = data_matrix.shape
            xMax = nx - 1
            yMax = ny - 1
            zMax = nz - 1

            colors = vtk.vtkImageMapToColors()
            colors.SetInputConnection(reader.GetOutputPort())
            colors.SetLookupTable(lut)

            imgactor = vtk.vtkImageActor()
            imgactor.SetInput(colors.GetOutput())
            if orientation == 1:
                imgactor.SetDisplayExtent(
                    np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
            elif orientation == 2:
                imgactor.SetDisplayExtent(
                    0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
            elif orientation == 3:
                imgactor.SetDisplayExtent(
                    0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

            imgactor.SetScale(resolution[0], resolution[1], resolution[2])
            # imgactor, blend = blend_funct(data_matrix, reader, lut, reader, lut, orientation)
            # self.vtkdata['%s_blend_cut_plane_%d' % (name, orientation)] = blend

            if position is not None:
                imgactor.SetOrigin(position[0], position[1], position[2])
                imgactor.SetPosition(-position[0], -position[1], -position[2])

            self.reader[name] = reader = matrix_to_image_reader(
                name, data_matrix, datatype, decimate)

            self.vtkdata['%s_cut_plane_colors_%d' %
                         (name, orientation)] = colors
            self.add_actor('%s_cut_plane_%d' % (name, orientation), imgactor)

        self.set_cut_planes_alpha(name, alpha=alpha)
        return imgactor

    def add_matrix_as_volume(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        dtype = 'matrix'
        position = tuple(default_value(dtype, 'position', **kwargs))
        resolution = tuple(default_value(dtype, 'resolution', **kwargs))
        alpha = default_value(dtype, ['volume_alpha', 'alpha'], **kwargs)
        alphamap = default_value(dtype, 'alphamap', **kwargs)
        cmap = default_value(dtype, ['matrix_colormap', 'colormap'], **kwargs)
        bg_id = default_value(dtype, 'bg_id', **kwargs)

        irange = default_value(dtype, 'intensity_range', **kwargs)
        if irange == attribute_definition[dtype]['intensity_range']:
            irange = (data_matrix.min(), data_matrix.max())

        if name in self.matrix:
            data_matrix = self.matrix[name]
        else:
            self.matrix[name] = data_matrix

        self.reader[name] = reader = matrix_to_image_reader(
            name, data_matrix, datatype, decimate)

        compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
        volumeMapper = vtk.vtkVolumeRayCastMapper()
        volumeMapper.SetVolumeRayCastFunction(compositeFunction)
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        # colorFunc = vtk.vtkColorTransferFunction()
        colorFunc = vtk.vtkDiscretizableColorTransferFunction()
        alphaChannelFunc = vtk.vtkPiecewiseFunction()

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(colorFunc)
        volume_property.SetScalarOpacity(alphaChannelFunc)
        self.volume_property[name] = dict(
            vtkVolumeProperty=volume_property, disp=True)

        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volume_property)

        if position is not None:
            volume.SetOrigin(position[0], position[1], position[2])
            volume.SetPosition(-position[0], -position[1], -position[2])

        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)

        volume.SetScale(resolution[0], resolution[1], resolution[2])

        if name in self.volume:
            old_volume = self.volume[name]
            self.ren.RemoveVolume(old_volume)
            del old_volume
        self.volume[name] = volume

        self.set_matrix_lookuptable(name, cmap, intensity_range=irange, cut_planes=False)
        self.set_volume_alpha(name, alpha, alphamap, intensity_range=irange, bg_id=bg_id)

    def add_blending(self, name, object_names, data_matrices, **kwargs):
        dtype = 'matrix'

        self.matrix[name] = data_matrices[0]

        resolution = default_value(dtype, 'resolution', **kwargs)
        position = default_value(dtype, 'position', **kwargs)

        readers = {}
        colors = {}

        nx, ny, nz = data_matrices[0].shape
        xMax = nx - 1
        yMax = ny - 1
        zMax = nz - 1

        blend = vtk.vtkImageBlend()

        blending_factor = default_value(dtype, 'blending_factor', **kwargs)

        for i, object_name in enumerate(object_names):
            blend.AddInputConnection(self.vtkdata[object_name + '_cut_plane_colors_1'].GetOutputPort())
            if i == 0:
                blend.SetOpacity(i, 1)
            else:
                blend.SetOpacity(i, blending_factor)
            # blend.SetOpacity(i, i + (1-2*i)*blending_factor)
            # blend.SetOpacity(i, 0.8)
        blend.SetBlendModeToNormal()
        blend.Update()

        self.blend[name] = blend

        for orientation in [1, 2, 3]:
            # blend_actor, blend = blend_funct(data_matrix_1, reader_1, lut_1, reader_2, lut_2, orientation)

            blend_actor = vtk.vtkImageActor()
            blend_actor.SetInput(blend.GetOutput())
            if orientation == 1:
                blend_actor.SetDisplayExtent(
                    np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
            elif orientation == 2:
                blend_actor.SetDisplayExtent(
                    0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
            elif orientation == 3:
                blend_actor.SetDisplayExtent(
                    0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

            blend_actor.SetScale(resolution[0], resolution[1], resolution[2])

            if position is not None:
                blend_actor.SetOrigin(position[0], position[1], position[2])
                blend_actor.SetPosition(-position[0], -position[1], -position[2])

            self.add_actor('%s_cut_plane_%d' % (name, orientation), blend_actor)

    def set_cut_planes_alpha(self, name, alpha):
        alpha = default_value('matrix', 'cut_planes_alpha', cut_planes_alpha=alpha)
        for orientation in [1, 2, 3]:
            self.actor[name + "_cut_plane_" + str(orientation)].SetOpacity(alpha)

    def set_volume_alpha(self, name, alpha=1.0, alphamap="constant", **kwargs):
        alphaChannelFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetScalarOpacity()
        alphaChannelFunc.RemoveAllPoints()

        bg_id = kwargs.get('bg_id', None)
        sh_id = kwargs.get('sh_id', None)
        irange = kwargs.get('intensity_range', (self.matrix[name].min(), self.matrix[name].max()))

        if alphamap == "constant":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(irange[0], alpha)
            alphaChannelFunc.AddPoint(irange[1], alpha)

            if bg_id is not None:
                if not bg_id - 1 == sh_id:
                    alphaChannelFunc.AddPoint(bg_id - 1, alpha)
                alphaChannelFunc.AddPoint(bg_id, 0.0)
                if not bg_id + 1 == sh_id:
                    alphaChannelFunc.AddPoint(bg_id + 1, alpha)

            if sh_id is not None:
                if not sh_id - 1 == bg_id:
                    alphaChannelFunc.AddPoint(sh_id - 1, alpha)
                alphaChannelFunc.AddPoint(sh_id, kwargs.get('shade_alpha', 0.1))
                if not sh_id + 1 == bg_id:
                    alphaChannelFunc.AddPoint(sh_id + 1, alpha)

        elif alphamap == "linear":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(irange[0], 0.0)
            alphaChannelFunc.AddPoint(irange[1], alpha)

    def set_matrix_lookuptable(self, name, colormap, **kwargs):
        irange = kwargs.pop('intensity_range', None)

        cut_planes = kwargs.get('cut_planes', True)

        lut = define_lookuptable(self.matrix[name],
                                 colormap_points=colormap['color_points'],
                                 colormap_name=colormap['name'],
                                 intensity_range=irange)
        if 'sh_id' in kwargs:
            lut.AddRGBPoint(kwargs['sh_id'], *kwargs.get('shade_color', (0., 0., 0.)))
        self.volume_property[name]['vtkVolumeProperty'].SetColor(lut)
        if cut_planes:
            for orientation in [1, 2, 3]:
                if name + "_cut_plane_colors_" + str(orientation) in self.vtkdata:
                    self.vtkdata[
                        name + "_cut_plane_colors_" + str(orientation)].SetLookupTable(lut)

    def move_cut_plane(self, name, position=0, orientation=1):
        actor = self.actor['%s_cut_plane_%d' % (name, orientation)]
        data_matrix = self.matrix[name]
        nx, ny, nz = data_matrix.shape

        xMax = nx - 1
        yMax = ny - 1
        zMax = nz - 1
        bounds = [xMax, yMax, zMax]

        if position > bounds[orientation - 1]:
            position = bounds[orientation - 1]
        elif position < 0:
            position = 0

        if orientation == 1:
            actor.SetDisplayExtent(position, position, 0, yMax, 0, zMax)

        elif orientation == 2:
            actor.SetDisplayExtent(0, xMax, position, position, 0, zMax)

        elif orientation == 3:
            actor.SetDisplayExtent(0, xMax, 0, yMax, position, position)

        self.render()

    def set_blending_factor(self, name, blending_factor):

        blending_factor = default_value('matrix', 'blending_factor', blending_factor=blending_factor)

        blend = self.blend[name]
        for i in xrange(blend.GetTotalNumberOfInputConnections()):
            # blend.SetOpacity(i, i + (1-2*i)*blending_factor)
            if i == 0:
                blend.SetOpacity(i, 1)
            else:
                blend.SetOpacity(i, blending_factor)
        blend.Update()

        for orientation in [1, 2, 3]:
            self.actor[name + "_cut_plane_" + str(orientation)].SetInput(blend.GetOutput())
            self.actor[name + "_cut_plane_" + str(orientation)].Update()

        # for orientation in [1, 2, 3]:
            # blend_actor, blend = blend_funct(data_matrix_1, reader_1, lut_1, reader_2, lut_2, orientation)
            # actor = self.actor['%s_cut_plane_%d' % (name, orientation)]
            # actor.SetInput(blend.GetOutput())
            # if orientation == 1:
            #     blend_actor.SetDisplayExtent(
            #         np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
            # elif orientation == 2:
            #     blend_actor.SetDisplayExtent(
            #         0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
            # elif orientation == 3:
            #     blend_actor.SetDisplayExtent(
            #         0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

            # blend_actor.SetScale(resolution[0], resolution[1], resolution[2])

            # if position is not None:
            #     blend_actor.SetOrigin(position[0], position[1], position[2])
            #     blend_actor.SetPosition(-position[0], -position[1], -position[2])

    def cell_color(self, name, cell_id):
        colorFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetRGBTransferFunction()
        return colorFunc.GetColor(cell_id)

    def color_cell(self, name, cell_id=None, color=None, alpha=None):
        if color is None:
            color = (1., 1., 1.)
        if cell_id is None:
            cell_id = 1
        colorFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetRGBTransferFunction()
        colorFunc.RemoveAllPoints()
        colorFunc.AddRGBPoint(cell_id - 1, 1., 1., 1.)
        colorFunc.AddRGBPoint(cell_id, *color)
        colorFunc.AddRGBPoint(cell_id + 1, 1., 1., 1.)

    def old_color_cell(self, name, cell_id=None, color=None, alpha=None, bg_id=1, colormap='glasbey'):
        """
        TODO: replace with method that allows user to identify a cell
        """

        alphaChannelFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetScalarOpacity()

        if alpha is None:
            alpha = 1.

        # colorFunc.AddRGBPoint(bg_id, 1.0, 1.0, 1.0)

        for matrix in self.matrix.values():

            if cell_id is None:
                # colorFunc.RemoveAllPoints()

                # self.volume_property[name]['vtkVolumeProperty'].SetColor(
                    # define_lookuptable(matrix, colormap=self.colormaps[colormap]))

                self.volume_property[name]['vtkVolumeProperty'].SetColor(
                    define_lookuptable(matrix, colormap_points=self.colormaps[colormap]._color_points, colormap_name=colormap))

                alphaChannelFunc.RemoveAllPoints()

                alphaChannelFunc.AddPoint(bg_id, 0.0)

                if colormap not in ['glasbey']:
                    alphaChannelFunc.RemoveAllPoints()
                    alphaChannelFunc.AddPoint(matrix.min(), 0.0)
                    alphaChannelFunc.AddPoint(matrix.max(), alpha)
                else:
                    # alphaChannelFunc.AddPoint(1, 0.0)
                    alphaChannelFunc.AddPoint(bg_id + 1, alpha)
                    alphaChannelFunc.AddPoint(matrix.max(), alpha)

            else:
                if color is None:
                    color = (1., 1., 1.)
                colorFunc = self.volume_property[name][
                    'vtkVolumeProperty'].GetRGBTransferFunction()
                colorFunc.AddRGBPoint(cell_id, *color)

                alphaChannelFunc.AddPoint(cell_id, alpha)

    def set_interactor_style(self, interactor_style=None, **kwargs):
        if interactor_style is None:
            interactor_style = self.default_interactor_style
        self.interactor_style = interactor_style
        self.iren.SetInteractorStyle(interactor_style)
        interactor_style.SetCurrentRenderer(self.ren)
