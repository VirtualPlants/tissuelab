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

__all__ = ['OmeroDbBrowser', 'OmeroModel', 'OmeroView']
from cStringIO import StringIO

from openalea.vpltk.qt import QtGui, QtCore
from openalea.image.pil import Image
from openalea.vpltk.qt.QtCore import Signal
from utils import memoized

import omero

#metadata_cache= {}

def hash_img(img):
    return 0, str(img.getId())

def dataset_to_items(dataset):
    item_type_dataset = QtGui.QStandardItem('dataset')
    item_dataset = QtGui.QStandardItem(dataset.getName())
    item_id = QtGui.QStandardItem(unicode(dataset.getId()))

    item_dataset.setData(dataset)

    return [item_dataset, item_type_dataset, item_id]


def project_to_items(project):
    item_type_project = QtGui.QStandardItem('project')
    item_project = QtGui.QStandardItem(project.getName())
    item_id = QtGui.QStandardItem(unicode(project.getId()))

    item_project.setData(project)

    return [item_project, item_type_project, item_id]


def group_to_items(group):
    item_type_group = QtGui.QStandardItem('group')
    item_group = QtGui.QStandardItem(group.getName())
    item_id = QtGui.QStandardItem(unicode(group.getId()))

    item_group.setData(group)

    return [item_group, item_type_group, item_id]


class OmeroModel(QtGui.QStandardItemModel):

    def __init__(self):
        self._connection = None
        self._data = []
        self.view = OmeroView()

        QtGui.QStandardItemModel.__init__(self)

    def setConnection(self, omero_connection):
        self._connection = omero_connection
        self.refresh()

    def refresh(self):
        # Here we should use a backend strategy to be able to change
        # db type easily
        self.clear()
        conn = self._connection
        if conn is None:
            return

        for group in conn.getGroupsMemberOf():
            row_group = group_to_items(group)
            self.appendRow(row_group)
            row_group[0].appendRow([QtGui.QStandardItem('Loading...'),
                                    QtGui.QStandardItem('...'),
                                    QtGui.QStandardItem(unicode(0))])

        self.setColumnCount(4)

    def omeroObject(self, idx):
        item = self.itemFromIndex(idx)
        parent = item.parent()
        if parent:
            item = parent.child
        else:
            item = self.item

        data_type = str(item(idx.row(), 1).text()).capitalize()
        data_id = int(item(idx.row(), 2).text())
        if data_type == 'Group':
            return None
        else:
            return self._connection.getObject(data_type, data_id)

