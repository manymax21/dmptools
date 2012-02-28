# hotkeys list
HOTKEYS = \
[
    {
        'name':'bufMove',
        'key':'q',
        'alt':False,
        'ctl':False,
        'release':True,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMove()");',
        'releaseCommand':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.bufMoveRelease()");'
    },
    {
        'name':'hideSelectionSwitch',
        'key':'h',
        'alt':False,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.hideSelSwitch()");'
    },
    {
        'name':'isolateSelection',
        'key':'h',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.isolateSelection()");',
    },
    {
        'name':'toggleNormals',
        'key':'n',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.toggleNormals()");',
    },
    {
        'name':'setWireframe',
        'key':'w',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setWireframe()");',
    },
    {
        'name':'setBackfaceCulling',
        'key':'B',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setBackfaceCulling()");',},
    {
        'name':'setDefaultMaterial',
        'key':'d',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultMaterial()");',
    },
    {
        'name':'cameraPanTool',
        'key':'z',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraPanTool()");',
    },
    {
        'name':'cameraZoomTool',
        'key':'Z',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.cameraZoomTool()");',
    },
    {
        'name':'resetPanZoom',
        'key':'Z',
        'alt':True,
        'ctl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.resetPanZoom()");',
    },
    {
        'name':'selectNgones',
        'key':'q',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectNgones()");',
    },
    {
        'name':'selectTriangles',
        'key':'p',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchSelectTriangles()");',
    },
    {
        'name':'switchLight',
        'key':'l',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchLight()");'
    },
    {
        'name':'switchHighlightedSelection',
        'key':'f',
        'alt':True,
        'ctl':False,'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.switchHighlightedSelection()");'
    },
    {
        'name':'askFlushUndo',
        'key':'f',
        'alt':False,
        'ctl':True,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.askFlushUndo()");'
    },
    {
        'name':'saveAs',
        'key':'S',
        'alt':False,
        'ctl':True,
        'release':False,
        'command':'SaveSceneAs;'
    },
    {
        'name':'freezeHistory',
        'key':'F',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'delete -ch;makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;'
    },
    {
        'name':'freezeHistoryCenterPivot',
        'key':'F',
        'alt':True,
        'ctl':True,
        'release':False,
        'command':'delete -ch;xform -cp;makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;'
    },
    {
        'name':'setDefaultRenderer',
        'key':'1',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setDefaultRenderer()");'
    },
    {
        'name':'setHardwareRenderer',
        'key':'2',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setHardwareRenderer()");'
    },
    {
        'name':'setViewport2Renderer',
        'key':'3',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.setViewport2Renderer()");'
    },
    {
        'name':'launchConsole',
        'key':'x',
        'alt':True,
        'ctl':False,
        'release':False,
        'command':'python("import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole()");'
    },
]
# end of hotkeys