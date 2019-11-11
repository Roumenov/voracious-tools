'''

jsConnectAttrs

'''

import maya.cmds as mc
import sys as sys
import ast as ast

def jsCA_driverTrans():
    
    getDriverTrans = mc.ls (sl = True)
    length = len (getDriverTrans)
    
    if length == 0:
        mc.textField (jsCA_getDriverTrans_TF, e = True, text = 'object, object, object...')
        mc.warning ('Selection cannot be zero')
    
    else:    
        getDriverTransStr = str(getDriverTrans)
        getDriverTransStr = getDriverTransStr.replace ("u'", "")
        getDriverTransStr = getDriverTransStr.replace ("[", "")
        getDriverTransStr = getDriverTransStr.replace ("]", "")
        getDriverTransStr = getDriverTransStr.replace ("'", "")
        getDriverTransStr = getDriverTransStr.replace ("[", "")
        mc.textField (jsCA_getDriverTrans_TF, e = True, text = getDriverTransStr)
        
        sys.stdout.write ('Enabled zig-zag connect mode. Make sure number of driver and driven objects are the same.')

def jsCA_drivenTrans():
        
    getDrivenTrans = mc.ls (sl = True)
    length = len (getDrivenTrans)
    
    if length == 0:
        mc.textField (jsCA_getDrivenTrans_TF, e = True, text = 'object, object, object...')
        mc.warning ('Selection cannot be zero')
    
    else:
        getDrivenTransStr = str(getDrivenTrans)
        getDrivenTransStr = getDrivenTransStr.replace ("u'", "")
        getDrivenTransStr = getDrivenTransStr.replace ("[", "")
        getDrivenTransStr = getDrivenTransStr.replace ("]", "")
        getDrivenTransStr = getDrivenTransStr.replace ("'", "")
        getDrivenTransStr = getDrivenTransStr.replace ("[", "")
        mc.textField (jsCA_getDrivenTrans_TF, e = True, text = getDrivenTransStr)    
        
def jsCA_driverAttrs():
    
    getDriverAttrs = mc.channelBox ('mainChannelBox', q=True, sma=True)
    if getDriverAttrs is None:
        length = None
    else:
        length = len (getDriverAttrs)
    
    if length == 0 or length is None:
        mc.textField (jsCA_getDriverAttrs_TF, e = True, text = 'attr')
        mc.warning ('Selection must be 1')
    
    elif length > 1:
        mc.warning ('Selection must be 1')
    
    else:
        
        getDriverAttrsStr = str (getDriverAttrs)
        getDriverAttrsStr = getDriverAttrsStr.replace ("u'", "")
        getDriverAttrsStr = getDriverAttrsStr.replace ("[", "")
        getDriverAttrsStr = getDriverAttrsStr.replace ("]", "")
        getDriverAttrsStr = getDriverAttrsStr.replace ("'", "")
        getDriverAttrsStr = getDriverAttrsStr.replace ("[", "")
        mc.textField (jsCA_getDriverAttrs_TF, e = True, text = getDriverAttrsStr)
        
def jsCA_drivenAttrs():
    
    getDrivenAttrs = mc.channelBox ('mainChannelBox', q=True, sma=True)
    if getDrivenAttrs is None:
        length = None
    else:
        length = len (getDrivenAttrs)
    
    if length == 0 or length == None:
        mc.textField (jsCA_getDrivenAttrs_TF, e = True, text = 'attr, attr, attr...')
        mc.warning ('Selection cannot be zero')
    
    else:
        
        getDrivenAttrsStr = str (getDrivenAttrs)
        getDrivenAttrsStr = getDrivenAttrsStr.replace ("u'", "")
        getDrivenAttrsStr = getDrivenAttrsStr.replace ("[", "")
        getDrivenAttrsStr = getDrivenAttrsStr.replace ("]", "")
        getDrivenAttrsStr = getDrivenAttrsStr.replace ("'", "")
        getDrivenAttrsStr = getDrivenAttrsStr.replace ("[", "")
        mc.textField (jsCA_getDrivenAttrs_TF, e = True, text = getDrivenAttrsStr)

