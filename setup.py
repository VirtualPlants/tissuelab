# -*- coding: utf-8 -*-
__revision__ = "$Id: setup.py 16731 2014-06-02 15:42:19Z gbaty $"


from setuptools import setup, find_packages

name = 'tissuelab'
version = '0.1'
description = 'OpenAleaLab extension Tissue'
long_description = description
authors = 'VP'
authors_email = 'vp'
url = 'url'

packages = find_packages('tissuelab')

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
    packages=['tissuelab'],
    package_dir={'tissuelab': 'tissuelab'},

    zip_safe=False,
    include_package_data=True,

    # Declare src and wralea as entry_points (extensions) of your package
    entry_points={

        'oalab.applet': [
            'VtkViewer = tissuelab.plugin.applet:VtkViewer',
            'VtkControlPanel = tissuelab.plugin.applet:VtkControlPanel',
            'OmeroClient = tissuelab.plugin.applet:OmeroClient',
            'LineageViewer = tissuelab.plugin.applet:LineageViewer',
        ],

        'oalab.lab': [
            'TissueLab = tissuelab.plugin.lab:TissueLab',
        ],

        'oalab.interface': [
        ],


    },
)
