import os
import maya.utils as utils
import maya.cmds as cmds
#import pathSetup as ps

VO_DIR = os.path.normpath(os.path.dirname(__file__)).replace('\\', '/')##....  gets this script's filepath
VO_ICON_PATH = os.path.normpath(os.path.join(VO_DIR, 'icons')).replace('\\', '/')
#PLUGIN_DIR = os.path.normpath(os.path.join(VO_DIR, 'plug-ins')).replace('\\', '/')
VO_SHELF_PATH = os.path.normpath(os.path.join(VO_DIR, 'shelves')).replace('\\', '/')

#shelf_contents = os.listdir(VO_SHELF_PATH)


def _reload():
    return


def return_paths(param = ''):
    if param == 'VO_DIR':
        return VO_DIR
    elif param == 'VO_ICON_PATH':
        return VO_ICON_PATH
    elif param == 'VO_SHELF_PATH':
        return VO_SHELF_PATH
    else:
        return VO_DIR, VO_ICON_PATH, VO_SHELF_PATH

#print(return_paths(param = ''))

def launch_sequence():
    print('launching . . .')
    shelf_contents = os.listdir(VO_SHELF_PATH)
    import pathSetup as ps  #....       import instance of pathSetup
    #utils.executeDeferred("ps.test_func(VO_DIR)")
    ps.addIconsPath(VO_ICON_PATH)
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
#utils.executeDeferred("vo_maya.ps.addIconsPath(%s)" % (VO_ICON_PATH))
#utils.executeDeferred("vo_maya.ps.load_shelf(%s)" % (VO_SHELF_PATH))
#cmds.evalDeferred("vo_maya.ps.load_shelf(%s)" % (VO_ICON_PATH))

#ps.test_func(VO_DIR)

#cmds.evalDeferred("launch_sequence()")
#utils.executeDeferred("import pathSetup;pathSetup.test_func()")


####utils.executeDeferred(launch_sequence())

#launch_sequence()


