
import vtk
import numpy as np

from openalea.core.observer import AbstractListener
from openalea.core.path import path as Path
from openalea.deploy.shared_data import shared_data

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.world import World
from openalea.core.service.ipython import interpreter as get_interpreter
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


def list_colormaps():
    colormap_names = []

    import tissuelab
    colormaps_path = Path(shared_data(tissuelab, 'colormaps/grey.lut')).parent

    for colormap_file in colormaps_path.walkfiles('*.lut'):
        colormap_name = str(colormap_file.name[:-4])
        colormap_names.append(colormap_name)
    colormap_names.sort()
    return colormap_names


def load_colormaps():
    from tissuelab.gui.vtkviewer.colormap_utils import Colormap, colormap_from_file
    colormaps = {}

    import tissuelab
    colormaps_path = Path(shared_data(tissuelab, 'colormaps/grey.lut')).parent

    for colormap_file in colormaps_path.walkfiles('*.lut'):
        colormap_name = str(colormap_file.name[:-4])
        print colormap_name
        colormaps[colormap_name] = colormap_from_file(
            colormap_file, name=colormap_name)
    return colormaps


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
                lut.AddRGBPoint(i, * colormap_points.values()[i])
        else:
            for i in np.unique(image):
                lut.AddRGBPoint(i, *colormap_points.values()[i % 256])
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


class VtkViewerWidget(QtGui.QWidget, AbstractListener):
    matrixAdded = QtCore.Signal(str)
    worldChanged = QtCore.Signal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        AbstractListener.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.vtk = VtkViewer()  # embedded into the VtkViewerWidget
        self.vtk.matrixAdded.connect(self.matrixAdded.emit)
        layout.addWidget(self.vtk)

        self.world = World()
        self.world.register_listener(self)

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_viewer'] = self
        self.interpreter.locals['viewer'] = self.vtk

        self._create_actions()
        self._create_connections()

    def _create_actions(self):
        self.action_auto_focus = QtGui.QAction(
            QtGui.QIcon(":/images/resources/resetzoom.png"), 'Auto focus', self)

    def _create_connections(self):
        self.action_auto_focus.triggered.connect(self.vtk.auto_focus)

    def toolbar_actions(self):
        return [
            self.action_auto_focus
        ]

    def notify(self, sender, event=None):
        signal, data = event
        print "VtkViewer : ",signal,"! ",data
        if signal == 'world_sync':
            self.worldChanged.emit()
            self.set_world(data)
        elif signal == 'world_object_changed':
            self.worldChanged.emit()
            self.set_world(data[0])

    def set_world(self, world):
        self.vtk.clear()
        for obj_name, world_object in world.items():
            if hasattr(world_object, "transform"):
                obj = world_object.transform()
            elif hasattr(world_object, "_repr_vtk_"):
                obj = world_object._repr_vtk_()
            else:
                obj = world_object.obj
            if isinstance(obj, np.ndarray):
                self.vtk.add_matrix(
                    obj_name, obj, datatype=obj.dtype, **world_object.kwargs)
            if isinstance(obj, vtk.vtkPolyData):
                self.vtk.add_polydata(obj_name, obj, **world_object.kwargs)
            if isinstance(obj, vtk.vtkActor):
                self.vtk.add_actor(obj_name, obj, **world_object.kwargs)
        self.vtk.compute()


class VtkViewer(QtGui.QWidget):
    matrixAdded = QtCore.Signal(str)

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

        layout.addWidget(self.frame)
        self.ren.ResetCamera()

        self.colormaps = load_colormaps()

        # vtk objects (like vtk volumes, vtk actors...) sorted by name in a
        # dictionnary
        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.property = {}

    def display_volume(self, name=None, disp=True):
        self.clear_scene()
        self._display_volume(name, disp)
        self.compute()

    def display_cut_planes(self, name=None, disp=True):
        self.clear_scene()
        self._display_cut_planes(name, disp)
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

    def initialize(self):
        pass
#         self.ren.ResetCamera()
#         self.iren.AddObserver("MouseMoveEvent", self.on_cursor_moved)


