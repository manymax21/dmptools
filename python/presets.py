#============================================
#
# presets.py
# michael.havart@gmail.com
# class used to manage various presets. 
#
#============================================

import os
import subprocess

class PresetsManager(object):
    """
    manage the dmptools presets.
    you can only set one preset at a time.
    usage:
    >>> presets = PresetsManager()
    >>> newpresets = presets.addPreset(key='', value=None)

    to remove a preset:
    >>> presets = PresetsManager()
    >>> newpresets = presets.removePreset(key='')

    to get a preset value (returns a list):
    >>> presets = PresetsManager()
    >>> preset = presets.getPreset(key='')

    to get a print version of all the presets (keys and values):
    >>> presets = PresetManager()
    >>> print presets.getStrPresets()
    """
    
    def __init__(self):
        """
        if the preset file doesn't exists create it.
        """
        # create the presets file in appdata/dmptools
        appdata = os.getenv('APPDATA')
        if not os.path.exists(appdata):
            appdata = os.getenv('USERPROFILE')+'/Documents'
        dmptoolspath = appdata+'/dmptools'
        if not os.path.exists(dmptoolspath):
            os.mkdir(dmptoolspath)
        PRESET_FILE = dmptoolspath+'/dmptools.presets'

        # create the preset file if it doesnt exists
        self.presetfile = PRESET_FILE
        if not os.path.exists(self.presetfile):
            # creating preset file
            print '> creating preset file'
            with open(self.presetfile, 'w') as FILE:
                FILE.write('')

    def addPreset(self, key='', value=None):
        """
        the preset key need to be a string and the value can be anything.
        if the key already exists in the preset file,
        then remove the old one and append a new one.
        returns a list of all the presets in the file.
        """
        dic = {key:value}
        # checking if the preset already exists
        presetList = self.getPresets()
        newPresetList = []
        if presetList:
            for preset in presetList:
                if not dic.keys() == preset.keys():
                    newPresetList.append(preset)
        newPresetList.append(dic)

        # remove the preset file to re-create the new one
        os.remove(self.presetfile)
        with open(self.presetfile, 'w') as FILE:
            for preset in newPresetList:
                FILE.write(str(preset)+'\n')

        return self.getPresets()

    def removePreset(self, key=''):
        """
        remove a preset from the preset file.
        returns a list of all the presets in the file.
        """
        presetList = self.getPresets()
        newPresetList = []
        if presetList:
            for preset in presetList:
                if not key in preset.keys():
                    newPresetList.append(preset)

        # remove the preset file to re-create the new one
        os.remove(self.presetfile)
        with open(self.presetfile, 'w') as FILE:
            for preset in newPresetList:
                FILE.write(str(preset)+'\n')

        return self.getPresets()

    def getPreset(self, key=''):
        """
        return the preset matching the key.
        """
        values = None
        with open(self.presetfile, 'r') as FILE:
            for line in FILE.readlines():
                try:
                    dic = eval(line)
                    if key in dic.keys():
                        values = dic.values()
                        break
                except:
                    pass

        return values

    def getPresets(self):
        """
        returns a list of dict from the preset file.
        """
        dictList = []
        with open(self.presetfile, 'r') as FILE:
            for line in FILE.readlines():
                try:
                    dictList.append(eval(line))
                except:
                    pass

        return dictList
        
    def openPresetFile(self):
        """
        open the preset file with notepad
        """
        if os.path.exists(self.presetfile):
            subprocess.Popen('notepad '+self.presetfile)
        else:
            raise UserWarning('preset file not found!')

    def getStrPresets(self):
        """ 
        convert presets dicts to str
        """
        global presetsStr
        presets = PresetsManager()
        presetsL = presets.getPresets()
        # recursive method
        def setStr(preset):
            global presetsStr
            for key in preset.keys():
                presetsStr += "-"+str(key)+":\n"
                for value in preset.values():
                    if type(value).__name__ == 'dict':
                        presetsStr += "\t"
                        setStr(value)
                    else:
                        presetsStr += "\t"+str(value)+"\n"
                        
        presetsStr = "Presets:\n"
        # go through all the presets
        for preset in presetsL:
            setStr(preset)
        
        return presetsStr


