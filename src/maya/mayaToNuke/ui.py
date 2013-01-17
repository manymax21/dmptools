import maya.cmds as cmds
import os

import dmptools.mayaToNuke.exporter as exporter

from dmptools.mayaToNuke.utils import Utils
from dmptools.presets import PresetsManager

WINDOW_NAME = 'mtn_Window'
PRESETS = PresetsManager()
UTILS = Utils()

class MayaToNukeUI(object):
    def __init__(self):
        """ get all the necessary values """
        # get stuff from presets
        textFieldValue = PRESETS.getPreset('mtn_textField')
        if not textFieldValue:
            self.textFieldValue = UTILS.tempPath()
        else:
            self.textFieldValue = textFieldValue[0]
        # stuff
        self.items = {}
        # get selection
        self.originalSel = cmds.ls(sl=True)
        # framerange info
        self.framerange = UTILS.getFramerange()
        # user info
        self.user = UTILS.user
        self.platform = UTILS.platform
        self.computer = UTILS.computer
        self.headerText = self.generateHeader()

    def buildUI(self):
        """ build the interface UI """
        # destroy the mayaToNuke windows if exists
        if cmds.window(WINDOW_NAME, exists=True):
            cmds.deleteUI(WINDOW_NAME, window=True)
        # create the main window
        self.win = cmds.window(WINDOW_NAME,
                        title="Maya To Nuke Interface",
                        mb=True,
                        w=650, h=300)
        # build menu bar
        self.menuBar()
        # create the main master form
        mainform = cmds.formLayout("mtn_mainForm")
        # create the header of the interface
        self.header = cmds.text('mtn_textHeader', label=self.headerText)
        # create the text field where to put the nuke output script
        txtOutput = cmds.text('mtn_textOutput', label="nuke script:")
        # textField
        self.textField = cmds.textField('mtn_fileField',
                        text=self.textFieldValue,
                        annotation='This is the output file')
                        
        cmds.textField(self.textField,
                        e=True,
                        changeCommand=self.saveSettings,
                        #enterCommand=self.saveSettings
                        )
        # open filedialog button
        outputButton = cmds.button('mtn_outputButton',
                        label = " ... ",
                        c=self.selectOutputFile,
                        annotation='Browse for a Nuke file - please type the .nk extension')
        # separators
        separator1 = cmds.separator()
        separatorTop = cmds.separator()
        separatorBottom = cmds.separator()
        # export, close and refresh buttons
        exportButton = cmds.button('mtn_exportButton',
                        label="Export",
                        c=self.export,
                        annotation='Generate Nuke script from selected items')
        closeButton = cmds.button('mtn_closeButton',
                        label="Close",
                        c=self.closeUI,
                        annotation='Close the mayaToNuke interface - Have a nice day -')
        reloadButton = cmds.iconTextButton('mtn_reloadButton',
                        label="Refresh",
                        st='iconOnly',
                        i='refresh.png',
                        c=self.refreshUI,
                        annotation='Refresh the UI with the current selection')
        # build options panel (create left and right panes)
        paneForm = self.doublePane()
        # attachForm
        cmds.formLayout(mainform,
                        edit = True,
                        attachForm = 
                        [
                            (reloadButton, "top", 5),
                            (reloadButton, "right", 5),
                            (self.header, "left", 5),
                            (self.header, "top", 5),
                            (txtOutput, "left", 5),
                            (outputButton, "right", 5),
                            (exportButton, "bottom", 5),
                            (exportButton, "left", 5),
                            (closeButton, "bottom", 5),
                            (closeButton, "right", 5),
                            (separator1, "left", 5),
                            (separator1, "right", 5),
                            (separatorTop, "left", 5),
                            (separatorTop, "right", 5),
                            (separatorBottom, "left", 5),
                            (separatorBottom, "right", 5),
                            (paneForm, "left", 5),
                            (paneForm, "right", 5)
                        ]
                    )
        # attachControl
        cmds.formLayout(mainform,
                        edit=True,
                        attachControl = 
                        [
                            (separator1, "top", 5, reloadButton),
                            (txtOutput, "top", 5, separator1),
                            (txtOutput, "top", 5, separator1),
                            (self.textField, "left", 5, txtOutput),
                            (self.textField, "right", 5, outputButton),
                            (outputButton, "top", 4, separator1),
                            (self.textField, "top", 5, separator1),
                            (separatorTop, "top", 5, self.textField),
                            (separatorBottom, "bottom", 5, exportButton),
                            (paneForm, "top", 4, separatorTop),
                            (paneForm, "bottom", 5, separatorBottom)
                        ])
        # attachPosition
        cmds.formLayout(mainform, edit=True,
                        attachPosition = 
                        [
                            (exportButton, "right", 5, 50),
                            (closeButton, "left", 5, 50)
                        ]
                    )
        cmds.showWindow(WINDOW_NAME)
        
    def doublePane(self):
        """build the double pane layout for the selection display"""
        # create the main form
        form = cmds.formLayout("mtn_optionsForm")
        # build bottom helpLine
        helpline = self.helpLine()
        cmds.setParent('..')
        # main frame layout
        frameL = cmds.frameLayout('mtn_doublePaneMainFrameLayout',
                                label = 'Items ready for export:',
                                cll = False,
                                cl = False,
                                bv = True)
        # create double paneLayout and its default separation value
        paneLayout = cmds.paneLayout('mtn_doublePane',
                                    configuration='vertical2',
                                    paneSize=[[1,0,100],[2,100,100]])
        # build the left panelayout
        leftPanel = self.leftPane()
        # build the right panelayout
        rightPanel = self.rightPane()
        # set the panes on their good position
        cmds.paneLayout('mtn_doublePane', edit=True, setPane = [ leftPanel, 1])
        cmds.paneLayout('mtn_doublePane', edit=True, setPane = [ rightPanel, 2])
        # attatch the forms
        cmds.formLayout(form,
                        edit = True,
                        attachForm = 
                            [
                                (frameL, "left", 5),
                                (frameL, "right", 5),
                                (frameL, "top", 5),
                                (helpline, "left", 5),
                                (helpline, "right", 5),
                                (helpline, "bottom", 2)
                            ]
                        )
        cmds.formLayout(form,
                        edit = True,
                        attachControl = 
                            [
                                (frameL, "bottom", 5, helpline)
                            ]
                        )
        return form
    
    def leftPane(self):
        """obsolete pane but maybe useful"""
        # pass scroll layout on the left side of the pane layout
        passesL = cmds.formLayout('mtn_leftPaneForm')
        colLayout = cmds.columnLayout(adj = True)
        cmds.setParent('..')
        # fill with stuff
        passes = ['infos']
        passList = cmds.textScrollList(append = passes, sii = True, ams = True)
        cmds.setParent('..')
        # attach form
        cmds.formLayout(passesL, edit = True,   attachForm = [
                                            (passList, "left", 5),
                                            (passList, "right", 5),
                                            (passList, "top", 15),
                                            (passList, "bottom", 5)
                                            ])
        return passesL

    def rightPane(self):
        """main layout where the selection is displayed"""
        # framelayoutTitle
        form = cmds.formLayout('mtn_rightPaneForm')
        selFrameL = cmds.scrollLayout('mtn_scrollRightPanel', hst = True, cr = True)
        colLayout = cmds.columnLayout('mtn_columnRightPanel', adj = True)
        # get items lists
        self.items = UTILS.filterSelection()
        # create objects framelayout
        self.objectsfrmLayout = cmds.frameLayout('mtn_objectsFrameLayout',
                            label = str(len(self.items['meshes']))+' objects:',
                            cll = True,
                            cl = True if not self.items['meshes'] else False,
                            bv = False,
                            annotation = 'Valid objects to export')
        self.objectsTxt = self.editableFrameLayout(self.items['meshes'])
        cmds.setParent('..')
        # create cameras framelayout
        self.camerasfrmLayout = cmds.frameLayout('mtn_camerasFrameLayout',
                            label = str(len(self.items['cameras']))+' cameras:',
                            cll = True,
                            cl = True if not self.items['cameras'] else False,
                            bv = False,
                            annotation = 'Valid cameras to export')
        self.camerasTxt = self.editableFrameLayout(self.items['cameras'])
        cmds.setParent('..')
        # create locators framelayout
        self.locatorsfrmLayout = cmds.frameLayout('mtn_locatorsFrameLayout',
                            label = str(len(self.items['locators']))+' locators:',
                            cll = True,
                            cl = True if not self.items['locators'] else False,
                            bv = False,
                            annotation = 'Valid locators to export')
        self.locatorsTxt = self.editableFrameLayout(self.items['locators'])
        cmds.setParent('..')
        # create lights framelayout        
        self.lightsfrmLayout = cmds.frameLayout('mtn_lightsFrameLayout',
                            label = str(len(self.items['lights']))+' lights:',
                            cll = True,
                            cl = True if not self.items['lights'] else False,
                            bv = False,
                            annotation = 'Valid lights to export')
        self.lightsTxt = self.editableFrameLayout(self.items['lights'])
        cmds.setParent('..')
        
        cmds.formLayout(form, edit = True, attachForm = [
                                            (selFrameL, "top", 15),
                                            (selFrameL, "left", 5),
                                            (selFrameL, "right", 5),
                                            (selFrameL, "bottom", 5)
                                            ])
        return form
    
    def editableFrameLayout(self, items):
        """name of the object"""
        form = cmds.formLayout('mtn_itemForm')
        txt = cmds.text('mtn_itemText', al = "left", label = UTILS.strFromList(items)[1])
        cmds.setParent('..')
        return txt

    def helpLine(self):
        """bottom interactive helpline"""
        # form that contains the framelayout
        form = cmds.formLayout('mtn_helplineForm')
        # framelayout that contains the helpline
        frame = cmds.frameLayout('mtn_helplineFrameLayout',
                            borderVisible = False,
                            labelVisible = False,
                            h = 20)
        # create helpline
        cmds.helpLine('mtn_helpline', h = 10)
        cmds.setParent('..')
        # attach the stuff
        cmds.formLayout(form, edit = True, attachForm = [
                                            (frame, 'left', 0),
                                            (frame, 'right', 0),
                                            (frame, 'top', 0),
                                            (frame, 'bottom', 0)
                                            ])
        return form

    def menuBar(self):
        """create the top menubar"""
        cmds.menu('mtn_menuBar', label='File', allowOptionBoxes = False )
        # add items
        # refresh button
        updateC = self.refreshUI
        cmds.menuItem(label='Refresh', c=updateC) 
        # settings button
        settingsC = self.settingsUI
        cmds.menuItem(label='Settings', c=settingsC) 
        # exit button
        print 'import maya.cmds as cmds;cmds.deleteUI("'+WINDOW_NAME+'", window = True)'
        exitC = 'import maya.cmds as cmds;cmds.deleteUI("'+WINDOW_NAME+'", window = True)'
        cmds.menuItem(label = 'Exit', c = exitC)
        # add help menu
        cmds.menu(label = 'Help', helpMenu = True)
        helpC = 'import webbrowser;webbrowser.open("http://github.com/michael-ha/dmptools/blob/master/README")'
        cmds.menuItem(label = 'Intranet Help', c = helpC)
        
        fun1C = 'import webbrowser;webbrowser.open("http://www.google.com/images?q=mecha &")'
        cmds.menuItem(label = 'Bonus: Mechas !!', c = fun1C)
        
        fun2C = 'import webbrowser;webbrowser.open("http://www.google.com/images?q=kittens &")'
        cmds.menuItem(label = 'Bonus: Kittens !!', c = fun2C)
        
        aboutC = 'import maya.cmds as cmds;cmds.confirmDialog(title = "about", message = "version v1.0", button = "OK")'
        cmds.menuItem(label = 'About', c = aboutC)

    def selectOutputFile(self, none=None):
        """opens a file dialog to point to the output path"""
        textfieldValue = cmds.textField(self.textField, text=True, q=True)
        if textfieldValue:
            directoryMask = os.path.dirname(textfieldValue+"/*.nk")
        else:
            directoryMask = "/*.nk"
            
        filedialog = cmds.fileDialog2(cap='Where to save the nuke script?',
                                    fm=0,
                                    ff='*.nk',
                                    dir=directoryMask,
                                    )
        if filedialog:
            outputpath = filedialog[0]
            cmds.textField(self.textField, e=True, text=outputpath)

    def textfieldValidator(self, inputText=''):
        """check if the input has an nk extension"""
        if inputText:
            outputFile = str(inputText)
            try:
                ext = outputFile.split('.')[-1]
            except:
                ext = ''
                pass
            if ext == 'nk':
                return outputFile
            else:
                return None
        else:
            print 'nothing found'
            return None

    def refreshUI(self, none=None):
        """method to refresh the interface from a new selection"""
        # get the new selection
        self.originalSel = cmds.ls(sl=True)
        self.items = UTILS.filterSelection()
        # refresh objects ui
        cmds.text(self.objectsTxt, e=True, label = UTILS.strFromList(self.items['meshes'])[1])
        cmds.frameLayout(self.objectsfrmLayout,
                            e=True,
                            label = str(len(self.items['meshes']))+' objects:',
                            cll = True,
                            cl = True if not self.items['meshes'] else False,
                            bv = False,
                            annotation = 'Valid objects to export')
        # refresh cameras ui
        cmds.text(self.camerasTxt, e=True, label = UTILS.strFromList(self.items['cameras'])[1])
        cmds.frameLayout(self.camerasfrmLayout,
                            e=True,
                            label = str(len(self.items['cameras']))+' cameras:',
                            cll = True,
                            cl = True if not self.items['cameras'] else False,
                            bv = False,
                            annotation = 'Valid cameras to export')
        # refresh locators ui
        cmds.text(self.locatorsTxt, e=True, label = UTILS.strFromList(self.items['locators'])[1])
        cmds.frameLayout(self.locatorsfrmLayout,
                            e=True,
                            label = str(len(self.items['locators']))+' locators:',
                            cll = True,
                            cl = True if not self.items['locators'] else False,
                            bv = False,
                            annotation = 'Valid locators to export')
        # refresh lights ui
        cmds.text(self.lightsTxt, e=True, label = UTILS.strFromList(self.items['lights'])[1])
        cmds.frameLayout(self.lightsfrmLayout,
                            e=True,
                            label = str(len(self.items['lights']))+' lights:',
                            cll = True,
                            cl = True if not self.items['lights'] else False,
                            bv = False,
                            annotation = 'Valid lights to export')
        # refresh header
        self.framerange = UTILS.getFramerange()
        headerText = self.generateHeader()
        cmds.text(self.header, label=headerText, e=True)

    def closeUI(self, none=None):
        """delete the main window"""
        # get settings before closing
        self.saveSettings()
        # close ui
        cmds.deleteUI(WINDOW_NAME, window = True)

    def export(self, selection):
        """start the export procedure"""
        # save settings
        self.saveSettings()
        if self.items:
            # get display values
            UTILS.getDisplayItems()
            #set display off
            UTILS.setDisplayOff()
            # get the output path from the textfield
            outputFile = self.textfieldValidator(cmds.textField(self.textField, text=True, q=True))
            if outputFile:
                # generate the nuke script
                EXPORTER = exporter.Exporter(self.items, outputFile, self.framerange)
                EXPORTER.startExport()
            else:
                cmds.confirmDialog(t = 'Error', m = 'The output file is not correct.\nex: /<path>/nukefile.nk')
            #set display back on
            UTILS.setDisplayOn()
            # set playback at the original frame
            cmds.currentTime(self.framerange['current'])
            #select original selection
            if self.originalSel:
                cmds.select(self.originalSel, r = True)
            
        else:
            cmds.confirmDialog(t = 'Error', m = 'There is nothing to export!')

    def saveSettings(self, none=None):
        # get settings values
        textField = cmds.textField(self.textField, text=True, q=True)
        # set presets
        PRESETS.addPreset('mtn_textField', textField)

    def settingsUI(self, non=None):
        """UI of mayaToNuke settings """
        settings = PRESETS.getStrPresets()
        # create ui
        if cmds.window('mtn_settings', exists=True):
            cmds.deleteUI('mtn_settings', window=True)
        settingsWindow = cmds.window('mtn_settings',
                            t='MayaToNuke settings window',
                            w=100,
                            h=50)
        cmds.formLayout()
        text = cmds.text(label=str(settings), align='left')
        cmds.showWindow(settingsWindow)

    def generateHeader(self):
        headerText = \
                'infos: '+self.platform+' | '+self.user+'@'+self.computer.lower()+\
                ' | frame range: ['\
                +str(self.framerange['first'])+' - '\
                +str(self.framerange['last'])+']'
        return headerText
