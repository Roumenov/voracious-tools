
"""
    vo-maya
    set up paths for plugins, icons, etc
    
"""
import maya.mel as mel
import os


#example of how dilloTools sets up its paths in the init

#DILLO_DIR = os.path.normpath(os.path.dirname(__file__))
#IMAGES_DIR = os.path.normpath(os.path.join(DILLO_DIR, 'images'))
#SCRIPTS_DIR = os.path.normpath(os.path.join(DILLO_DIR, 'scripts')).replace('\\', '/')
#PLUGIN_DIR = os.path.normpath(os.path.join(DILLO_DIR, 'plugins')).replace('\\', '/')

import os

VO_DIR = os.path.normpath(os.path.dirname(__file__))##....  gets this script's filepath
ICONS_DIR = os.path.normpath(os.path.join(VO_DIR, 'icons'))
PLUGIN_DIR = os.path.normpath(os.path.join(VO_DIR, 'plug-ins')).replace('\\', '/')
PLUGIN_DIR = os.path.normpath(os.path.join(VO_DIR, 'shelves')).replace('\\', '/')


                    ############        ================================        ############
                    ###                                                                  ###
                    #   ...........bunch of stuff ripped from red9's setup.py...........   #
                    ###                                                                  ###
                    ############        ================================        ############


def addScriptsPath(path):
    '''
    Add additional folders to the ScriptPath
    '''
    scriptsPath = os.environ.get('MAYA_SCRIPT_PATH')

    if os.path.exists(path):
        if path not in scriptsPath:
            log.info('Adding To Script Paths : %s' % path)
            os.environ['MAYA_SCRIPT_PATH'] += '%s%s' % (os.pathsep, path)
        else:
            log.info('Red9 Script Path already setup : %s' % path)
    else:
        log.debug('Given Script Path is invalid : %s' % path)

def addPluginPath(path=None):
    '''
    Make sure the plugin path has been added. If run as a module
    this will have already been added
    '''
    if not path:
        path = os.path.join(red9ModulePath(), 'plug-ins')
    plugPaths = os.environ.get('MAYA_PLUG_IN_PATH')
    if os.path.exists(path) and path not in plugPaths:
        log.info('Adding Red9 Plug-ins to Plugin Paths : %s' % path)
        os.environ['MAYA_PLUG_IN_PATH'] += '%s%s' % (os.pathsep, path)
    else:
        log.info('Red9 Plug-in Path already setup')

def addIconsPath(path=None):
    '''
    Make sure the icons path has been added. If run as a module
    this will have already been added
    '''
    if not path:
        path = os.path.join(red9ModulePath(), 'icons')
    iconsPath = os.environ.get('XBMLANGPATH')

    if os.path.exists(path) and path not in iconsPath:
        log.info('Adding Red9 Icons To XBM Paths : %s' % path)
        os.environ['XBMLANGPATH'] += '%s%s' % (os.pathsep, path)
    else:
        log.info('Red9 Icons Path already setup')

def delete_shelf(shelf_name):
    '''
    Delete maya shelf and update maya shelf optionVars
    :param shelf_name: string: name of the shelf to be deleted
    :return:
    '''
    if mayaIsBatch():
        return
    if not cmds.shelfLayout(shelf_name, q=True, ex=True):
        return

    shelfs = cmds.optionVar(q='numShelves')
    current_shelf = None

    # Shelf preferences.
    for i in range(shelfs + 1):
        if shelf_name == cmds.optionVar(q="shelfName%i" % i):
            current_shelf = i
            break

    try:
        if current_shelf:
            # manage shelve ids
            for i in range(current_shelf, shelfs + 1):
                cmds.optionVar(iv=("shelfLoad%s" % str(i), cmds.optionVar(q="shelfLoad%s" % str(i + 1))))
                cmds.optionVar(sv=("shelfName%s" % str(i), cmds.optionVar(q="shelfName%s" % str(i + 1))))
                cmds.optionVar(sv=("shelfFile%s" % str(i), cmds.optionVar(q="shelfFile%s" % str(i + 1))))

        cmds.optionVar(remove="shelfLoad%s" % shelfs)
        cmds.optionVar(remove="shelfName%s" % shelfs)
        cmds.optionVar(remove="shelfFile%s" % shelfs)
        cmds.optionVar(iv=("numShelves", shelfs - 1))

        cmds.deleteUI(shelf_name, layout=True)
        pref_file = os.path.join(mayaPrefs(), 'prefs', 'shelves', 'shelf_%s.mel.deleted' % shelf_name)
        if os.path.exists(pref_file):
            os.remove(pref_file)
        mel.eval("shelfTabChange")
        log.info('Shelf deleted: % s' % shelf_name)
    except StandardError, err:
        log.warning('shelf management failed : %s' % err)

def load_shelf(shelf_path):
    '''
    load Maya shelf
    :param shelf_path: string: file path to maya shelf
    '''
    if mayaIsBatch():
        return

    # get current top shelf
    gShelfTopLevel = mel.eval("string $shelf_ly=$gShelfTopLevel")
    top = cmds.shelfTabLayout(gShelfTopLevel, q=True, st=True)

    if os.path.exists(shelf_path):
        # print shelf_path
        delete_shelf(shelf_path)
        mel.eval('source "%s"' % shelf_path)
        mel.eval('loadNewShelf("%s")' % shelf_path)##....       BINGO!! loads a new shelf!
        log.info('Shelf loaded: % s' % shelf_path)
        return True
    else:
        log.error('Cant load shelf, file doesnt exist: %s' % shelf_path)

    # restore users top shelf
    cmds.shelfTabLayout(gShelfTopLevel, e=True, st=top)