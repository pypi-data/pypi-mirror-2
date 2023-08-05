from Tkinter import *

def makeEntry(parent,  label ,  type = 'str'):
    '''creates a frame containg a label and Entry widget, and returns 
        a Tkinter variable'''

    vdict = {'str':'StringVar()', 'int': 'IntVar()'}
    labelWidth = 20
    frm = Frame(parent)
    frm.pack(side = TOP)
    vType = vdict[type]
    exec('eVar = %s' % vType)
    Label(frm,  text = label,  anchor = E, width = labelWidth).pack(side = LEFT)
    Entry(frm, textvariable = eVar).pack(side = LEFT)
    return eVar


''' note on memumaker's data input:
    the top level is a list of tuples
      [(...),(...), ...]
      each tuple has three elements: a string name, a shortcut underline key, and
        EITHER a reference to a method (i.e. a command item)
          ('Cancel', 0, self.onCancel)
        OR a list (indicating a top-level cascade menu item).
          ('File', 0,[...])
          this list's items are EITHER tuples with the same contents (name, 
            underline key, and a command|list)
          OR the string 'separator' 
      
    This version has been changed from Lutz's to make class 
    avaliable by import & instantiation v. a mixin '''

class MenuMaker(object):
    def menuMaker(self, parent,  menuItems):
        menubar = Menu(parent)
        parent.config(menu=menubar)
        for title,  key,  dat in menuItems:
            if not isinstance(dat, list): # a main menuBar command item
                menubar.add_command(label= title, underline = key,  command = dat,  background='lightgrey')
            else:
                new = Menu(menubar)
                self.addMenuItems(parent,  new,  dat)
                menubar.add_cascade(label=title,  underline=key, menu = new)

    def addMenuItems(self, parent, menu, items):
        #after Mark Lutz :: Programming Python
        for item in items:                     # scan nested items list
            if item == 'separator':            # string: add separator
                menu.add_separator({})
            elif type(item) == ListType:       # list: disabled item list
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif type(item[2]) != ListType:
                menu.add_command(label = item[0],         # command: 
                                 underline = item[1],         # add command
                                 command   = item[2])         # cmd=callable
            else:
                pullover = Menu(menu)
                self.addMenuItems(pullover, item[2])          # sublist:
                menu.add_cascade(label     = item[0],         # make submenu
                                            underline  = item[1],         # add cascade
                                            menu        = pullover) 

if __name__ == '__main__':
    
    from Tkinter import *
    class fred(Toplevel,  MenuMaker):
        def __init__(self,  master = None):
            Toplevel.__init__(self, master = None)
            self.title('hello world')
            self.setMenuData()
            mm = MenuMaker()
            mm.menuMaker(self, self.mnuItems)

        def setMenuData(self):
            self.mnuItems=[
                ('Cancel', 0, self.cancel), 
                ('Ok', 0, self.ok), 
                ('File', 0,                             # a GuiMaker menu def tree
                    [('Open...',    0, self.onOpen),   # build in method for self
                    ('Save',       0, self.onSave),   # label, shortcut, callback
                    'separator',
                    ('Quit...',    0, self.cancel)]
                    ),
                    ('Edit', 0,
                         [('Undo',       0, self.onUndo),
                          ('Redo',       0, self.onRedo),
                          'separator',
                          ('Cut',        0, self.onCut)]
                    ), ]

        def cancel(self):
            self.destroy()

        def ok(self):
            print 'ok '* 10
            
        def onOpen(self):
            pass

        def onSave(self):
            pass

        def onUndo(self):
            pass

        def onRedo(self):
            pass

        def onCut(self):
            pass    

    root=Tk()
    root.withdraw()
    fred()
    root.mainloop() 

#    root = Tk()
#    var = makeEntry(root, 'test: ', 'str')
#    var.set('nonesense')
#    var2 = makeEntry(root,  'another: ',  'str')
#    var2.set('beans for breakfast')
#    root.mainloop()
