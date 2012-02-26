#================================================
#
# michael.havart@gmail.com
# make.py
#
# Nuke & Maya dmpTools Windows local make file
# This will install Nuke and Maya source code
# in the user respective folders.
#
#================================================

import os
import sys
import fileinput
import shutil
from shutil import *

# test if we are on Windows
if not os.name == 'nt' and not len(sys.argv) == 4:
    raise UserWarning('This install only works on windows!')

# globals
MODULE_NAME = 'dmptools'
VERSION = '1.0.0'
PROJECT_NAME = sys.argv[-1] == 'dmptools.sublime-project'
ACTIVE_FILE_PATH = sys.argv[-2]
ACTIVE_FILE = os.path.basename(ACTIVE_FILE_PATH)
MAKE = ACTIVE_FILE.split('.')[0] == 'Make'
MODULE_PATH = sys.argv[-3]
PYTHON_SOURCE_PATH = MODULE_PATH+'/python/'
# ACTIVE_FILE_IN_PROJECT set to False by default
ACTIVE_FILE_IN_PROJECT = False
# check if the active file is in the project path
for root, dirs, files in os.walk(MODULE_PATH):
    for f in files:
        if ACTIVE_FILE in f and 'workspace' in ACTIVE_FILE_PATH:
            ACTIVE_FILE_IN_PROJECT = True
            break
USER = os.environ['USERNAME']
EXCLUDE_DIRS = ['.git',
                'csh',
                'mel',
                'documentation',
                'gizmos',
                ]
EXCLUDE_FILES = ['pyc']
# nuke globals
NUKE_PATH = 'c:/users/'+USER+'/.nuke/'
NUKE_PRESET_FILE = NUKE_PATH+MODULE_NAME+'/dmptools.presets'
# maya globals
MAYA_GLOBAL = 'c:/users/'+USER+'/documents/maya/'
MAYA_PATH = MAYA_GLOBAL+'/scripts/'
MAYA_PRESET_FILE = MAYA_PATH+MODULE_NAME+'/dmptools.presets'
MAYA_USERSETUP_FILE = '// file automatically generated by Make.py'
MAYA_USERSETUP_FILE += '// userSetup.mel\n'
MAYA_USERSETUP_FILE += '//\n\n'
MAYA_USERSETUP_FILE += '// create dmptools shelf\n'
MAYA_USERSETUP_FILE += 'python ("import dmptools.dmptoolsShelf as dmpShelf;dmpShelf.main()");\n'
MAYA_USERSETUP_FILE += '// createHotkeys\n'
MAYA_USERSETUP_FILE += 'python ("import dmptools.createHotkeys as createHotkeys;createHotkeys.main()");\n'

# string replacements
REPLACEMENTS = {
                '!VERSION!' : VERSION,
                '!NUKE_SHARE!' : NUKE_PATH+MODULE_NAME+'/pictures',
                '!NUKE_PRESET_FILE!' : NUKE_PRESET_FILE,
                '!MAYA_GLOBAL!' : MAYA_GLOBAL,
                '!MAYA_PATH!' : MAYA_PATH+MODULE_NAME,
                '!MAYA_PICTURES!' : MAYA_PATH+MODULE_NAME+'/pictures',
                '!MAYA_SHELF!' : MAYA_PATH+MODULE_NAME+'/pictures/shelf',
                '!MAYA_PRESET_FILE!' : MAYA_PRESET_FILE,
                }

def installNuke():
    # install maya process
    print '=============================='
    print '           N U K E            '
    print '=============================='
    print 'installing nuke '+MODULE_NAME+' in '+NUKE_PATH+MODULE_NAME+' ...'    

    # delete old dmpTools
    if os.path.exists(NUKE_PATH+MODULE_NAME):
        print ' > deleting old dmpTools ...'
        shutil.rmtree(NUKE_PATH+MODULE_NAME)
    # install nuke tools
    install(PYTHON_SOURCE_PATH+'/nuke', NUKE_PATH+MODULE_NAME)
    # copy preset file in the maya source path
    if os.path.exists(PYTHON_SOURCE_PATH+'/nuke/macros/presets.py'):
        if os.path.exists(PYTHON_SOURCE_PATH+'/maya/presets.py'):
            os.remove(PYTHON_SOURCE_PATH+'/maya/presets.py')
        shutil.copy2(PYTHON_SOURCE_PATH+'/nuke/macros/presets.py', PYTHON_SOURCE_PATH+'/maya')
    # replacements
    print ' > doing replacements...'
    replacements(NUKE_PATH+MODULE_NAME)

    print ' > done.'

