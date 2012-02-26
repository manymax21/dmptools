#============================================
#
# presets.py
# michael.havart@gmail.com
# class used to manage dmptools presets. 
#
#============================================

import os
import subprocess

class PresetsManager(object):
    """
    manage the dmptools presets.
    you can only set one preset at a time.
    usage:
    presets = PresetsManager()
    newpresets = presets.addPreset(key='', value=None)

    to remove a preset:
    presets = PresetsManager()
    newpresets = presets.removePreset(key='')

    """
    def __init__(self):
        """
        if the preset file doesn't exists create it.
        """
        # detect the current soft context (Maya or Nuke)
        # if nothing found then raise an error.
        try:
            import nuke
            PRESET_FILE = '!NUKE_PRESET_FILE!'
        except ImportError:
            try:
                import maya
                PRESET_FILE = '!MAYA_PRESET_FILE!'
            except ImportError:
                raise UserWarning('no Maya or Nuke module found')

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