class OmeroView(QtGui.QTreeView):
    objectSelected = Signal(object)
    imageSelected = Signal(object)

    def __init__(self):
        QtGui.QTreeView.__init__(self)
        self.expanded.connect(self.expandChildren)
        # self.itemClicked.connect(self.popUp)

        self.setEditTriggers(QtGui.QTreeView.NoEditTriggers)

        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self.setIconSize(QtCore.QSize(50, 50))
        self.fineTune()

    def setClient(self, omeroClient):
        self.client = omeroClient

    def fineTune(self):
        for icol in range(4):
            self.resizeColumnToContents(icol)
        titles = ['Category', 'Name', 'Id', 'Image']
        if self.model():
            self.model().setHorizontalHeaderLabels(titles)

    @memoized(hash_img, 100)
    def image_info(self,image):
        tags     = []
        comments = []
        keyvals  = []

        for ann in image.listAnnotations():
            if isinstance(ann, omero.gateway.TagAnnotationWrapper):
                tags.append(ann.getValue())
            if isinstance(ann, omero.gateway.MapAnnotationWrapper):
                keyvals.append(ann.getValue())
            if isinstance(ann, omero.gateway.CommentAnnotationWrapper):
                comments.append(ann.getValue())

        info = "Image Name : %s\n" % image.getName()
        info += "Image ID : %d\n" % image.getId()
        info += "Image Owner: %s\n" % image.getOwnerFullName()
        desc = image.getDescription()
        if desc == '':
            info += "Image Description : None\n"
        else:
            info += "Image Description : %s\n" % desc
        info += "Import Date: %s\n" % image.getDate()
        info += "Dimensions (XY): %d " % image.getSizeX() + "x %d\n" % image.getSizeY()
        info += "Pixels Size (XYZ) (um): %s " % image.getPixelSizeX() + "x  %s " % image.getPixelSizeY() + "x %s\n" % image.getPixelSizeZ()
        info += "Pixels Type: %s\n" % image.getPixelsType()
        info += "Z-sections/Timepoints: %d " % image.getSizeZ() + " x %d\n" % image.getSizeT()
        info += "ROI Count: %d\n" % image.getROICount()
        info += "Channels: %s\n" % image.getChannelLabels()

        if not tags:
            info += "Tags: None\n"
        else:
            info += "Tags: %s\n" % tags

        if not keyvals:
            info += "Key-Value Pairs: None\n"
        else:
            info += "Key-Value Pairs: %s\n" % keyvals

        if not comments:
            info += "Comments: None"
        else:
            info += "Comments: %s" % comments
        return info

    @memoized(hash_img, 500)
    def image_to_thumb(self, image):
        img_data = image.getThumbnail()
        renderedThumb = Image.open(StringIO(img_data))
        filename = "thumbnail_%d.png" % image.getId()

        renderedThumb.save(filename, 'PNG')
        return QtGui.QIcon(filename)

    def image_to_items(self, image):
        img_id = unicode(image.getId())
        item_type_image = QtGui.QStandardItem('image')
        item_image = QtGui.QStandardItem(image.getName())
        item_id = QtGui.QStandardItem(img_id)
        item_thumbnail = QtGui.QStandardItem()

        item_image.setData(image)
        img_icon = self.image_to_thumb(image)
        item_thumbnail.setIcon(img_icon)
        img_info = self.image_info(image)

        item_thumbnail.setToolTip(img_info)

        return [item_image, item_type_image, item_id, item_thumbnail]

    def expandChildren(self, index):
        item = self.model().itemFromIndex(index)
        parent = item.parent()
        if parent:
            item = parent.child
        else:
            item = self.model().item
        type = str(item(index.row(), 1).text()).capitalize()
        id = int(item(index.row(), 2).text())
        _it = self.model().itemFromIndex(index)
        conn = self.model()._connection
        self.setCursor(QtCore.Qt.WaitCursor)
        if type == 'Group':
            _it.removeRows(0, _it.rowCount())
            conn.SERVICE_OPTS.setOmeroGroup(id)
            for i, project in enumerate(conn.listProjects()):
                row_project = project_to_items(project)
                _it.appendRow(row_project)
                row_project[0].appendRow([QtGui.QStandardItem('Loading...'),
                                          QtGui.QStandardItem('...'),
                                          QtGui.QStandardItem(unicode(0))])
            for i, dataset in enumerate(conn.listOrphans('Dataset')):
                row_dataset = dataset_to_items(dataset)
                _it.appendRow(row_dataset)
                row_dataset[0].appendRow([QtGui.QStandardItem('Loading...'),
                                          QtGui.QStandardItem('...'),
                                          QtGui.QStandardItem(unicode(0))])
            for image in conn.listOrphans('Image'):
                row_img = self.image_to_items(image)
                _it.appendRow(row_img)

        if type == 'Project':
            _it.removeRows(0, _it.rowCount())
            for i, dataset in enumerate(_it.data().listChildren()):
                row_dataset = dataset_to_items(dataset)
                _it.appendRow(row_dataset)
                row_dataset[0].appendRow([QtGui.QStandardItem('Loading...'),
                                          QtGui.QStandardItem('...'),
                                          QtGui.QStandardItem(unicode(0))])
                # for image in dataset.listChildren():
                #     row_dataset[0].removeRows(0, _it.rowCount())
                #     row_img = image_to_items(image)
                #     row_dataset[0].appendRow(row_img)
        if type == 'Dataset':
            _it.removeRows(0, _it.rowCount())
            for i, image in enumerate(_it.data().listChildren()):
                row_img = self.image_to_items(image)
                _it.appendRow(row_img)
        self.fineTune()
        self.setCursor(QtCore.Qt.ArrowCursor)

    def currentChanged(self, current, previous):
        try:
            obj = self.model().omeroObject(current)
            self.objectSelected.emit(obj)

        except:
            self.client.reconnect()

    # Drag and drop

    def startDrag(self, supportedActions):
        from openalea.core.service.mimetype import encode
        index = self.selectedIndexes()
        obj = self.model().omeroObject(index[0])
        conn = self.model()._connection

        uri = '%(NAME)s = omero://%(USER)s@%(HOST)s:%(PORT)s/id=%(ID)s' % dict(
            USER=conn._ic_props['omero.user'],
            PORT=conn.port,
            HOST=conn.host,
            NAME=obj.getName(),
            ID=obj.getId(),
        )

        mimetype, mimedata = encode(uri, mimetype='openalealab/omero')
        qmime_data = QtCore.QMimeData()
        qmime_data.setData(mimetype, mimedata)
        qmime_data.setText(obj.getName())
        drag = QtGui.QDrag(self)
        drag.setMimeData(qmime_data)
        drag.start()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalealab/omero"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("openalealab/omero"):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        event.ignore()


class OmeroDbBrowser(QtGui.QWidget):
    objectSelected = Signal(object)
    imageSelected = Signal(object)

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.view = OmeroView()
        self.model = OmeroModel()
        self.view.setModel(self.model)

        self.grid = QtGui.QGridLayout(self)
        self.grid.addWidget(self.view, 0, 0)

        self.resize(QtCore.QSize(800, 600))

        self.view.objectSelected.connect(self.objectSelected.emit)
        self.view.imageSelected.connect(self.imageSelected.emit)

    def setConnection(self, omero_connection):
        self.model.setConnection(omero_connection)
        self.view.fineTune()

    def setClient(self, omeroClient):
        self.client = omeroClient
        self.view.setClient(omeroClient)


if __name__ == '__main__':
    import sys
    # import tissuelab.omero
    app = QtGui.QApplication.instance()
    if app:
        EMBEDED = True
    else:
        EMBEDED = False
        app = QtGui.QApplication(sys.argv)

    from omero.gateway import BlitzGateway
    conn = BlitzGateway('root', 'omero', host='localhost', port=4064)
    conn.connect()

    def f(obj):
        print 'image:', obj

    w = OmeroDbBrowser()
    w.imageSelected.connect(f)
    w.setConnection(conn)
    w.show()

    if not EMBEDED:
        app.exec_()

    conn._closeSession()