def jsCA_pickQDriver():
    
    getQDriverObj = mc.ls (sl = True)
    getQDriverAttrs = mc.channelBox ('mainChannelBox', q=True, sma=True)
    if getQDriverAttrs is None:
        length = None
    else:
        length = len (getQDriverAttrs)
        getQDriverObj = getQDriverObj[0]
    
    
    
    if length == 0 or length is None:
        mc.textField (jsCA_getQDriver_TF, e = True, text = 'object.attr')
        mc.warning ('Selection must be 1')
    
    else:
        
        getQDriverAttrsStr = str (getQDriverAttrs)
        getQDriverAttrsStr = getQDriverAttrsStr.replace ("u'", "")
        getQDriverAttrsStr = getQDriverAttrsStr.replace ("[", "")
        getQDriverAttrsStr = getQDriverAttrsStr.replace ("]", "")
        getQDriverAttrsStr = getQDriverAttrsStr.replace ("'", "")
        getQDriverAttrsStr = getQDriverAttrsStr.replace ("[", "")
        getQDriverAttrsStr = '%s.%s' %(getQDriverObj, getQDriverAttrsStr)
        mc.textField (jsCA_getQDriver_TF, e = True, text = getQDriverAttrsStr)

def jsCA_pickQDriven():
    
    getQDrivenObj = mc.ls (sl = True)
    getQDrivenAttrs = mc.channelBox ('mainChannelBox', q=True, sma=True)
    if getQDrivenAttrs is None:
        length = None
    else:
        length = len (getQDrivenAttrs)
        getQDrivenObj = getQDrivenObj[0]
    
    if length == 0 or length is None:
        mc.textField (jsCA_getQDriven_TF, e = True, text = 'object.attr, attr, attr...')
        mc.warning ('Selection must be 1')
    
    else:
        
        getQDrivenAttrsStr = str (getQDrivenAttrs)
        getQDrivenAttrsStr = getQDrivenAttrsStr.replace ("u'", "")
        getQDrivenAttrsStr = getQDrivenAttrsStr.replace ("[", "")
        getQDrivenAttrsStr = getQDrivenAttrsStr.replace ("]", "")
        getQDrivenAttrsStr = getQDrivenAttrsStr.replace ("'", "")
        getQDrivenAttrsStr = getQDrivenAttrsStr.replace ("[", "")
        getQDrivenAttrsStr = '%s.%s' %(getQDrivenObj, getQDrivenAttrsStr)
        mc.textField (jsCA_getQDriven_TF, e = True, text = getQDrivenAttrsStr)

def jsCA_QC():
    
    jsCA_QDriver_TF_q = mc.textField (jsCA_getQDriver_TF, q = True, tx = True)
    jsCA_QDriven_TF_q = mc.textField (jsCA_getQDriven_TF, q = True, tx = True)
    
    if 'object.' in jsCA_QDriver_TF_q or 'object.' in jsCA_QDriven_TF_q:
        
        mc.warning ('Please fill both fields.')
        pass
    
    else:
    
        jsCA_strList = str(jsCA_QDriven_TF_q)
        split_excludeFirst = jsCA_strList.split ('.')
        excludeFirst = jsCA_strList.replace (split_excludeFirst[0], '')
        excludeFirst = excludeFirst.replace ('.', '')
        
        jsCA_qAttrs = "['%s']" %excludeFirst
        jsCA_qAttrs = jsCA_qAttrs.replace (", ", "', '")
        jsCA_qAttrs = ast.literal_eval(jsCA_qAttrs)
        
        for attr in jsCA_qAttrs:
            
            mc.connectAttr (jsCA_QDriver_TF_q, '%s.%s' %(split_excludeFirst[0], attr))
    
