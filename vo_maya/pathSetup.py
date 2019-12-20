
"""
    pathSetup
    set up paths for plugins, icons, shelves, etc
"""

import os
import maya.mel as mel
import maya.cmds as cmds

VO_DIR = os.path.normpath(os.path.dirname(__file__)).replace('\\', '/')##....  gets this script's filepath
VO_ICON_PATH = os.path.normpath(os.path.join(VO_DIR, 'icons')).replace('\\', '/')
#PLUGIN_DIR = os.path.normpath(os.path.join(VO_DIR, 'plug-ins')).replace('\\', '/')
VO_SHELF_PATH = os.path.normpath(os.path.join(VO_DIR, 'shelves')).replace('\\', '/')

#shelf_contents = os.listdir(VO_SHELF_PATH)

def return_paths(param = ''):
    if param == 'VO_DIR':
        return VO_DIR
    elif param == 'VO_ICON_PATH':
        return VO_ICON_PATH
    elif param == 'VO_SHELF_PATH':
        return VO_SHELF_PATH
    else:
        return VO_DIR, VO_ICON_PATH, VO_SHELF_PATH

def test_func(thingy):
    print('tasted')
    print(thingy)


def path_check(path,environPath):
    """
    function to check for path validity and log info for error handling
    """
    return



############        ================================        ############
###                                                                  ###
#   ...........bunch of stuff ripped from red9's setup.py...........   #
###                                                                  ###
############        ================================        ############


def add_path(path, pathName):
    print('adding %s path') % (pathName)

    iconsPath = os.environ.get(pathName)

    if os.path.exists(path) and path not in iconsPath:
        os.environ[pathName] += '%s%s' % (os.pathsep, path)
    else:
        return False

def addIconsPath(path):
    print('adding icon path')
    #if not path:
    #    path = os.path.join(vo_maya.VO_DIR, 'icons')
    iconsPath = os.environ.get('XBMLANGPATH')

    if os.path.exists(path) and path not in iconsPath:
        #log.info('Adding vo-icons To XBM Paths : %s' % path)
        os.environ['XBMLANGPATH'] += '%s%s' % (os.pathsep, path)
    else:
        return
        #log.info('Red9 Icons Path already setup')

#TODO:   figure out whether this is useful at all.
#        Since importing shelf copies it to shelves folder
def addShelfPath(path):
    print('adding shelf path')
    #if not path:
    #    path = os.path.join(vo_maya.VO_DIR, 'icons')
    shelfPath = os.environ.get('MAYA_SHELF_PATH')

    if os.path.exists(path) and path not in shelfPath:
        #log.info('Adding vo-icons To XBM Paths : %s' % path)
        os.environ['MAYA_SHELF_PATH'] += '%s%s' % (os.pathsep, path)
    else:
        return False
        #log.info('Red9 Icons Path already setup')

def load_shelf(path):
    #path = vo_maya.VO_SHELF_PATH
    print('loading shelves')
    #print(shelf_path)
    # get current top shelf
    
    gShelfTopLevel = mel.eval("string $shelf_ly=$gShelfTopLevel")
    top = cmds.shelfTabLayout(gShelfTopLevel, q=True, st=True)

    if os.path.exists(path):
        print(path)
        #delete_shelf(path)
        mel.eval('source "%s"' % path)
        mel.eval('loadNewShelf("%s")' % path)##....       BINGO!! loads a new shelf!
        #log.info('Shelf loaded: % s' % path)
        return True
    else:
        return False
        #log.error('Cant load shelf, file doesnt exist: %s' % path)

    # restore users top shelf
    cmds.shelfTabLayout(gShelfTopLevel, e=True, st=top)



def delete_shelf(shelf_name):
    '''
    Delete maya shelf and update maya shelf optionVars
    :param shelf_name: string: name of the shelf to be deleted
    :return:
    '''
    if cmds.about(batch=True):
        return
    if not cmds.shelfLayout(shelf_name, q=True, ex=True):
        return

    # Shelf preferences....

    #https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/CommandsPython/
    cmds.deleteUI(shelf_name, layout=True)
    #mel.eval("shelfTabChange")


def launch_sequence():
    print('launching . . .')
    shelf_contents = os.listdir(VO_SHELF_PATH)
    #import pathSetup as ps  #....       import instance of pathSetup
    #utils.executeDeferred("ps.test_func(VO_DIR)")
    addIconsPath(VO_ICON_PATH)
    #ps.addShelfPath(VO_SHELF_PATH)
    """
    for shelf in shelf_contents:
        shelf_name = 'vo_' + shelf.split('_')[2].replace('.mel','')
        ps.delete_shelf(shelf_name)
        shelf_path = os.path.normpath(os.path.join(VO_SHELF_PATH,shelf)).replace('\\', '/')
        #print(shelf_path)
        ps.load_shelf(shelf_path)
    """
    #TODO:  update user prefs to save shelf changes

    """
    try:
        ps.addIconsPath(VO_ICON_PATH)  #....     run setup script with value from this module
    except:
        raise print('error adding voracious maya icon path')
    try:
        ps.load_shelf(VO_SHELF_PATH)
    except:
        raise print('error loading voracious shelves')
    """

