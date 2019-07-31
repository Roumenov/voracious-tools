
"""
    function wrappers for shelf buttons
    typically this means a version that feeds the selection into the arguments
    largely this is to simplify shelf editing for artists and allow them to 
    more easily batch operations with saved selections.

    TODO: add procs for building shelves, not sure how to copy shelves while maya is running, though
"""



import pymel.core as pm
#import vo_usefulFunctions as uf
#reload(uf)




def meta_tag_wrapper():
    for target in pm.ls(sl=1):
        vo_meta.meta_tag(target)


