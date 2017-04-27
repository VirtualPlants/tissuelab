# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################


from openalea.core.service.control import create_control, group_controls
from openalea.core.control.manager import ControlContainer

from openalea.oalab.utils import ModalDialog, qicon
from openalea.oalab.service.qt_control import edit
from openalea.oalab.service.drag_and_drop import add_drop_callback
from openalea.vpltk.qt import QtGui
import weakref
from tissuelab.omero.omerodbbrowser import OmeroDbBrowser

from openalea.core.settings import Settings

omero_attributes = {}
# omero_attributes['project'] = dict(value="",interface="IEnumStr",constraints=dict(enum=[""]),label="Project") 
omero_attributes['dataset'] = dict(value="",interface="IEnumStr",constraints=dict(enum=[""]),label="Dataset") 
omero_attributes['filename'] = dict(value="",interface="IStr",constraints={},label="Filename")

class OmeroExportPanel(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        self._connection = None

        self._manager = ControlContainer()
        # self._view = ControlManagerWidget(manager=self._manager)
        self._view = None

        self._layout = QtGui.QVBoxLayout(self)

        self.refresh_manager()

        self._label = QtGui.QLabel(u"Enter where to save image")
        self._layout.addWidget(self._label)

        # self._layout.addWidget(self._view)

        self.refresh_view()


    # def notify(self, sender, event=None):
    #     signal, data = event

    def refresh_manager(self):
        self._manager.clear_followers()
        self._manager.clear()
        for name in ['dataset','filename']:
            attribute = omero_attributes[name]
            self._manager.add(name, interface=attribute['interface'], value=attribute['value'], label=attribute['label'], constraints=attribute['constraints'])
            # self._manager.register_follower(name, self._item_changed(name))
        self._manager.enable_followers()
    
    def refresh_view(self):
        view = self._view
        if self._view is not None:
            view = self._view()
        if view:
            self._layout.removeWidget(view)
            view.close()
            del view
        view = edit(self._manager)
        view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._view = weakref.ref(view)
        self._layout.addWidget(view)

    def update_connection(self, conn):
        self._connection = conn
        # project_list = [p.getName() for p in conn.listProjects()]
        self._manager.disable_followers()
        # self._manager.control('project').interface.enum = project_list

        dataset_list = []
        for project in conn.listProjects():
            dataset_list += [d.getName()+"@"+project.getName()+":id="+str(d.getId()) for d in project.listChildren()]
        self._manager.control('dataset').interface.enum = dataset_list

        # self.refresh_manager()
        self.refresh_view()
        self._manager.enable_followers()

    def update_image_name(self, name):
        self._manager.disable_followers()
        self._manager.control('filename').value = name
        # self.refresh_manager()
        self.refresh_view()
        self._manager.enable_followers()

    def get_project(self):
        import re
        dataset_uri = self._manager.control('dataset').value
        dataset_name, project_name = re.match("(.+)@(.+):",dataset_uri).groups()
        projects = [p for p in self._connection.listProjects() if p.getName() == project_name]
        return None if len(projects)==0 else projects[0]

    def get_dataset(self):
        import re
        dataset_uri = self._manager.control('dataset').value
        dataset_id = re.match(".*id=(\d+)", dataset_uri).groups()[0]
        return self._connection.getObject('Dataset',dataset_id)

    def get_filename(self):
        return self._manager.control('filename').value

    # def _item_changed(self, item):
    #     def _changed(old, new):
    #         self._omero_item_changed(item, old, new)
    #     return _changed

    # def _omero_item_changed(self, item, old, new):
    #     print item, new
    #     self._manager.disable_followers()
    #     if self._connection:
    #         if item == 'project':
    #             project_name = new
    #             projects = [p for p in self._connection.listProjects() if p.getName() == project_name]

    #             if len(projects)>0:
    #                 project = projects[0]
    #                 dataset_list = [d.getName() for d in project.listChildren()]
    #                 self._manager.control('dataset').interface.enum = dataset_list
    #             else:
    #                 self._manager.control('dataset').interface.enum = [""]
    #             self.refresh_view()

    #     print self._manager.controls()
    #     raw_input()
    #     self._manager.enable_followers()

        # for project in conn.listProjects():
        #         row_project = project_to_items(project)
        #         row_group[0].appendRow(row_project)
        #         for dataset in project.listChildren():

class OmeroClient(QtGui.QWidget):


    connectionEstablished = QtCore.Signal(str, bool)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.browser = OmeroDbBrowser()
        self.browser.setClient(self)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.browser)

        self._create_menu()

        # TODO: should be moved to service or manager
        from openalea.core.service.ipython import interpreter
        interpreter().user_ns['omerodb'] = self

        add_drop_callback(self, 'openalea/interface.IImage', self.drop_image)

        self._current = [None, None, None]
        self._connection = None

    def _create_menu(self):
        self.menu = QtGui.QMenu('Omero')

        self.action_connect_db = QtGui.QAction(
            qicon('Crystal_Clear_filesystem_socket.png'), u'Connect to database', self)
        self.action_connect_db.triggered.connect(self.connect)

        self.action_reload_db = QtGui.QAction(
            qicon('Crystal_Clear_Quick_restart.png'), u'Reload database', self)
        self.action_reload_db.triggered.connect(self.reload)

        self.action_close_db = QtGui.QAction(
            qicon('Crystal_Clear_Action-delete-icon.png'), u'Close database', self)
        self.action_close_db.triggered.connect(self.close_db)

        self.menu.addAction(self.action_connect_db)
        self.menu.addAction(self.action_reload_db)
        self.menu.addAction(self.action_close_db)

    def toolbar_actions(self):
        return [
            self.action_connect_db,
            self.action_reload_db,
            self.action_close_db,
        ]

    def menu_actions(self):
        return [
            self.action_connect_db,
            self.action_reload_db,
            self.action_close_db,
        ]

    def menus(self):
        return [self.menu]

    def reconnect(self):
        [username, host, port] =  self._current
        print "closing old db"
        self.close_db()
        password = self.password
        self.connect(username, password, host, port)

    def connect(self, username=None, password=None, host='localhost', port=4064):
        if username is None or password is None:

            config = Settings()
            try:
                username = config.get("omero", "username")
                host = config.get("omero", "host")
                port = int(config.get("omero", "port"))
            except:
                username = None
                host = "localhost"
                port = 4064

            username = create_control('username', 'IStr', value=username)
            password = create_control('password', 'IStr')
            host = create_control('host', 'IStr', value=host)
            port = create_control('port', 'IInt', value=port, constraints={'min': 0, 'max': 65536})
            gr = group_controls([username, password, host, port])
            container = edit(gr)
            qt_password = container.editor[password]()
            qt_password.setEchoMode(QtGui.QLineEdit.Password)
            dialog = ModalDialog(container)
            if dialog.exec_():
                username = username.value
                password = password.value
                host = host.value
                port = port.value
                config.set("omero", "username", username)
                config.set("omero", "host", host)
                self.password = password
                config.set("omero", "port", str(port))
                config.write()

            else:
                username = None

        if [username, host, port] == self._current:
            return
        elif username is not None:
            if self._connection:
                self._connection._closeSession()
            from omero.gateway import BlitzGateway
            conn = BlitzGateway(username, password, host=host, port=port)
            conn.connect()
            self._current = [username, host, port]
            self._connection = conn
            self.browser.setConnection(conn)

        # for project in conn.listProjects():
        #         row_project = project_to_items(project)
        #         row_group[0].appendRow(row_project)
        #         for dataset in project.listChildren():

    def reload(self):
        self.browser.model.refresh()
        self.browser.view.fineTune()

    def close_db(self):
        self._current = [None, None, None]
        self._connection._closeSession()
        self.browser.setConnection(None)
        self._connection = None

    def read(self, **kwargs):
        """
        category,uid
        """
        if not self._connection:
            return
        category = kwargs['category'] if 'category' in kwargs else None
        uid = kwargs['uid'] if 'uid' in kwargs else None
        if uid and category:
            return self._connection.getObject(category, uid)

    def get_image(self, uid):
        image_wrapper = self.read(category='Image', uid=uid)
        from tissuelab.omero.utils import image_wrapper_to_ndarray
        return image_wrapper_to_ndarray(image_wrapper)

    def get_voxelsize(self, uid):
        image_wrapper = self.read(category='Image', uid=uid)
        vs = (image_wrapper.getPixelSizeX(),image_wrapper.getPixelSizeY(),image_wrapper.getPixelSizeZ())
        return tuple([s if s is not None else 1 for s in vs])

    def drop_image(self, obj, **kwargs):
        from tissuelab.omero.utils import nd_array_to_image_generator
        from omero.model import DatasetI

        img = obj
        print kwargs.get('name',"Unnamed"),img.shape
        img_name = kwargs.get('name',"Unnamed")


        size_z = img.shape[2]
        size_c = 1
        size_t = 1

        if self._connection:

            export_panel = OmeroExportPanel()
            dialog = ModalDialog(export_panel)
            export_panel.setParent(dialog)
            export_panel.update_connection(self._connection)
            export_panel.update_image_name(img_name+".tif")
            
            if dialog.exec_():
                project = export_panel.get_project()
                dataset = export_panel.get_dataset()
                img_filename = export_panel.get_filename()
                
                if dataset is not None:
                    ds = dataset._obj

                    self._connection.SERVICE_OPTS['omero.group']= str(self._connection.getGroupFromContext().getId())

                    omero_image = self._connection.createImageFromNumpySeq(nd_array_to_image_generator(img)(), img_name+".tif", size_z, size_c, size_t, description="", dataset=ds)
                    omero_image = self._connection.getObject("Image", omero_image.getId())

                    voxelsize = kwargs.get('voxelsize',(1,1,1))
                    if hasattr(img,'voxelsize'):
                        voxelsize = img.voxelsize

                    from omero.model.enums import UnitsLength
                    from omero.model import LengthI
                    
                    p = omero_image.getPrimaryPixels()._obj
                    p.setPhysicalSizeX(LengthI(voxelsize[0], UnitsLength.MICROMETER))
                    p.setPhysicalSizeY(LengthI(voxelsize[1], UnitsLength.MICROMETER))
                    p.setPhysicalSizeZ(LengthI(voxelsize[2], UnitsLength.MICROMETER))
                    self._connection.getUpdateService().saveObject(p)

                    self.browser.model.refresh()
                    self.browser.view.fineTune()

            else:
                pass


