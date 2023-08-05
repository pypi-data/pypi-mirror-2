#!/usr/bin/env python
# coding: utf-8

__doc__ = """ python wrapper for dialog/Xdialog/gdialog programs.

Global variables:

DIALOG_CMD - dialog command(default is "dialog", you may want to use gdialog or Xdialog instead)
USE_STDOUT - use stdout for dialog output; you should use it only with Xdialog
BACKTITLE - Specifies a backtitle string to be displayed on the backdrop of all dialogs(could be overridden with backtitle keyword argument).

Functions accept following keyword arguments:

size - window size (HEIGHT,WIDTH)
extra_button - show "Extra" button; if  you assign it to callable it will be executed on "Extra" button press
    e.g. extra_button=lambda menuitem: dlg.msgbox(menuitem)
    use isinstance(result,dlg.Extra) to check if "Extra" button was pressed
help_button - show "Help" button; if you assign it to callable it will be executed on "Help" button press
    e.g. help_button=show_help
    use isinstance(result,dlg.Help) to check if "Help" button was pressed
no_cancel - Suppress the "Cancel" button in checklist, inputbox and menu box.
title - Specifies a title string to be  displayed  at  the  top  of  the dialog box.
backtitle - Specifies a backtitle string to be displayed on the backdrop, at the top of the screen.
cancel_label - Override the label used for "Cancel" buttons.
exit_label - Override the label used for "EXIT" buttons.
extra_label - Override the label used for "Extra" buttons.
help_label - Override the label used for "Help" buttons.
no_label - Override the label used for "No" buttons.
ok_label - Override the label used for "Ok" buttons.
yes_label - Override the label used for "Yes" buttons.
max_input - Limit input strings to the given size. If not specified, the limit is 2048.
no_ok - Suppress the "OK" button in checklist, inputbox and menu box modes.
no_shadow - Suppress shadows that would be drawn to the right and bottom of each dialog box.

timeout - Timeout (exit with error code) if no user response within the given number of seconds.

Read 'man dialog' for more information.

"""
__version__ = '0.2'
__author__ = 'Mikhail Sakhno'
__author_email__ = 'pawn13@gmail.com'
__url__ = 'http://tabed.org/dlg/'
__download_url__ = 'http://tabed.org/dlg/dlg.tar.gz'

import subprocess,sys

DIALOG_CMD = 'dialog'
if not sys.stdin.isatty():
    if not os.system('which gdialog >/dev/null'):
        DIALOG_CMD = 'gdialog'
    elif not os.system('which Xdialog >/dev/null'):
        DIALOG_CMD = 'Xdialog'
    else:
        pass # don't know what to do?
USE_STDOUT = False
BACKTITLE = None

def _func_name():
    return sys._getframe(1).f_code.co_name

class Extra(object):
    pass

class Help(object):
    pass

class _dialog(object):
    def __init__(self,mode,**kargs):
        self.args = kargs.get('args',[])
        self.args2 = kargs.get('args2',[])
        self.args0 = kargs.get('args0',[])
        self.size = kargs.get('size',[0,0])
        self.mode = mode
        if 'ret' in kargs:
            self._return=kargs['ret']
        if 'extra_button' in kargs:
            if callable(kargs['extra_button']):
                self._extra = kargs['extra_button']
        if 'help_button' in kargs:
            if callable(kargs['help_button']):
                self._help = kargs['help_button']
        for k in ('extra_button','help_button','no_cancel','nocancel','no_ok','nook','no_shadow'):
            if k in kargs:
                self.args0+=['--%s' % k.replace('_','-')]
        if 'backtitle' not in kargs and BACKTITLE:
            kargs['backtitle'] = BACKTITLE
        for k in ('title','cancel_label','exit_label','extra_label','help_label','no_label','ok_label','yes_label','backtitle','max_input','timeout'):
            if k in kargs:
                self.args0+=['--%s' % k.replace('_','-'),kargs[k]]
    def run(self):
        self.proc = subprocess.Popen(map(str,[DIALOG_CMD]+self.args0+(['--stdout'] if USE_STDOUT else [])+['--%s' % self.mode]+self.args+self.size+self.args2), **({'stdout':subprocess.PIPE} if USE_STDOUT else {'stderr':subprocess.PIPE}))
        self.errlev = self.proc.wait()
        if self.errlev in (0,2,3):
            self.result = self._return((self.proc.stdout if USE_STDOUT else self.proc.stderr).read())
            if self.errlev == 2:
                if self._help.func_code.co_argcount:
                    self._help(self.result)
                else:
                    self._help()
                self.result = type('Help',(type(self.result),Help,),{})(self.result)
            elif self.errlev == 3:
                if self._extra.func_code.co_argcount:
                    self._extra(self.result)
                else:
                    self._extra()
                self.result = type('Extra',(type(self.result),Extra,),{})(self.result)
        else:
            self.result = None
            if self.errlev == 1:
                self.result = False
        return self.result
    def _return(self,res):
        return res
    def _help(self):
        pass
    def _extra(self,result):
        pass

def yesno(text,default=True,**kargs):
    return isinstance(_dialog(_func_name(),args=[text],args0=[] if default else ['--defaultno'],**kargs).run(),basestring)

def msgbox(text,**kargs):
    return _dialog(_func_name(),args=[text],**kargs).run()

def infobox(text,**kargs):
    return _dialog(_func_name(),args=[text],**kargs).run()

def pause(text,seconds,**kargs):
    return isinstance(_dialog(_func_name(),args=[text],args2=[seconds],**kargs).run(),basestring)

