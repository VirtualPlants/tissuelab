# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       File contributor(s): Alizon König <alizon.konig@inria.fr>,
#                            Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

import numpy as np
import vtk

from scipy.cluster.vq import vq
from copy import deepcopy

from openalea.core.world.world import World
from tissuelab.gui.vtkviewer.vtkworldviewer import world_kwargs


class SelectPointInteractorStyle (vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None, world=None, points_name=None, image_name=None):
        #vtk.vtkInteractorStyleTrackballCamera.__init__(self,parent=parent)
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressed)
        self.AddObserver("KeyPressEvent", self.KeyPressed)
        self.AddObserver("MouseMoveEvent", self.MouseMoved)

        self.selected_cell = -1
        self.selected_axis = 'x'
        self.grab_mode = False

        if world is None:
            self.world = World()
        else:
            self.world = world

        self.world_object = self.world[points_name]
        self.data = deepcopy(self.world[points_name].data)

        self.image_world_object = self.world[image_name]

        self.cell_sphere = vtk.vtkSphereSource()
        self.cell_actor = vtk.vtkActor()

        self.axis_polydata = vtk.vtkPolyData()
        self.axis_polydata_actor = vtk.vtkActor()

        self.selected_axis_polydata = vtk.vtkPolyData()
        self.selected_axis_polydata_actor = vtk.vtkActor()

        self.motion_plane = vtk.vtkPlaneSource()
        self.motion_plane.SetResolution(100, 100)
        self.motion_plane.SetCenter(0.0, 0.0, 0.0)
        self.motion_plane.SetNormal(0.0, 0.0, 1.0)

        self.motion_plane.SetPoint1(100., 0.0, 0.0)
        self.motion_plane.SetPoint2(0., 100.0, 0.0)
        # self.motion_plane.SetPoint1(100.*np.array(self.motion_plane.GetPoint1()))
        # self.motion_plane.SetPoint2(np.cross([0,0,1],100.*np.array(self.motion_plane.GetPoint1())))
        self.motion_plane.Update()

        motion_plane_mapper = vtk.vtkPolyDataMapper()
        motion_plane_mapper.SetInputConnection(self.motion_plane.GetOutputPort())

        self.motion_plane_actor = vtk.vtkActor()
        self.motion_plane_actor.SetMapper(motion_plane_mapper)
        self.motion_plane_actor.GetProperty().SetColor(1.0, 0.0, 1.0)
        self.motion_plane_actor.GetProperty().SetOpacity(0.3)


    def add_selected_cell(self):
        self.cell_sphere.SetRadius(2.0)
        self.cell_sphere.SetThetaResolution(16)
        self.cell_sphere.SetPhiResolution(16)
        self.cell_sphere.SetCenter(self.data.points[self.selected_cell])

        cell_mapper = vtk.vtkPolyDataMapper()
        cell_mapper.SetInputConnection(self.cell_sphere.GetOutputPort())

        self.cell_actor.SetMapper(cell_mapper)
        self.cell_actor.GetProperty().SetColor(1.0, 1.0, 1.0)
        self.cell_actor.GetProperty().SetOpacity(0.3)

        for name in self.world.keys():
            if 'selected_cell' in name:
                self.world.remove(name)

        self.world.add(self.cell_actor, "selected_cell_"+str(self.selected_cell), position=self.world_object.get('position'))

    def add_axes(self):
        cell_center = np.array(self.cell_sphere.GetCenter())
        points = {}
        points['x-'] = deepcopy(cell_center)
        points['x-'][0] -= 1000.
        points['x+'] = deepcopy(cell_center)
        points['x+'][0] += 1000.
        points['y-'] = deepcopy(cell_center)
        points['y-'][1] -= 1000.
        points['y+'] = deepcopy(cell_center)
        points['y+'][1] += 1000.
        points['z-'] = deepcopy(cell_center)
        points['z-'][2] -= 1000.
        points['z+'] = deepcopy(cell_center)
        points['z+'][2] += 1000.

        axis_points = vtk.vtkPoints()
        axis_points.InsertNextPoint(points['x-'])
        axis_points.InsertNextPoint(points['x+'])
        axis_points.InsertNextPoint(points['y-'])
        axis_points.InsertNextPoint(points['y+'])
        axis_points.InsertNextPoint(points['z-'])
        axis_points.InsertNextPoint(points['z+'])

        colors = {}
        colors['red'] = (255, 0, 0)
        colors['green'] = (0, 255, 0)
        colors['blue'] = (0, 0, 255)

        #axis_colors.SetNumberOfComponents(3)
        #axis_colors.InsertNextTupleValue(colors['red'])
        #axis_colors.InsertNextTupleValue(colors['green'])
        #axis_colors.InsertNextTupleValue(colors['blue'])

        axis_colors = vtk.vtkUnsignedCharArray()
        axis_colors.SetNumberOfComponents(3)
        axis_lines = vtk.vtkCellArray()
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)
        line_id = axis_lines.InsertNextCell(line)
        axis_colors.InsertTupleValue(line_id, colors['red'])
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 2)
        line.GetPointIds().SetId(1, 3)
        line_id = axis_lines.InsertNextCell(line)
        axis_colors.InsertTupleValue(line_id, colors['green'])
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 4)
        line.GetPointIds().SetId(1, 5)
        line_id = axis_lines.InsertNextCell(line)
        axis_colors.InsertTupleValue(line_id, colors['blue'])

        self.axis_polydata.SetPoints(axis_points)
        self.axis_polydata.SetLines(axis_lines)
        self.axis_polydata.GetCellData().SetScalars(axis_colors)
        #self.world.add(axis_polydata,"axes",linewidth=1,colormap='glasbey')

        axis_mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            axis_mapper.SetInput(self.axis_polydata)
        else:
            axis_mapper.SetInputData(self.axis_polydata)

        self.axis_polydata_actor.SetMapper(axis_mapper)
        self.world.add(self.axis_polydata_actor, "axes", position=self.world_object.get('position'))
        #self.GetCurrentRenderer().AddActor(axis_polydata_actor)

    def add_selected_axis(self):
        cell_center = np.array(self.cell_sphere.GetCenter())
        points = {}
        points['x-'] = deepcopy(cell_center)
        points['x-'][0] -= 1000.
        points['x+'] = deepcopy(cell_center)
        points['x+'][0] += 1000.
        points['y-'] = deepcopy(cell_center)
        points['y-'][1] -= 1000.
        points['y+'] = deepcopy(cell_center)
        points['y+'][1] += 1000.
        points['z-'] = deepcopy(cell_center)
        points['z-'][2] -= 1000.
        points['z+'] = deepcopy(cell_center)
        points['z+'][2] += 1000.

        selected_axis_points = vtk.vtkPoints()
        selected_axis_points.InsertNextPoint(points['x-'])
        selected_axis_points.InsertNextPoint(points['x+'])
        selected_axis_points.InsertNextPoint(points['y-'])
        selected_axis_points.InsertNextPoint(points['y+'])
        selected_axis_points.InsertNextPoint(points['z-'])
        selected_axis_points.InsertNextPoint(points['z+'])

        colors = {}
        colors['red'] = (255, 0, 0)
        colors['green'] = (0, 255, 0)
        colors['blue'] = (0, 0, 255)

        selected_axis_colors = vtk.vtkUnsignedCharArray()
        selected_axis_colors.SetNumberOfComponents(3)
        selected_axis_lines = vtk.vtkCellArray()
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)
        if self.selected_axis == 'x':
            line_id = selected_axis_lines.InsertNextCell(line)
            selected_axis_colors.InsertTupleValue(line_id, colors['red'])
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 2)
        line.GetPointIds().SetId(1, 3)
        if self.selected_axis == 'y':
            line_id = selected_axis_lines.InsertNextCell(line)
            selected_axis_colors.InsertTupleValue(line_id, colors['green'])
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 4)
        line.GetPointIds().SetId(1, 5)
        if self.selected_axis == 'z':
            line_id = selected_axis_lines.InsertNextCell(line)
            selected_axis_colors.InsertTupleValue(line_id, colors['blue'])

        self.selected_axis_polydata.SetPoints(selected_axis_points)
        self.selected_axis_polydata.SetLines(selected_axis_lines)
        self.selected_axis_polydata.GetCellData().SetScalars(selected_axis_colors)

        selected_axis_mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            selected_axis_mapper.SetInput(self.selected_axis_polydata)
        else:
            selected_axis_mapper.SetInputData(self.selected_axis_polydata)

        self.selected_axis_polydata_actor.SetMapper(selected_axis_mapper)
        self.selected_axis_polydata_actor.GetProperty().SetLineWidth(3)
        self.world.add(self.selected_axis_polydata_actor, "selected_axis", position=self.world_object.get('position'))

    def update_motion_plane(self):
        camera_center = np.array(self.GetCurrentRenderer().GetActiveCamera().GetPosition())
        camera_focal_point = np.array(self.GetCurrentRenderer().GetActiveCamera().GetFocalPoint())
        cell_center = np.array(self.cell_sphere.GetCenter())
        self.motion_plane.SetCenter(cell_center)
        self.motion_plane.SetNormal((camera_center - cell_center) / np.linalg.norm(camera_center - cell_center))
        # self.motion_plane.SetNormal((camera_center-camera_focal_point)/np.linalg.norm(camera_center-camera_focal_point))
        self.motion_plane.Update()
        # self.world.add(self.motion_plane_actor,"motion_plane")

        # self.motion_picker.AddPickList(self.motion_plane_actor)

    def LeftButtonPressed(self, obj, event):
        if self.GetInteractor().GetShiftKey():
            self.selected_cell = -1
            pos = self.GetInteractor().GetEventPosition()
            self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
            points = self.GetInteractor().GetPicker().GetPickedPositions()
            coord = np.zeros(3)
            points.GetPoint(0, coord)

            if (self.GetInteractor().GetPicker().GetPointId() != -1):
                if len(self.data.points) > 0:
                    pick_cell_matching = vq(np.array([coord]+np.array(self.world_object.get('position'))), np.array(self.data.points.values()))
                    label = self.data.points.keys()[pick_cell_matching[0][0]]
                    self.selected_cell = label

                    self.add_selected_cell()

                    self.add_axes()
                    self.grab_mode = False
        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonDown(self)

        if self.selected_cell == -1:
            for name in self.world.keys():
                if 'selected_cell' in name:
                    self.world.remove(name)
            self.world.remove('axes')
            self.grab_mode = False
            self.world.remove("selected_axis")
            # self.world.remove("motion_plane")
            self.selected_cell == -1

    def KeyPressed(self, obj, event):
        #key = obj.GetKeySym()
        #key = self.GetInteractor().GetKeySym()
        key = self.GetInteractor().GetKeyCode().lower()
        motion_step = 0.5

        if self.selected_cell != -1:

            if key == 'f':
                position = np.array(self.cell_sphere.GetCenter())/np.array(self.image_world_object.get('resolution'))
                self.image_world_object.set_attribute('x_plane_position',int(np.round(position[0])))
                self.image_world_object.set_attribute('y_plane_position',int(np.round(position[1])))
                self.image_world_object.set_attribute('z_plane_position',int(np.round(position[2])))

            elif key == 'g':
                if self.grab_mode:
                    self.grab_mode = False
                    self.world.remove("selected_axis")
                    self.GetInteractor().GetPicker().DeletePickList(self.motion_plane_actor)
                    self.GetInteractor().GetPicker().PickFromListOff()
                    self.update_motion_plane()
                else:
                    self.grab_mode = True
                    self.selected_axis = 'x'
                    self.add_selected_axis()
                    self.update_motion_plane()
                    # self.GetInteractor().GetPicker().InitializePickList()
                    self.GetInteractor().GetPicker().AddPickList(self.motion_plane_actor)
                    self.GetInteractor().GetPicker().PickFromListOn()


            elif key in ['x', 'y', 'z']:
                if self.grab_mode:
                    if self.selected_axis != key:
                        self.selected_axis = key
                        self.add_selected_axis()
                        self.update_motion_plane()
                    else:
                        self.selected_axis = None
                        self.world.remove("selected_axis")

            elif key == 'q':
                for name in self.world.keys():
                    if 'selected_cell' in name:
                        self.world.remove(name)
                self.world.remove('axes')
                self.grab_mode = False
                self.world.remove("selected_axis")
                self.selected_cell == -1
                self.GetInteractor().GetPicker().DeletePickList(self.motion_plane_actor)
                self.GetInteractor().GetPicker().PickFromListOff()

            elif key in ['s', 'u', 'c']:
                # self.data.points[self.selected_cell] = self.world['selected_cell_'+str(self.selected_cell)].data.points[self.selected_cell]
                self.data.points[self.selected_cell] = np.array(self.cell_sphere.GetCenter())
                #self.world.add(self.data, self.world_object.name)
                if key == 'c':
                    self.data.point_data[self.selected_cell] = 1
                elif key == 'u':
                    self.data.point_data[self.selected_cell] = 0
                else:
                    if not self.selected_cell in self.data.point_data.keys():
                        self.data.point_data[self.selected_cell] = 1
                self.world[self.world_object.name].data = self.data
                for name in self.world.keys():
                    if 'selected_cell' in name:
                        self.world.remove(name)
                self.world.remove('axes')
                self.grab_mode = False
                self.world.remove("selected_axis")
                # self.world.remove("motion_plane")
                self.selected_cell == -1
                self.GetInteractor().GetPicker().DeletePickList(self.motion_plane_actor)
                self.GetInteractor().GetPicker().PickFromListOff()

            elif key == 'd':
                print self.selected_cell
                for name in self.world.keys():
                    if 'selected_cell' in name:
                        self.world.remove(name)
                self.world.remove('axes')
                self.grab_mode = False
                self.world.remove("selected_axis")
                # self.world.remove("motion_plane")
                if self.selected_cell in self.data.points.keys():
                    del self.data.points[self.selected_cell]
                if self.selected_cell in self.data.point_data.keys():
                    del self.data.point_data[self.selected_cell]

                    #self.world.add(self.data, self.world_object.name, **world_kwargs(self.world_object))
                    self.world[self.world_object.name].data = self.data
                self.selected_cell == -1
                self.GetInteractor().GetPicker().DeletePickList(self.motion_plane_actor)
                self.GetInteractor().GetPicker().PickFromListOff()

            elif key == 'a':
                added_cell = np.sort(list(set(np.arange(np.max(self.data.points.keys())+2)).difference(set(self.data.points.keys()))))[0]
                if added_cell != self.selected_cell:
                    print "Add cell : ",added_cell
                    self.selected_cell = added_cell
                    self.grab_mode = True
                    self.selected_axis = 'x'
                    self.add_selected_axis()
                    self.update_motion_plane()
                    # self.GetInteractor().GetPicker().InitializePickList()
                    self.GetInteractor().GetPicker().AddPickList(self.motion_plane_actor)
                    self.GetInteractor().GetPicker().PickFromListOn()

    def MouseMoved(self, obj, event):
        if self.grab_mode:
            pos = self.GetInteractor().GetEventPosition()
            self.GetInteractor().GetPicker().Pick(pos[0], pos[1], 0, self.GetCurrentRenderer())
            # points = self.GetInteractor().GetPicker().GetPickedPositions()
            coord = np.zeros(3)

            mouse_position = self.GetInteractor().GetPicker().GetPickPosition()
            # points.GetPoint(0, coord)
            # print coord

            # camera_center = np.array(self.GetCurrentRenderer().GetActiveCamera().GetPosition())
            cell_center = np.array(self.cell_sphere.GetCenter())
            # renderer_aspect = self.GetCurrentRenderer().GetAspect()
            # camera_matrix = self.GetCurrentRenderer().GetActiveCamera().GetProjectionTransformMatrix(renderer_aspect[0]/renderer_aspect[1],0,1)
            # camera_matrix = np.array([[camera_matrix.GetElement(i,j) for j in xrange(4)] for i in xrange(4)])
            # print camera_matrix
            # print np.dot(camera_matrix,np.concatenate([cell_center,[1]]))

            if self.selected_axis is None:
                plane_normal = np.array(self.motion_plane.GetNormal())
                plane_normal = plane_normal / np.linalg.norm(plane_normal)
                plane_vector_1 = np.array(self.motion_plane.GetPoint1()) - cell_center
                plane_vector_1 = plane_vector_1 / np.linalg.norm(plane_vector_1)
                plane_vector_2 = np.cross(plane_normal, plane_vector_1)
                new_cell_center = deepcopy(cell_center)
                new_cell_center += np.dot(mouse_position - cell_center, plane_vector_1) * plane_vector_1
                new_cell_center += np.dot(mouse_position - cell_center, plane_vector_2) * plane_vector_2
                # new_cell_center = mouse_position
            elif self.selected_axis == 'x':
                new_cell_center = cell_center + \
                    np.dot(mouse_position - cell_center, np.array([1, 0, 0])) * np.array([1, 0, 0])
            elif self.selected_axis == 'y':
                new_cell_center = cell_center + \
                    np.dot(mouse_position - cell_center, np.array([0, 1, 0])) * np.array([0, 1, 0])
            elif self.selected_axis == 'z':
                new_cell_center = cell_center + \
                    np.dot(mouse_position - cell_center, np.array([0, 0, 1])) * np.array([0, 0, 1])
            self.cell_sphere.SetCenter(new_cell_center)

            for p in xrange(self.axis_polydata.GetNumberOfPoints()):
                self.axis_polydata.GetPoints().SetPoint(
                    p,
                    (np.array(
                        self.axis_polydata.GetPoint(p)) +
                        new_cell_center -
                        cell_center))

            self.world.add(self.cell_actor, "selected_cell_"+str(self.selected_cell))
            self.world.add(self.axis_polydata_actor, "axes")

            if self.selected_axis is not None:
                for p in xrange(self.selected_axis_polydata.GetNumberOfPoints()):
                    self.selected_axis_polydata.GetPoints().SetPoint(
                        p,
                        (np.array(
                            self.selected_axis_polydata.GetPoint(p)) +
                            new_cell_center -
                            cell_center))
                self.world.add(self.selected_axis_polydata_actor, "selected_axis")

                self.update_motion_plane()
                vtk.vtkInteractorStyleTrackballCamera.OnMouseMove(self)
        else:
            vtk.vtkInteractorStyleTrackballCamera.OnMouseMove(self)
