
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


def add_shelf(path):
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

