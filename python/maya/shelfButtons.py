# shelf buttons list
BUTTONS = [
    {
        'name' : 'Separator0',
        'command' : 'print "| soft >"',
        'icon' : 'textureEditorOpenBar.png',
        'annotation' : '| soft >'
    },
    {
        'name' : 'Terminator',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            mayaCommands.launchConsole()',
        'icon' : 'Console.xpm',
        'annotation' : 'Launch the Console2 terminal.'
    },
    {
        'name' : 'SublimeText',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            mayaCommands.launchSublimeText()',
        'icon' : 'SublimeText.xpm',
        'annotation' : 'Launch the Sublime Text editor.'
    },
    {
        'name' : 'Nuke',
        'command' : 'import dmptools.mayaCommands as mayaCommands;\
            mayaCommands.launchNuke()',
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
            mayaCommands.newScriptEditor()',
        'icon' : 'text.png',
        'annotation' : 'New Script Editor.'
    },
    {
        'name' : 'mayaToNuke',
        'command' : 'import dmptools.mayaToNuke.launcher as mtnlauncher;\
            mtnlauncher.main()',
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
