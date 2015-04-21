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

from openalea.core.db import ErrorDbDatoDoNotExists, ErrorDbNotReachable
from openalea.core.path import path as Path


def browse_db(conn):
    if conn is None:
        return

    db_id = {}
    db_category = {}

    for group in conn.getGroupsMemberOf():
        group_id = group.getId()
        group_name = group.getName()
        group_path = group_name
        db_id[group_path] = group_id
        db_category[group_path] = 'Group'
        conn.SERVICE_OPTS.setOmeroGroup(group.getId())
        for project in conn.listProjects():
            project_id = project.getId()
            project_name = project.getName()
            project_path = '/'.join([group_path, project_name])
            db_id[project_path] = project_id
            db_category[project_path] = 'Project'
            for dataset in project.listChildren():
                dataset_id = dataset.getId()
                dataset_name = dataset.getName()
                dataset_path = '/'.join([project_path, dataset_name])
                db_id[dataset_path] = dataset_id
                db_category[dataset_path] = 'Dataset'
                for image in dataset.listChildren():
                    image_id = image.getId()
                    image_name = image.getName()
                    image_path = '/'.join([dataset_path, image_name])
                    db_id[image_path] = image_id
                    db_category[image_path] = 'Image'

        for dataset in conn.listOrphans('Dataset'):
            for image in dataset.listChildren():
                image_id = image.getId()
                image_name = image.getName()
                image_path = '/'.join([dataset_path, image_name])
                db_id[image_path] = image_id
                db_category[image_path] = 'Image'

        for image in conn.listOrphans('Image'):
            image_id = image.getId()
            image_name = image.getName()
            image_path = '/'.join([dataset_path, image_name])
            db_id[image_path] = image_id
            db_category[image_path] = 'Image'
    return db_category, db_id


class OmeroDb(object):

    def __init__(self):
        self._db_id = {}
        self._db_cat = {}

    def _parse(self, uri):
        username, uri = uri.split('@')
        host, uri = uri.split(':')
        port = uri.split('/')[0]
        uri = '/'.join(uri.split('/')[1:])
        if uri.startswith('id='):
            identifier = uri.lstrip('id=')
            uri = None
        else:
            identifier = None
        return username, host, port, uri, identifier

    def _get(self, username, host, port, uri, identifier, category='Image'):
        from openalea.oalab.gui.utils import password
        _passwd = password()
        if _passwd is None:
            return

        from omero.gateway import BlitzGateway
        conn = BlitzGateway(username, _passwd, host=host, port=port)
        if conn.connect():
            if identifier:
                img = conn.getObject(category, identifier)
                if img is None:
                    raise ErrorDbDatoDoNotExists('omero://%s@%s:%d/id:%s' % (username, host, port, identifier))
            else:
                if not self._db_id:
                    self._db_cat, self._db_id = browse_db(conn)
                identifier = self._db_id[uri]
                img = conn.getObject(category, identifier)
                if img is None:
                    raise ErrorDbDatoDoNotExists('omero://%s@%s:%d/%s' % (username, host, port, uri))
            from tissuelab.omero.utils import image_wrapper_to_ndarray
            matrix = image_wrapper_to_ndarray(img)
            return matrix
        else:
            raise ErrorDbNotReachable('omero://%s@%s:%d' % (username, host, port))

    def _download(self, path, username, host, port, uri, identifier):
        matrix = self._get(username, host, port, uri, identifier)
        from openalea.image.serial.basics import imsave
        from openalea.image.spatial_image import SpatialImage
        imsave(path, SpatialImage(matrix))
        return matrix

    def get(self, uri, path=None, force=False):
        username, host, port, uri, identifier = self._parse(uri)
        if path:
            path = Path(path)
            if path.exists() and force is False:
                from openalea.image.serial.basics import imread
                return imread(path)
            elif path.exists() and force is True:
                return self._download(path, username, host, port, uri, identifier)
            elif not path.exists():
                return self._download(path, username, host, port, uri, identifier)
        else:
            return self._get(username, host, port, uri, identifier)
