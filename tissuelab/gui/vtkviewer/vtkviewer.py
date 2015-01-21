
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
                self.vtk.add_matrix(obj_name, obj)
            if isinstance(obj, vtk.vtkActor):
                self.vtk.add_actor(obj_name, obj)
        # self.vtk.compute()


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

    def add_matrix(self, name, data_matrix, datatype=np.uint16, decimate=1):
        matrix = self.matrix[name] = data_matrix

        nx, ny, nz = matrix.shape
        data_string = matrix.tostring('F')

        reader = self.reader[name] = vtk.vtkImageImport()
        reader.CopyImportVoidPointer(data_string, len(data_string))
        reader.SetDataScalarTypeToUnsignedShort()
        reader.SetNumberOfScalarComponents(1)
        reader.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
        reader.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)

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