def installMaya():
    # install maya process
    print '=============================='
    print '           M A Y A            '
    print '=============================='
    print 'installing maya '+MODULE_NAME+' in '+MAYA_PATH+MODULE_NAME+' ...'    

    # delete old dmpTools
    if os.path.exists(MAYA_PATH+MODULE_NAME):
        print ' > deleting old dmpTools ...'
        shutil.rmtree(MAYA_PATH+MODULE_NAME)
    # install maya tools (python & mel)
    install(PYTHON_SOURCE_PATH+'/maya', MAYA_PATH+MODULE_NAME)
    # remove preset file from the maya source path
    if os.path.exists(PYTHON_SOURCE_PATH+'/maya/presets.py'):
        os.remove(PYTHON_SOURCE_PATH+'/maya/presets.py')
    # replacements
    print ' > doing replacements...'
    replacements(MAYA_PATH+MODULE_NAME)
    # create userSetup to load the shelf
    createUserSetup()

    print ' > done.'

def replacements(path):
    # check the files in the install path
    for root, dirs, files in os.walk(path):
        for f in files:
            # go through python & mel files only
            if f.split('.')[-1] in ['py', 'mel']:
                for line in fileinput.input(root+'/'+f, inplace=1):
                    # if the key in REPLACEMENTS is in the file then replace the line
                    for rep in REPLACEMENTS.keys():
                        if rep in line:
                            line = line.replace(rep, REPLACEMENTS[rep])
                    # write the replaced line in the file
                    sys.stdout.write(line)

def createUserSetup():
    '''
        create the userSetup file for Maya startup
    '''
    userSetup = MAYA_PATH+'/userSetup.mel'
    if os.path.exists(userSetup):
        os.remove(userSetup)
    # create the userSetup file
    print ' > creating '+MAYA_PATH+'/userSetup.mel'
    FILE = open(userSetup, 'w')
    FILE.write(MAYA_USERSETUP_FILE)
    FILE.close()

def install(src, dst, symlinks=False, ignore=None):
    '''
        slightly different shutil.copytree
    '''
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                if os.path.split(srcname)[-1] not in EXCLUDE_DIRS:
                    print ' > installing directory', srcname, 'to', dstname
                    install(srcname, dstname, symlinks, ignore)
            else:
                if os.path.split(srcname)[-1].split('.')[-1] not in EXCLUDE_FILES:
                    print ' > installing file', srcname, 'to', dstname
                    copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError, why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)

def errorMsg(message):
    from ctypes import c_int, WINFUNCTYPE, windll
    from ctypes.wintypes import HWND, LPCSTR, UINT
    prototype = WINFUNCTYPE(c_int, HWND, LPCSTR, LPCSTR, UINT)
    paramflags = (1, "hwnd", 0), (1, "text", message), (1, "caption", None), (1, "flags", 0)
    MessageBox = prototype(("MessageBoxA", windll.user32), paramflags)
    MessageBox(text=message)

def install_dmptools():
    # install Nuke dmptools
    installNuke()
    # install Maya dmptools
    installMaya()

def main():
    # if the project name is 'dmptools'
    # and the active file is in the project path
    # then run the install
    if PROJECT_NAME and ACTIVE_FILE_IN_PROJECT:
        print 'excuting python.exe',' '.join(sys.argv)
        install_dmptools()
    else:
        # yield a windows error message
        errorMsg('You need to install from here:\n\
            '+MODULE_PATH+'\n\
            You run from:\n\
            '+ACTIVE_FILE_PATH+'')

if __name__ == '__main__':
    main()
