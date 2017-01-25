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

from Qt import QtCore, QtGui, QtWidgets

from openalea.core.service.control import create_control, group_controls
from openalea.oalab.utils import ModalDialog, qicon
from openalea.oalab.service.qt_control import edit

from tissuelab.omero.omerodbbrowser import OmeroDbBrowser

class OmeroClient(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.browser = OmeroDbBrowser()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.browser)

        self._create_menu()

        # TODO: should be moved to service or manager
        from openalea.core.service.ipython import interpreter
        interpreter().user_ns['db'] = self

        self._current = [None, None, None]
        self._connection = None

    def _create_menu(self):
        self.menu = QtWidgets.QMenu('Omero')

        self.action_connect_db = QtWidgets.QAction(
            qicon('Crystal_Clear_filesystem_socket.png'), u'Connect to database', self)
        self.action_connect_db.triggered.connect(self.connect)

        self.action_reload_db = QtWidgets.QAction(
            qicon('Crystal_Clear_Quick_restart.png'), u'Reload database', self)
        self.action_reload_db.triggered.connect(self.reload)

        self.action_close_db = QtWidgets.QAction(
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

    def connect(self, username=None, password=None, host='localhost', port=4064):
        if username is None or password is None:
            username = create_control('username', 'IStr')
            password = create_control('password', 'IStr')
            host = create_control('host', 'IStr', value=host)
            port = create_control('port', 'IInt', value=port, constraints={'min': 0, 'max': 65536})
            gr = group_controls([username, password, host, port])
            container = edit(gr)
            qt_password = container.editor[password]()
            qt_password.setEchoMode(QtWidgets.QLineEdit.Password)
            dialog = ModalDialog(container)
            if dialog.exec_():
                username = username.value
                password = password.value
                host = host.value
                port = port.value
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