def jsCA_execute():
    
    getDriverTrans = mc.textField (jsCA_getDriverTrans_TF, q = True, text = True)
    getDriverTrans = "['%s']" %getDriverTrans
    getDriverTrans = getDriverTrans.replace (", ", "', '")
    getDriverTrans = ast.literal_eval(getDriverTrans)
    
    getDrivenTrans = mc.textField (jsCA_getDrivenTrans_TF, q = True, text = True)
    getDrivenTrans = "['%s']" %getDrivenTrans
    getDrivenTrans = getDrivenTrans.replace (", ", "', '")
    getDrivenTrans = ast.literal_eval(getDrivenTrans)
    
    getDriverAttrs = mc.textField (jsCA_getDriverAttrs_TF, q = True, text = True)
    getDriverAttrs = "['%s']" %getDriverAttrs
    getDriverAttrs = getDriverAttrs.replace (", ", "', '")
    getDriverAttrs = ast.literal_eval(getDriverAttrs)
    
    getDrivenAttrs = mc.textField (jsCA_getDrivenAttrs_TF, q = True, text = True)
    getDrivenAttrs = "['%s']" %getDrivenAttrs
    getDrivenAttrs = getDrivenAttrs.replace (", ", "', '")
    getDrivenAttrs = ast.literal_eval(getDrivenAttrs)
    
    len_driverTrans = len(getDriverTrans)
    len_drivenTrans = len(getDrivenTrans)
    len_driverAttrs = len(getDriverAttrs)
    len_drivenAttrs = len(getDrivenAttrs)
    
    if 'object, object, object...' in getDriverTrans or 'object, object, object...' in getDrivenTrans or 'attr' in getDriverAttrs or 'attr, attr, attr...' in getDrivenAttrs:
        
        mc.warning ('Please fill all fields.')
        pass
    
    else:
        
        if len_driverTrans == 1 and len_drivenTrans == 1:
            
            for attr in getDrivenAttrs:
                lock = mc.getAttr ('%s.%s' %(getDrivenTrans[0], attr), l = True)
                if lock == False:
                    mc.connectAttr ('%s.%s' %(getDriverTrans[0], getDriverAttrs[0]), '%s.%s' %(getDrivenTrans[0], attr))
        
        elif len_driverTrans > 1 and len_driverTrans == len_drivenTrans:
            
            count = 0
            
            for obj in getDrivenTrans:
                               
                for attr in getDrivenAttrs:
                    
                    if count <= len_driverTrans - 1:
                        
                        lock = mc.getAttr ('%s.%s' %(obj, attr), l = True)
                        if lock == False:
                            print count
                            mc.connectAttr ('%s.%s' %(getDriverTrans[count], getDriverAttrs[0]), '%s.%s' %(obj, attr))
                            
                count = count + 1
                            
                        #if count == len_driverTrans - 1:
                            
        elif len_driverTrans > 1 and len_drivenTrans < len_driverTrans:
            
            mc.warning ('Driver count must be either 1 or match driven count')
        
        elif len_driverTrans == 1 and len_drivenTrans > 1:
            
            for obj in getDrivenTrans:
                               
                for attr in getDrivenAttrs:
                    
                    lock = mc.getAttr ('%s.%s' %(obj, attr), l = True)
                    if lock == False:
                        mc.connectAttr ('%s.%s' %(getDriverTrans[0], getDriverAttrs[0]), '%s.%s' %(obj, attr))
            
            
            
