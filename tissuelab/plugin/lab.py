from openalea.oalab.plugins.labs.default import DefaultLab


class TissueLab(DefaultLab):
    name = 'tissue'
    icon = 'icon_tissuelab.png'
    alias = 'Tissue'

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

    connections = [
        ('VtkViewer:matrixAdded', 'VtkControlPanel:set_matrix'),
        ('VtkControlPanel:attributeChanged', 'World:change_object_attribute'),
#        ('VtkViewer:worldChanged', 'VtkControlPanel:clear'),
    ]

    layout = {
        'children': {0: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 7: [11, 12], 8: [9, 10]},
        'parents': {0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 8, 10: 8, 11: 7, 12: 7},
        'properties': {
            0: {'amount': 0.04774535809018567, 'splitDirection': 2},
            1: {'widget':
                {'applets': [
                    {'name': u'ContextualMenu'}],
                 'properties': {'position': 0}
                 }},
            2: {'amount': 0.1609375, 'splitDirection': 1},
            3: {'amount': 0.4850467289719626, 'splitDirection': 2},
            4: {'amount': 0.6540136901057871, 'splitDirection': 1},
            5: {'widget':
                {'applets': [
                    {'name': u'ProjectManager'}],
                 'properties': {'position': 0, 'title': '<b>Project</b>'}
                 }},
            6: {'widget':
                {'applets': [
                    {'name': u'VtkControlPanel'},
                    {'name': u'ControlManager'},
                    {'name': u'World'},
                    {'name': u'PkgManagerWidget'}],
                 'properties': {'position': 0}
                 }},
            7: {'amount': 0.7252336448598131, 'splitDirection': 2},
            8: {'amount': 0.4803738317757009, 'splitDirection': 2},
            9: {'widget':
                {'applets': [
                    {'name': u'LineageViewer'},
                    {'name': u'FigureWidget'}
                ],
                    'properties': {'position': 2, 'title': '<b>2D</b> Viewers'}
                }},
            10: {'widget':
                 {'applets': [{'name': u'VtkViewer'}],
                  'properties': {'position': 2, 'title': '<b>3D</b> Viewer'}}},
            11: {'widget':
                 {'applets': [
                     {'name': u'EditorManager'}],
                  'properties': {'position': 0}}},
            12: {'widget':
                 {'applets': [
                     {'name': u'ShellWidget'},
                     {'name': u'HistoryWidget'},
                     {'name': u'HelpWidget'},
                     {'name': u'Logger'}],
                  'properties': {'position': 2}
                  }}
        }}

    def __call__(self, mainwin=None):
        if mainwin is None:
            return self.__class__

        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
