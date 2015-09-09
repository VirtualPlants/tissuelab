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

from openalea.oalab.plugin.builtin.lab.default import DefaultLab


class TissueLab(DefaultLab):
    __plugin__ = True
    name = 'tissue'
    icon = 'icon_tissuelab.png'
    label = 'Tissue'

    applets = [
        'ProjectManager',
        'ControlManager',
        'PkgManagerWidget',
        'EditorManager',
        'VtkViewer',
        'Viewer3D',
        'OmeroClient',
        'HelpWidget',
        'Logger',
        'HistoryWidget',
        'World',
        'LineageViewer',
    ]

    connections = []

    layout = {'parents': {0: None, 13: 0, 14: 0, 15: 14, 16: 14, 17: 16, 18: 16, 19: 13, 20: 13, 21: 15, 22: 15},
              'properties': {
        0: {u'amount': 0.24132492113564669, u'splitDirection': 1},
        13: {u'amount': 0.46854460093896716, u'splitDirection': 2},
        14: {u'amount': 0.5823488533703961, u'splitDirection': 1},
        15: {u'amount': 0.7474178403755869, u'splitDirection': 2},
        16: {u'amount': 0.49107981220657276, u'splitDirection': 2},
        17: {u'widget': {'applets': [{'name': u'FigureWidget', 'properties': {'num': 3}}]}},
        18: {u'widget': {'applets': [{'name': u'TissueViewer'}], 'properties': {}}},
        19: {u'widget': {'applets': [{'name': u'ProjectManager'}], 'properties': {}}},
        20: {u'widget': {'applets': [
            {'name': u'WorldControl'},
            {'name': u'ControlManager', 'properties': {'position': 2, 'icon': None}},
            {'name': u'PkgManagerWidget'}
        ], 'properties': {}}},
        21: {u'widget': {'applets': [{'name': u'EditorManager'}]}},
        22: {u'widget': {'applets': [{'name': u'ShellWidget'}]}}},
        'children': {0: [13, 14], 16: [17, 18], 13: [19, 20], 14: [15, 16], 15: [21, 22]}}

    def __call__(self, mainwin=None):
        if mainwin is None:
            return self.__class__

        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
