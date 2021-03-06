# shelf buttons list
BUTTONS = [
    {
        'name' : 'HotkeysList',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.showHotkeysList()',
        'icon' : 'textureEditorOpenBar.png',
        'annotation' : 'Show the hotkeys list window'
    },
    {
        'name' : 'Separator0',
        'command' : 'print "| soft >"',
        'icon' : 'textureEditorOpenBar.png',
        'annotation' : '| soft >'
    },
    {
        'name' : 'Terminator',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchConsole()',
        'icon' : 'Console.xpm',
        'annotation' : 'Launch the Console2 terminal.'
    },
    {
        'name' : 'SublimeText',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchSublimeText()',
        'icon' : 'SublimeText.xpm',
        'annotation' : 'Launch the Sublime Text editor.'
    },
    {
        'name' : 'Nuke',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.launchNuke()',
        'icon' : 'Nuke.xpm',
        'annotation' : 'Launch Nuke.'
    },
    {
        'name' : 'Separator1',
        'command' : 'print "< soft | tools >"',
        'icon' : 'textureEditorOpenBar.png',
        'annotation' : '< soft | tools >'
    },
    {
        'name' : 'newScriptEditor',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            reload(mayaCommands);mayaCommands.newScriptEditor()',
        'icon' : 'text.png',
        'annotation' : 'New Script Editor.'
    },
    {
        'name' : 'mayaToNuke',
        'command' : 'import dmptools.mayaToNuke.launcher as mayaToNukeLauncher;\
            mayaToNukeLauncher.main()',
        'icon' : 'MayaToNuke.xpm',
        'annotation' : 'Maya to Nuke Exporter.'
    },
    {
        'name' : 'ratioCalculator',
        'command' : 'import dmptools.ratioCalculator as ratioCalculator;\
            ratioCalculator.main()',
        'icon' : 'RatioCalculator.xpm',
        'annotation' : 'Camera-Image ratio calculator.'
    },
  ]