def jsCA_t():
                            
    getDriverTrans = mc.textField (jsCA_getDriverTrans_TF, q = True, text = True)
    getDriverTrans = "['%s']" %getDriverTrans
    getDriverTrans = getDriverTrans.replace (", ", "', '")
    getDriverTrans = ast.literal_eval(getDriverTrans)
    print getDriverTrans[0]
    
    getDrivenTrans = mc.textField (jsCA_getDrivenTrans_TF, q = True, text = True)
    getDrivenTrans = "['%s']" %getDrivenTrans
    getDrivenTrans = getDrivenTrans.replace (", ", "', '")
    getDrivenTrans = ast.literal_eval(getDrivenTrans)
    print getDrivenTrans[0]
    
    getDriverAttrs = mc.textField (jsCA_getDriverAttrs_TF, q = True, text = True)
    getDriverAttrs = "['%s']" %getDriverAttrs
    getDriverAttrs = getDriverAttrs.replace (", ", "', '")
    getDriverAttrs = ast.literal_eval(getDriverAttrs)
    print getDriverAttrs[0]
    
    getDrivenAttrs = mc.textField (jsCA_getDrivenAttrs_TF, q = True, text = True)
    getDrivenAttrs = "['%s']" %getDrivenAttrs
    getDrivenAttrs = getDrivenAttrs.replace (", ", "', '")
    getDrivenAttrs = ast.literal_eval(getDrivenAttrs)
    print getDrivenAttrs[0]
    
    len_driverTrans = len(getDriverTrans)
    len_drivenTrans = len(getDrivenTrans)
    len_driverAttrs = len(getDriverAttrs)
    len_drivenAttrs = len(getDrivenAttrs)
    
    if 'object' != getDriverTrans[0] and 'object' != getDrivenTrans or getDriverTrans is None or getDrivenTrans is None:
    
        if len_driverTrans == 1:
                
            for obj in getDrivenTrans:
                lock = mc.getAttr ('%s.tx' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.tx' %getDriverTrans[0], '%s.tx' %obj)
                lock = mc.getAttr ('%s.ty' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.ty' %getDriverTrans[0], '%s.ty' %obj)
                lock = mc.getAttr ('%s.tz' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.tz' %getDriverTrans[0], '%s.tz' %obj)
        
        elif len_driverTrans > 1 and len_driverTrans == len_drivenTrans:
            
            count = 0
            
            for obj in getDrivenTrans:
                
                if count <= len_driverTrans - 1:
                    lock = mc.getAttr ('%s.tx' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.tx' %getDriverTrans[count], '%s.tx' %obj)
                    lock = mc.getAttr ('%s.ty' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.ty' %getDriverTrans[count], '%s.ty' %obj)
                    lock = mc.getAttr ('%s.tz' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.tz' %getDriverTrans[count], '%s.tz' %obj)
                    
                    count = count + 1
                            
        elif len_driverTrans > 1 and len_driverTrans != len_drivenTrans:
            
            mc.warning ('Driver count must be either 1 or match driven count')
    else:
        mc.warning ('Please fill driver and driven object fields.')

def jsCA_r():
                            
    getDriverTrans = mc.textField (jsCA_getDriverTrans_TF, q = True, text = True)
    getDriverTrans = "['%s']" %getDriverTrans
    getDriverTrans = getDriverTrans.replace (", ", "', '")
    getDriverTrans = ast.literal_eval(getDriverTrans)
    print getDriverTrans[0]
    
    getDrivenTrans = mc.textField (jsCA_getDrivenTrans_TF, q = True, text = True)
    getDrivenTrans = "['%s']" %getDrivenTrans
    getDrivenTrans = getDrivenTrans.replace (", ", "', '")
    getDrivenTrans = ast.literal_eval(getDrivenTrans)
    print getDrivenTrans[0]
    
    getDriverAttrs = mc.textField (jsCA_getDriverAttrs_TF, q = True, text = True)
    getDriverAttrs = "['%s']" %getDriverAttrs
    getDriverAttrs = getDriverAttrs.replace (", ", "', '")
    getDriverAttrs = ast.literal_eval(getDriverAttrs)
    print getDriverAttrs[0]
    
    getDrivenAttrs = mc.textField (jsCA_getDrivenAttrs_TF, q = True, text = True)
    getDrivenAttrs = "['%s']" %getDrivenAttrs
    getDrivenAttrs = getDrivenAttrs.replace (", ", "', '")
    getDrivenAttrs = ast.literal_eval(getDrivenAttrs)
    print getDrivenAttrs[0]
    
    len_driverTrans = len(getDriverTrans)
    len_drivenTrans = len(getDrivenTrans)
    len_driverAttrs = len(getDriverAttrs)
    len_drivenAttrs = len(getDrivenAttrs)
    
    if 'object' != getDriverTrans[0] and 'object' != getDrivenTrans or getDriverTrans is None or getDrivenTrans is None:
    
        if len_driverTrans == 1:
                
            for obj in getDrivenTrans:
                lock = mc.getAttr ('%s.rx' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.rx' %getDriverTrans[0], '%s.rx' %obj)
                lock = mc.getAttr ('%s.ry' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.ry' %getDriverTrans[0], '%s.ry' %obj)
                lock = mc.getAttr ('%s.rz' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.rz' %getDriverTrans[0], '%s.rz' %obj)
        
        elif len_driverTrans > 1 and len_driverTrans == len_drivenTrans:
            
            count = 0
            
            for obj in getDrivenTrans:
                
                if count <= len_driverTrans - 1:
                    lock = mc.getAttr ('%s.rx' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.rx' %getDriverTrans[count], '%s.rx' %obj)
                    lock = mc.getAttr ('%s.ry' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.ry' %getDriverTrans[count], '%s.ry' %obj)
                    lock = mc.getAttr ('%s.rz' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.rz' %getDriverTrans[count], '%s.rz' %obj)
                    
                    count = count + 1
                            
        elif len_driverTrans > 1 and len_driverTrans != len_drivenTrans:
            
            mc.warning ('Driver count must be either 1 or match driven count')
            
    else:
        mc.warning ('Please fill driver and driven object fields.')

def jsCA_s():
                            
    getDriverTrans = mc.textField (jsCA_getDriverTrans_TF, q = True, text = True)
    getDriverTrans = "['%s']" %getDriverTrans
    getDriverTrans = getDriverTrans.replace (", ", "', '")
    getDriverTrans = ast.literal_eval(getDriverTrans)
    print getDriverTrans[0]
    
    getDrivenTrans = mc.textField (jsCA_getDrivenTrans_TF, q = True, text = True)
    getDrivenTrans = "['%s']" %getDrivenTrans
    getDrivenTrans = getDrivenTrans.replace (", ", "', '")
    getDrivenTrans = ast.literal_eval(getDrivenTrans)
    print getDrivenTrans[0]
    
    getDriverAttrs = mc.textField (jsCA_getDriverAttrs_TF, q = True, text = True)
    getDriverAttrs = "['%s']" %getDriverAttrs
    getDriverAttrs = getDriverAttrs.replace (", ", "', '")
    getDriverAttrs = ast.literal_eval(getDriverAttrs)
    print getDriverAttrs[0]
    
    getDrivenAttrs = mc.textField (jsCA_getDrivenAttrs_TF, q = True, text = True)
    getDrivenAttrs = "['%s']" %getDrivenAttrs
    getDrivenAttrs = getDrivenAttrs.replace (", ", "', '")
    getDrivenAttrs = ast.literal_eval(getDrivenAttrs)
    print getDrivenAttrs[0]
    
    len_driverTrans = len(getDriverTrans)
    len_drivenTrans = len(getDrivenTrans)
    len_driverAttrs = len(getDriverAttrs)
    len_drivenAttrs = len(getDrivenAttrs)
    
    if 'object' != getDriverTrans[0] and 'object' != getDrivenTrans or getDriverTrans is None or getDrivenTrans is None:
        
        if len_driverTrans == 1:
                
            for obj in getDrivenTrans:
                lock = mc.getAttr ('%s.sx' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.sx' %getDriverTrans[0], '%s.sx' %obj)
                lock = mc.getAttr ('%s.sy' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.sy' %getDriverTrans[0], '%s.sy' %obj)
                lock = mc.getAttr ('%s.sz' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.sz' %getDriverTrans[0], '%s.sz' %obj)
        
        elif len_driverTrans > 1 and len_driverTrans == len_drivenTrans:
            
            count = 0
            
            for obj in getDrivenTrans:
                
                if count <= len_driverTrans - 1:
                    lock = mc.getAttr ('%s.sx' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.sx' %getDriverTrans[count], '%s.sx' %obj)
                    lock = mc.getAttr ('%s.sy' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.sy' %getDriverTrans[count], '%s.sy' %obj)
                    lock = mc.getAttr ('%s.sz' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.sz' %getDriverTrans[count], '%s.sz' %obj)
                    
                    count = count + 1
                            
        elif len_driverTrans > 1 and len_driverTrans != len_drivenTrans:
            
            mc.warning ('Driver count must be either 1 or match driven count')
            
    else:
        mc.warning ('Please fill driver and driven object fields.')
        
def jsCA_all():
                            
    getDriverTrans = mc.textField (jsCA_getDriverTrans_TF, q = True, text = True)
    getDriverTrans = "['%s']" %getDriverTrans
    getDriverTrans = getDriverTrans.replace (", ", "', '")
    getDriverTrans = ast.literal_eval(getDriverTrans)
    print getDriverTrans[0]
    
    getDrivenTrans = mc.textField (jsCA_getDrivenTrans_TF, q = True, text = True)
    getDrivenTrans = "['%s']" %getDrivenTrans
    getDrivenTrans = getDrivenTrans.replace (", ", "', '")
    getDrivenTrans = ast.literal_eval(getDrivenTrans)
    print getDrivenTrans[0]
    
    getDriverAttrs = mc.textField (jsCA_getDriverAttrs_TF, q = True, text = True)
    getDriverAttrs = "['%s']" %getDriverAttrs
    getDriverAttrs = getDriverAttrs.replace (", ", "', '")
    getDriverAttrs = ast.literal_eval(getDriverAttrs)
    print getDriverAttrs[0]
    
    getDrivenAttrs = mc.textField (jsCA_getDrivenAttrs_TF, q = True, text = True)
    getDrivenAttrs = "['%s']" %getDrivenAttrs
    getDrivenAttrs = getDrivenAttrs.replace (", ", "', '")
    getDrivenAttrs = ast.literal_eval(getDrivenAttrs)
    print getDrivenAttrs[0]
    
    len_driverTrans = len(getDriverTrans)
    len_drivenTrans = len(getDrivenTrans)
    len_driverAttrs = len(getDriverAttrs)
    len_drivenAttrs = len(getDrivenAttrs)
    
    if 'object' != getDriverTrans[0] and 'object' != getDrivenTrans or getDriverTrans is None or getDrivenTrans is None:
        
        if len_driverTrans == 1:
                
            for obj in getDrivenTrans:
                
                cbCheck = mc.channelBox ('mainChannelBox', q = True, sma = True)
                if cbCheck:
                    attrs = cbCheck
                else:
                    attrs = mc.listAttr (obj, v = 1, k = 1, l = 0)
                
                for attr in attrs:
                    lock = mc.getAttr ('%s.%s' %(obj,attr), l = True)
                    if lock == False:
                        match = mc.objExists ('%s.%s' %(getDriverTrans[0],attr))
                        print match
                        if match:
                            mc.connectAttr ('%s.%s' %(getDriverTrans[0],attr), '%s.%s' %(obj,attr))
                '''
                lock = mc.getAttr ('%s.sx' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.sx' %getDriverTrans[0], '%s.sx' %obj)
                lock = mc.getAttr ('%s.sy' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.sy' %getDriverTrans[0], '%s.sy' %obj)
                lock = mc.getAttr ('%s.sz' %obj, l = True)
                if lock == False:
                    mc.connectAttr ('%s.sz' %getDriverTrans[0], '%s.sz' %obj)
                '''
        
        elif len_driverTrans > 1 and len_driverTrans == len_drivenTrans:
            
            count = 0
            
            for obj in getDrivenTrans:
                
                cbCheck = mc.channelBox ('mainChannelBox', q = True, sma = True)
                if cbCheck:
                    attrs = cbCheck
                else:
                    attrs = mc.listAttr (obj, v = 1, k = 1, l = 0)
                for attr in attrs:
                    lock = mc.getAttr ('%s.%s' %(obj,attr), l = True)
                    if lock == False:
                        match = mc.objExists ('%s.%s' %(getDriverTrans[0],attr))
                        print match
                        if match:
                            mc.connectAttr ('%s.%s' %(getDriverTrans[0],attr), '%s.%s' %(obj,attr))
                '''
                if count <= len_driverTrans - 1:
                    lock = mc.getAttr ('%s.sx' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.sx' %getDriverTrans[count], '%s.sx' %obj)
                    lock = mc.getAttr ('%s.sy' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.sy' %getDriverTrans[count], '%s.sy' %obj)
                    lock = mc.getAttr ('%s.sz' %obj, l = True)
                    if lock == False:
                        mc.connectAttr ('%s.sz' %getDriverTrans[count], '%s.sz' %obj)
                    
                    count = count + 1
                '''
                            
        elif len_driverTrans > 1 and len_driverTrans != len_drivenTrans:
            
            mc.warning ('Driver count must be either 1 or match driven count')
            
    else:
        mc.warning ('Please fill driver and driven object fields.')

def jsCA_driverTransSel():
    
    getDriverTrans = mc.textField (jsCA_getDriverTrans_TF, q = True, text = True)
    if 'object,' not in getDriverTrans:
        toSel2 = getDriverTrans.replace (", ", "', '")
        toSel3 = "'%s'" %toSel2
        eval ("mc.select (%s)" %toSel3)
    else:
        mc.warning ('Nothing to select.')
    
def jsCA_drivenTransSel():
    
    getDrivenTrans = mc.textField (jsCA_getDrivenTrans_TF, q = True, text = True)
    if 'object,' not in getDrivenTrans:
        toSel2 = getDrivenTrans.replace (", ", "', '")
        toSel3 = "'%s'" %toSel2
        eval ("mc.select (%s)" %toSel3)
    else:
        mc.warning ('Nothing to select.')
    
def jsCA_qDriverTransSel():
    
    jsCA_QDriver_TF_q = mc.textField (jsCA_getQDriver_TF, q = True, tx = True)
    if 'object.' not in jsCA_QDriver_TF_q:
        spl = jsCA_QDriver_TF_q.split ('.')
        mc.select (spl[0])
    else:
        mc.warning ('Nothing to select.')
    
def jsCA_qDrivenTransSel():
    
    jsCA_QDriven_TF_q = mc.textField (jsCA_getQDriven_TF, q = True, tx = True)
    if 'object.' not in jsCA_QDriven_TF_q:
        spl = jsCA_QDriven_TF_q.split ('.')
        mc.select (spl[0])
    else:
        mc.warning ('Nothing to select.')

# Create UI

jsCA_winHide = 'jsCA_createWin'
jsCA_winTitleHide = 'Connect Attributes'
mc.windowPref (jsCA_winHide, width = 200, height = 200)

if (mc.window (jsCA_winHide, exists = True)):
    mc.deleteUI (jsCA_winHide)

mc.window (jsCA_winHide, rtf = True, width = 200, height = 200, title = jsCA_winTitleHide, s = True)
mc.columnLayout (adj = True, rs = 2)

mc.text (' ')
mc.text ('Normal/Batch Connect', al = 'center', fn = 'boldLabelFont')
mc.text (' ')

mc.rowColumnLayout (rowSpacing = (2,1), nc = 4)

jsCA_getDriverTrans_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'object, object, object...')
mc.button (l = 'Load Driver Object(s)', c = lambda x:jsCA_driverTrans(), w = 132, bgc = (.619,.784,.902))
mc.text (' ')
mc.button (l = 'Select', c = lambda x:jsCA_driverTransSel(), w = 50, bgc = (.937,.867,.570))

jsCA_getDriverAttrs_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'attr')
mc.button (l = 'Load Driver Attribute', c = lambda x:jsCA_driverAttrs(), bgc = (.619,.784,.902))
mc.text (' ')
mc.text ('   -   ')

jsCA_getDrivenTrans_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'object, object, object...')
mc.button (l = 'Load Driven Object(s)', c = lambda x:jsCA_drivenTrans(), bgc = (.661,.620,.902))
mc.text (' ')
mc.button (l = 'Select', c = lambda x:jsCA_drivenTransSel(), w = 50, bgc = (.937,.867,.570))

jsCA_getDrivenAttrs_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'attr, attr, attr...')
mc.button (l = 'Load Driven Attribute(s)', c = lambda x:jsCA_drivenAttrs(), bgc = (.661,.620,.902))
mc.text (' ')
mc.text ('   -   ')

mc.setParent ('..')

mc.button (l = 'Connect Loaded Attrs', c = lambda x:jsCA_execute(), bgc = (.635,.882,.605))
mc.rowColumnLayout (rowSpacing = (2,1), nc = 9)
mc.button (l = ' Translate ', c = lambda x:jsCA_t(), bgc = (.635,.882,.605))
mc.text (' ')
mc.button (l = ' Rotate ', c = lambda x:jsCA_r(), bgc = (.635,.882,.605))
mc.text (' ')
mc.button (l = ' Scale ', c = lambda x:jsCA_s(), bgc = (.635,.882,.605))
mc.text (' ')
mc.button (l = ' Trans/Rot/Scl ', c = lambda x:(jsCA_t(), jsCA_r(), jsCA_s()), w = 105, bgc = (.635,.882,.605))
mc.text (' ')
mc.button (l = ' Channel Box ', c = lambda x:(jsCA_all()), w = 115, bgc = (.635,.882,.605))
mc.setParent ('..')

mc.text (' ')
mc.text ('Quick Connect', al = 'center', fn = 'boldLabelFont')
mc.text (' ')
mc.rowColumnLayout (rowSpacing = (2,1), nc = 4)
jsCA_getQDriver_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'object.attr')
mc.button (w = 132, l = 'Load Driver + Attr', c = lambda x:jsCA_pickQDriver(), bgc = (.619,.784,.902))
mc.text (' ')
mc.button (l = 'Select', c = lambda x:jsCA_qDriverTransSel(), w = 50, bgc = (.937,.867,.570))
jsCA_getQDriven_TF = mc.textField (bgc = (.15,.15,.15), w=200, ed = 1, text = 'object.attr, attr, attr...')
mc.button (w = 132, l = 'Load Driven + Attr(s)', c = lambda x:jsCA_pickQDriven(), bgc = (.661,.620,.902))
mc.text (' ')
mc.button (l = 'Select', c = lambda x:jsCA_qDrivenTransSel(), w = 50, bgc = (.937,.867,.570))

mc.setParent ('..')

mc.button (l = 'Quick Connect', c = lambda x:jsCA_QC(), bgc = (.635,.882,.605))

mc.showWindow (jsCA_winHide)