# -*- coding: utf-8 -*-
__revision__ = "$Id: setup.py 16731 2014-06-02 15:42:19Z gbaty $"

import os
import os.path as osp
from setuptools import setup, find_packages

name = 'tissuelab'
version = '0.1'
description = 'OpenAleaLab extension Tissue'
long_description = description
authors = 'VP'
authors_email = 'vp'
url = 'url'


def get_package_data(name, extlist):
    """Return data files for package name with extensions in extlist
    Thanks to Pierre Raybaut, Spyder (http://spyderlib.googlecode.com)"""
    flist = []
    # Workaround to replace os.path.relpath (not available until Python 2.6):
    offset = len(name) + len(os.pathsep)
    for dirpath, _dirnames, filenames in os.walk(name):
        for fname in filenames:
            if not fname.startswith('.') and osp.splitext(fname)[1] in extlist:
                flist.append(osp.join(dirpath, fname)[offset:])
    return flist


def get_subpackages(name):
    """Return subpackages of package name.
    Thanks to Pierre Raybaut, Spyder (http://spyderlib.googlecode.com)"""
    splist = []
    for dirpath, _dirnames, _filenames in os.walk(name):
        if osp.isfile(osp.join(dirpath, '__init__.py')):
            splist.append(".".join(dirpath.split(os.sep)))
    return splist

data_ext = [
    # Documentation
    '.txt', '.html',
    # Images
    '.png', '.jpg', '.svg',
    # Databases
    '.xml',
    # Qt
    '.ui',
    # i18n
    '.mo', '.ts', '.po',
    # templates
    '.template', '.NFG',
    # colormaps
    '.lut'
]

sphinx_ext = [
    '.txt',
    '.html',
    '.js',
    '.inv',
    '.css',
    '.png',
    '.gif',
]

packages = get_subpackages('tissuelab')

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='',

    # package installation
    packages=packages,

    zip_safe=False,
    include_package_data=True,
    package_data={'tissuelab':get_package_data('tissuelab', data_ext)},

    # Declare src and wralea as entry_points (extensions) of your package
    entry_points={

        'gui_scripts': [
            'pymage = tissuelab.gui.pymage:main',
        ],

        'oalab.applet': [
            'oalab.applet/tissuelab = tissuelab.plugin.applet',
        ],

        'oalab.lab': [
            'oalab.lab/tissuelab = tissuelab.plugin.lab',
        ],

        'oalab.db': [
            'oalab.db/tissuelab = tissuelab.plugin.db',
        ],

    },
)
