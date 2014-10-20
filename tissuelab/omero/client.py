
from openalea.core.service.control import create_control, group_controls
from openalea.oalab.gui.utils import ModalDialog
from openalea.oalab.service.qt_control import edit
from openalea.vpltk.qt import QtCore, QtGui
from tissuelab.omero.omerodbbrowser import OmeroDbBrowser

class OmeroClient(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.browser = OmeroDbBrowser()

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.browser)

        self._create_menu()

        # TODO: should be moved to service or manager
        from openalea.oalab.session.session import Session
        session = Session()
        session.interpreter.locals['db'] = self

        self._current = [None, None, None]
        self._connection = None

    def _create_menu(self):
        self.menu = QtGui.QMenu('Omero')

        self.action_connect_db = QtGui.QAction(u'Connect to database', self)
        self.action_connect_db.triggered.connect(self.connect)

        self.menu.addAction(self.action_connect_db)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        menu.addAction(self.action_connect_db)
        menu.exec_(event.globalPos())

    def connect(self, username=None, password=None, host='localhost', port=4064):
        if username is None or password is None:
            username = create_control('username', 'IStr')
            password = create_control('password', 'IStr')
            host = create_control('host', 'IStr', value=host)
            port = create_control('port', 'IInt', value=port, constraints={'min':0, 'max':65536})
            gr = group_controls([username, password, host, port])
            editor = edit(gr)
            dialog = ModalDialog(editor)
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
                from omero.gateway import BlitzGateway
                conn = BlitzGateway(username, password, host=host, port=port)
                conn.connect()
                self._current = [username, host, port]
                self._connection = conn
                self.browser.setConnection(conn)

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
        image = self.read(category='Image', uid=uid)

        # Prepare plane list...
        sizeZ = image.getSizeZ()
        sizeC = image.getSizeC()
        sizeT = image.getSizeT()
        zctList = []

        for z in range(sizeZ):
            for c in range(sizeC):
                for t in range(sizeT):
                    zctList.append((z, c, t))

        planes = image.getPrimaryPixels().getPlanes(zctList)

        import numpy
        seg = numpy.array(list(planes))

        return seg