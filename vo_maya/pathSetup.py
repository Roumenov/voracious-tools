
"""
    pathSetup
    set up paths for plugins, icons, shelves, etc
"""

print('begin path setup')
import maya.mel as mel
import os
import maya.cmds as cmds


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
        return False
        #log.info('Red9 Icons Path already setup')

#TODO:   figure out whether this is useful at all.
#        Since importing shelf copies it to shelves folder
def addShelfPath(path):
    print('adding icon path')
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
    #if mayaIsBatch():
    #    return
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
        #pref_file = os.path.join(mayaPrefs(), 'prefs', 'shelves', 'shelf_%s.mel.deleted' % shelf_name)
        if os.path.exists(pref_file):
            os.remove(pref_file)
        mel.eval("shelfTabChange")
        #log.info('Shelf deleted: % s' % shelf_name)
    except StandardError, err:
        #log.warning('shelf management failed : %s' % err)
