
import vtk
import numpy as np

from openalea.core.observer import AbstractListener
from openalea.vpltk.qt import QtGui
from openalea.oalab.world import World
from openalea.core.service.ipython import interpreter as get_interpreter
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


def define_LUT(image, LUT_type):
    lut = vtk.vtkLookupTable()
    if LUT_type == "bw":
        lut.SetTableRange(image.min(), image.max())
        lut.SetSaturationRange(0, 0)
        lut.SetHueRange(0, 0)
        lut.SetValueRange(0, 1)
    elif LUT_type == "color":
        lut.SetNumberOfTableValues(image.max() + 1)
        lut.SetNumberOfColors(image.max() + 1)
        lut.SetRange(image.min(), image.max())
    lut.Build()
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


def blend_funct(data_matrix, data1, LUT1, data2, LUT2, orientation):
    nx, ny, nz = data_matrix.shape
    xMax = nx - 1
    yMax = ny - 1
    zMax = nz - 1

    p1Colors = vtk.vtkImageMapToColors()
    p1Colors.SetInputConnection(data1.GetOutputPort())
    p1Colors.SetLookupTable(LUT1)
    p2Colors = vtk.vtkImageMapToColors()
    p2Colors.SetInputConnection(data2.GetOutputPort())
    p2Colors.SetLookupTable(LUT2)
    blend = vtk.vtkImageBlend()
    blend.AddInput(p1Colors.GetOutput())
    blend.AddInput(p2Colors.GetOutput())
    blend.SetOpacity(0, 0.5)
    blend.SetOpacity(1, 0.5)
    imgactor = vtk.vtkImageActor()
    imgactor.SetInput(blend.GetOutput())
    if orientation == 1:
        imgactor.SetDisplayExtent(np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
    elif orientation == 2:
        imgactor.SetDisplayExtent(0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))
    elif orientation == 3:
        imgactor.SetDisplayExtent(0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)

    imgactor.SetOrigin(nx / 2., ny / 2., nz / 2.)
    imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)

    return imgactor, blend


class VtkControlPanel(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QVBoxLayout(self)

        from openalea.oalab.service.qt_control import qt_editor
        from openalea.core.control import Control
        x = Control('x', 'IInt', 0)
        x.interface.min = 0
        x.interface.max = 255
        editor = qt_editor(x)
        self._layout.addWidget(editor)


class VtkViewerWidget(QtGui.QWidget, AbstractListener):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        AbstractListener.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.vtk = VtkViewer()
        layout.addWidget(self.vtk)

        self.world = World()
        self.world.register_listener(self)

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_viewer'] = self
        self.interpreter.locals['viewer'] = self.vtk

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_sync':
            self.set_world(data)

    def set_world(self, world):
        self.vtk.clear()
        for obj_name, world_object in world.items():
            obj = world_object.obj
            if isinstance(obj, np.ndarray):
                self.vtk.add_matrix(obj_name, obj, datatype=obj.dtype)
            if isinstance(obj, vtk.vtkActor):
                self.vtk.add_actor(obj_name, obj)
        self.vtk.compute()


class VtkViewer(QtGui.QWidget):

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

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        layout.addWidget(self.frame)
        self.ren.ResetCamera()

        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}

    def display_volume(self, disp=True):
        self._display_volume(disp)
        self.compute()

    def _display_volume(self, disp=True):
        for name, volume in self.volume.items():
            self.ren.RemoveVolume(volume)
            del self.volume[name]
        self.volume_property.clear()
        if disp:
            for name, data_matrix in self.matrix.items():
                self.add_matrix_as_volume(name, data_matrix, data_matrix.dtype)
        else:
            pass

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
        elif position < bounds[orientation - 1]:
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
            self.ren.AddVolume(volume)
        for name, actor in self.actor.items():
            self.ren.AddActor(actor)

        self.iren.Initialize()
        self.iren.Start()
        self.ren.ResetCamera()
        self.render()

    def render(self):
        self.iren.Render()

    def add_actor(self, name, actor):
        self.actor[name] = actor

    def add_matrix(self, name, data_matrix, datatype=np.uint8, decimate=1):
        self.matrix[name] = data_matrix
        self.add_matrix_cut_planes(name, data_matrix, datatype, decimate)

    def add_matrix_cut_planes(self, name, data_matrix, datatype=np.uint16, decimate=1):
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)
        bwLut = define_LUT(data_matrix, "bw")
        colorLut = define_LUT(data_matrix, "color")
        for orientation in [1, 2, 3]:
            actor, blend = blend_funct(data_matrix, reader, bwLut, reader, colorLut, orientation)
            self.vtkdata['%s_blend_cut_plane_%d' % (name, orientation)] = blend
            self.add_actor('%s_cut_plane_%d' % (name, orientation), actor)

    def add_matrix_as_volume(self, name, data_matrix, datatype=np.uint16, decimate=1):
        nx, ny, nz = data_matrix.shape
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)

        compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
        volumeMapper = vtk.vtkVolumeRayCastMapper()
        volumeMapper.SetVolumeRayCastFunction(compositeFunction)
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        colorFunc = vtk.vtkColorTransferFunction()
        alphaChannelFunc = vtk.vtkPiecewiseFunction()

        volume_property = self.volume_property[name] = vtk.vtkVolumeProperty()
        volume_property.SetColor(colorFunc)
        volume_property.SetScalarOpacity(alphaChannelFunc)

        volume = self.volume[name] = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volume_property)
        volume.SetOrigin(nx / 2., ny / 2., nz / 2.)
        volume.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)

        self.color_cell(name)

    def color_cell(self, name, cell_id=None, color=None, alpha=None, bg_id=0, cmap='default'):

        colorFunc = self.volume_property[name].GetRGBTransferFunction()
        alphaChannelFunc = self.volume_property[name].GetScalarOpacity()

        if alpha is None:
            alpha = 1.

        if color is None:
            color = (1., 1., 1.)

        colorFunc.AddRGBPoint(bg_id, 1.0, 1.0, 1.0)
        alphaChannelFunc.AddPoint(bg_id, 0.0)

        for matrix in self.matrix.values():

            if cell_id is None:

                if cmap == 'random':
                    from random import random as r
                    for i in np.unique(matrix):
                        colorFunc.AddRGBPoint(i, r(), r(), r())
                elif cmap == 'monocolor':
                    for i in np.unique(matrix):
                        colorFunc.AddRGBPoint(i, *color)
                else:
                    m = np.max(matrix)
                    for i in np.unique(matrix):
                        if i != 0:
                            colorFunc.AddRGBPoint(i, i / np.float(m), 1 - i / np.float(m), 0.0)

                for i in np.unique(matrix):
                    if i != 0:
                        alphaChannelFunc.AddPoint(i, alpha)

            else:
                colorFunc.AddRGBPoint(cell_id, *color)
                alphaChannelFunc.AddPoint(cell_id, alpha)

    def demo_matrix1(self):
        dtype = np.uint16
        matrix1 = np.zeros([75, 75, 75], dtype=dtype)
        matrix1[25:55, 25:55, 25:55] = 1
        matrix1[45:74, 45:74, 45:74] = 10
        return matrix1

    def demo_matrix2(self):
        dtype = np.uint16
        matrix2 = np.zeros([75, 75, 75], dtype=dtype)
        matrix2[0:10, 0:10, 0:10] = 1

        return matrix2

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
        self.color_cell('matrix2', cmap='monocolor')

        self.add_actor('sphere', sphere)

        self.compute()

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)