#     def on_cursor_moved(self, iren, event):
#         if self.picker is None:
#             return
#         x, y = iren.GetEventPosition()
#         self.picker.Pick(x, y, 0, self.ren)
#         print self.picker.GetSubId()

    def clear_scene(self):
        for name, volume in self.volume.items():
            self.ren.RemoveVolume(volume)
        for name, actor in self.actor.items():
            self.ren.RemoveActor(actor)

    def clear(self):
        for name, volume in self.volume.items():
            self.ren.RemoveVolume(volume)
            del self.volume[name]
        for name, actor in self.actor.items():
            self.ren.RemoveActor(actor)
            del self.actor[name]

        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.vtkdata = {}

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

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata)

        if polydata.GetCellData().GetNumberOfComponents() > 0:
            cmap = kwargs.get('colormap', 'glasbey')
            cell_data = np.frombuffer(polydata.GetCellData().GetArray(0), np.uint32)
            lut = define_lookuptable(cell_data, colormap_points=self.colormaps[cmap]._color_points, colormap_name=cmap)
        elif polydata.GetPointData().GetNumberOfComponents() > 0:
            cmap = kwargs.get('colormap', 'glasbey')
            cell_data = np.frombuffer(polydata.GetPointData().GetArray(0), np.uint32)
            lut = define_lookuptable(cell_data, colormap_points=self.colormaps[cmap]._color_points, colormap_name=cmap)
        else:
            cmap = kwargs.get('colormap', 'grey')
            lut = define_lookuptable(
                np.arange(1),
                colormap_points=self.colormaps[cmap]._color_points,
                colormap_name=cmap,
                i_min=0,
                i_max=1)
            # lut = define_lookuptable(np.arange(1), colormap=self.colormaps[cmap], i_min=0, i_max=1)

        mapper.SetLookupTable(lut)

        polydata_actor = vtk.vtkActor()
        polydata_actor.SetMapper(mapper)
        polydata_actor.GetProperty().SetPointSize(1)

        self.add_actor('%s_polydata' % (name), polydata_actor)

    def set_polydata_lookuptable(self, name, colormap='grey', **kwargs):
        # lut = define_lookuptable(np.arange(1), colormap=self.colormaps[colormap])
        lut = define_lookuptable(
            np.arange(1),
            colormap_points=self.colormaps[colormap]._color_points,
            colormap_name=colormap)
        self.actor[name + '_polydata'].GetMapper().SetLookupTable(lut)

    def set_polydata_property(self, name, property=None, **kwargs):
        cmap = kwargs.get('colormap', 'grey')
        i_min = kwargs.get('i_min', None)
        i_max = kwargs.get('i_max', None)

        n_triangles = self.actor[name + '_polydata'].GetMapper().GetInput().GetPolys().GetNumberOfCells()

        vtk_property = vtk.vtkLongArray()
        if property is None:
            for t in xrange(n_triangles):
                vtk_property.InsertValue(t, t)
            # lut = define_lookuptable(np.arange(n_triangles), colormap=self.colormaps[cmap])
            lut = define_lookuptable(
                np.arange(n_triangles),
                colormap_points=self.colormaps[cmap]._color_points,
                colormap_name=cmap)
        else:
            assert len(property.keys()) == n_triangles
            for (fid, t) in zip(property.keys(), xrange(n_triangles)):
                vtk_property.InsertValue(t, property[fid])

            # lut = define_lookuptable(np.array(property.values()), colormap=self.colormaps[cmap], i_min=i_min, i_max=i_max)
            lut = define_lookuptable(
                np.array(
                    property.values()),
                colormap_points=self.colormaps[cmap]._color_points,
                colormap_name=cmap,
                i_min=i_min,
                i_max=i_max)

        self.actor[name + '_polydata'].GetMapper().GetInput().GetCellData().SetScalars(vtk_property)

        self.actor[name + '_polydata'].GetMapper().SetLookupTable(lut)

    def add_matrix(self, name, data_matrix, datatype=np.uint8, decimate=1, **kwargs):
        self.matrix[name] = data_matrix

        self.add_matrix_as_volume(
            name, data_matrix, datatype, decimate, **kwargs)
        self.add_matrix_cut_planes(
            name, data_matrix, datatype, decimate, **kwargs)

        self._display_cut_planes(name, kwargs.get('cut_planes', True))
        self._display_volume(name, kwargs.get('volume', True))

        self.matrixAdded.emit(name)

    def add_matrix_cut_planes(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        self.reader[name] = reader = matrix_to_image_reader(
            name, data_matrix, datatype, decimate)
        cmap = kwargs.get('colormap', 'grey')
        alpha = kwargs.get('alpha', 1.0)
        # bwLut = define_lookuptable(data_matrix, colormap=self.colormaps["grey"])
        # colorLut = define_lookuptable(data_matrix, colormap=self.colormaps["glasbey"])
        # lut = define_lookuptable(data_matrix, colormap=self.colormaps[cmap])
        lut = define_lookuptable(data_matrix, colormap_points=self.colormaps[cmap]._color_points, colormap_name=cmap)
        resolution = kwargs.get('resolution', (1.0, 1.0, 1.0))

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

            imgactor.SetOrigin(nx / 2., ny / 2., nz / 2.)
            # imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)
            imgactor.SetPosition(- nx / 2., -ny / 2., -nz / 2.)
            imgactor.SetScale(resolution[0], resolution[1], resolution[2])
            # imgactor, blend = blend_funct(data_matrix, reader, lut, reader, lut, orientation)
            # self.vtkdata['%s_blend_cut_plane_%d' % (name, orientation)] = blend
            self.vtkdata['%s_cut_plane_colors_%d' %
                         (name, orientation)] = colors
            self.add_actor('%s_cut_plane_%d' % (name, orientation), imgactor)
        self.set_cut_planes_alpha(name, alpha)

    def add_matrix_as_volume(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        nx, ny, nz = data_matrix.shape
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

        volume = self.volume[name] = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volume_property)
        volume.SetOrigin(nx / 2., ny / 2., nz / 2.)
        # volume.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)
        volume.SetPosition(- nx / 2., -ny / 2., -nz / 2.)

        resolution = kwargs.get('resolution', (1.0, 1.0, 1.0))
        volume.SetScale(resolution[0], resolution[1], resolution[2])

        cmap = kwargs.get('colormap', 'grey')
        alpha = kwargs.get('alpha', 1.0)
        alphamap = kwargs.get('alphamap', 'linear')
        # self.color_cell(name, alpha=alpha, colormap=cmap)
        self.set_matrix_lookuptable(name, cmap, cut_planes=False)
        self.set_volume_alpha(name, alpha, alphamap)

    def set_volume_alpha(self, name, alpha=1.0, alphamap="constant", **kwargs):
        alphaChannelFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetScalarOpacity()
        alphaChannelFunc.RemoveAllPoints()

        bg_id = kwargs.get('bg_id', None)
        i_min = kwargs.get('i_min', self.matrix[name].min())
        i_max = kwargs.get('i_max', self.matrix[name].max())

        if alphamap == "constant":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(i_min, alpha)
            alphaChannelFunc.AddPoint(i_max, alpha)

            if bg_id is not None:
                alphaChannelFunc.AddPoint(bg_id - 1, alpha)
                alphaChannelFunc.AddPoint(bg_id, 0.0)
                alphaChannelFunc.AddPoint(bg_id + 1, alpha)

        elif alphamap == "linear":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(i_min, 0.0)
            alphaChannelFunc.AddPoint(i_max, alpha)

    def set_cut_planes_alpha(self, name, alpha=1.0, **kwargs):
        for orientation in [1, 2, 3]:
            self.actor[
                name + "_cut_plane_" + str(orientation)].SetOpacity(alpha)

    def set_matrix_lookuptable(self, name, colormap='grey', **kwargs):
        i_min = kwargs.get('i_min', None)
        i_max = kwargs.get('i_max', None)
        cut_planes = kwargs.get('cut_planes', True)
        # lut = define_lookuptable(self.matrix[name], self.colormaps[colormap], i_min, i_max)
        lut = define_lookuptable(self.matrix[name],
                                 colormap_points=self.colormaps[colormap]._color_points, colormap_name=colormap, i_min=i_min, i_max=i_max)
        self.volume_property[name]['vtkVolumeProperty'].SetColor(lut)
        if cut_planes:
            for orientation in [1, 2, 3]:
                self.vtkdata[
                    name + "_cut_plane_colors_" + str(orientation)].SetLookupTable(lut)

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

                # if colormap == 'random':
                #     from random import random as r
                #     for i in np.unique(matrix):
                #         colorFunc.AddRGBPoint(i, r(), r(), r())
                # elif colormap == 'monocolor':
                #     for i in np.unique(matrix):
                #         colorFunc.AddRGBPoint(i, *color)

                # elif colormap == 'grey':
                # colorFunc.AddRGBPoint(matrix.min(),0.0,0.0,0.0)
                # colorFunc.AddRGBPoint(matrix.max(),1.0,1.0,1.0)
                # colorFunc.AddHSVPoint(matrix.min(),0.0,1.0,0.5)
                # colorFunc.AddHSVPoint(matrix.max(),0.5,1.0,0.5)

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

    # def color_intensity(self, name, intensity_min=0, intensity_max=255,
    # colormap='grey'):

    #     colorFunc = self.volume_property[name]['vtkVolumeProperty'].GetRGBTransferFunction()
    #     alphaChannelFunc = self.volume_property[name]['vtkVolumeProperty'].GetScalarOpacity()

    def demo_matrix_xyz(self):
        dtype = np.uint16
        matrix = np.zeros([100, 100, 100], dtype=dtype)
        matrix[90:100, 0:10, 0:10] = 1
        matrix[0:10, 90:100, 0:10] = 2
        matrix[0:10, 0:10, 90:100] = 3
        return matrix

    def demo_matrix1(self):
        dtype = np.uint16
        matrix = np.zeros([75, 75, 75], dtype=dtype)
        matrix[25:55, 25:55, 25:55] = 1
        matrix[45:74, 45:74, 45:74] = 10
        return matrix

    def demo_matrix2(self):
        dtype = np.uint16
        matrix = np.zeros([75, 75, 75], dtype=dtype)
        matrix[0:10, 0:10, 0:10] = 1

        return matrix

    def demo_actor(self):
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        return actor

    def demo(self):

        self.clear()

        matrix1 = self.demo_matrix1()
        matrix2 = self.demo_matrix2()
        sphere = self.demo_actor()

        self.add_matrix('matrix1', matrix1)
        self.color_cell('matrix1')

        self.add_matrix('matrix2', matrix2)
        self.color_cell('matrix2', colormap='monocolor')

        self.add_actor('sphere', sphere)

        self.compute()

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)