def inputbox(text,default='',**kargs):
    return _dialog(_func_name(),args=[text],args2=[default],ret=lambda res:res.rstrip(),**kargs).run()

def passwordbox(text,default='',**kargs):
    return _dialog(_func_name(),args=[text],args2=[default],ret=lambda res:res.rstrip(),**kargs).run()
    
def dselect(path,**kargs):
    return _dialog(_func_name(),args=[path],**kargs).run()

def fselect(path,**kargs):
    return _dialog(_func_name(),args=[path],**kargs).run()

def calendar(text,day,month,year,**kargs):
    return _dialog(_func_name(),args=[text],args2=[year,month,day],ret=lambda res: tuple(map(int,res.split('/'))),**kargs).run()

def timebox(text,hour,minute,second=0,**kargs):
    return _dialog(_func_name(),args=[text],args2=[hour,minute,second],ret=lambda res: tuple(map(int,res.split(':'))),**kargs).run()

def form(text,items,**kargs):
    args2=[len(items)]
    for i,item in enumerate(items):
        if isinstance(item,basestring):
            item=(item,'')
        args2+=[item[0],i+1,1,item[1],i+1,15,30,30]
    return _dialog(_func_name(),args=[text],args2=args2,ret=lambda res:res.splitlines() ,**kargs).run()

def passwordform(text,items,**kargs):
    args2=[len(items)]
    for i,item in enumerate(items):
        if isinstance(item,basestring):
            item=(item,'')
        args2+=[item[0],i+1,1,item[1],i+1,15,30,30]
    return _dialog(_func_name(),args=[text],args2=args2,ret=lambda res:res.splitlines() ,**kargs).run()

def menu(text,items,**kargs):
    args2=[len(items)]
    for item in items:
        if isinstance(item,basestring):
            item=(item,item)
        if len(item)==1:
            item=(item[0],item[0])
        args2.extend(item)
    return _dialog(_func_name(),args=[text],args2=args2,ret=lambda res:res.strip().strip('"\'') ,**kargs).run()

def radiolist(text,items,**kargs):
    args2=[len(items)]
    for item in items:
        if isinstance(item,basestring):
            item=(item,item)
        if len(item)==1:
            item=(item[0],item[0])
        args2.extend(item)
    return _dialog(_func_name(),args=[text],args2=args2,ret=lambda res:res.strip().strip('"\'') ,**kargs).run()

def checklist(text,items,**kargs):
    args2=[len(items)]
    for item in items:
        if isinstance(item,basestring):
            item=(item,item)
        if len(item)==1:
            item=(item[0],item[0])
        if len(item)==3:
            item=(item[0],item[1],'on' if item[2] else 'off')
        elif len(item)==2:
            item=(item[0],item[1],'off')
        args2.extend(item)
    return _dialog(_func_name(),args=[text],args2=args2,ret=lambda res:[i.strip('"\'') for i in res.split()] ,**kargs).run()

def editbox(path,**kargs):
    return _dialog(_func_name(),args=[path],**kargs).run()

def textbox(path,**kargs):
    return _dialog(_func_name(),args=[path],**kargs).run()
 
def tailbox(path,**kargs):
    return _dialog(_func_name(),args=[path],**kargs).run()

#def tailboxbg(path,**kargs):
#    return _dialog(_func_name(),args=[path],**kargs).run()

class progressbox(_dialog):
    """
    Will show what you send there with "update" method, until you call "close" method.
    Example:
    pb = dlg.progressbox('example')
    for line in open('/some/file'):
        pb.update(line)
    pb.close()
    """
    def __init__(self,text='',**kargs):
        #super(_dialog,self).__init__(_func_name(),args=[text],**kargs)
        _dialog.__init__(self,'progressbox',args=[text] if text else [],**kargs)
        self.proc = subprocess.Popen(map(str,[DIALOG_CMD]+self.args0+['--%s' % self.mode]+self.args+self.size+self.args2),stdin=subprocess.PIPE)
    def update(self,val):
        print >>self.proc.stdin, val
    def close(self):
        self.proc.stdin.close()

class gauge(_dialog):
    """
    A  gauge  box displays a meter along the bottom of the box.  The meter indicates the percentage.
    Example:
    gauge1 = dlg.gauge('example')
    for percent in range(0,100):
        gauge1.update(percent)
        time.sleep(0.01)
    gause1.close()
    """
    def __init__(self,text,percent=0,**kargs):
        #super(_dialog,self).__init__(_func_name(),args=[text],**kargs)
        _dialog.__init__(self,'gauge',args=[text],**kargs)
        self.proc = subprocess.Popen(map(str,[DIALOG_CMD]+self.args0+['--%s' % self.mode]+self.args+self.size+self.args2),stdin=subprocess.PIPE)
    def update(self,val):
        print >>self.proc.stdin, val
    def close(self):
        self.proc.stdin.close()

def mixedgauge(text,items,percent=0,**kargs):
    args2=[percent]
    for item in items:
        if isinstance(item,basestring):
            item=(item,item)
        if len(item)==1:
            item=(item[0],item[0])
        args2.extend(item)
    return _dialog(_func_name(),args=[text],args2=args2,**kargs).run()




#TODO:
#inputmenu    <text> <height> <width> <menu height> <tag1> <item1>...
#mixedform    <text> <height> <width> <form height> <label1> <l_y1> <l_x1> <item1> <i_y1> <i_x1> <flen1> <ilen1> <itype>...

