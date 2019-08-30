import os
import maya.utils as utils
import maya.cmds as cmds
#import pathSetup as ps

VO_DIR = os.path.normpath(os.path.dirname(__file__))##....  gets this script's filepath
VO_ICON_PATH = os.path.normpath(os.path.join(VO_DIR, 'icons')).replace('\\', '/')
#PLUGIN_DIR = os.path.normpath(os.path.join(VO_DIR, 'plug-ins')).replace('\\', '/')
VO_SHELF_PATH = os.path.normpath(os.path.join(VO_DIR, 'shelves')).replace('\\', '/')

shelf_contents = os.listdir(VO_SHELF_PATH)

print('pathoing!')
print(VO_SHELF_PATH)
print(shelf_contents)

def launch_sequence():
    print('launching . . .')
    import pathSetup as ps  #....       import instance of pathSetup
    #utils.executeDeferred("ps.test_func(VO_DIR)")
    ps.addIconsPath(VO_ICON_PATH)
    for shelf in shelf_contents:
        shelf_path = os.path.normpath(os.path.join(VO_SHELF_PATH,shelf)).replace('\\', '/')
        print(shelf_path)
        ps.add_shelf(shelf_path)
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


utils.executeDeferred(launch_sequence())

#launch_sequence()


