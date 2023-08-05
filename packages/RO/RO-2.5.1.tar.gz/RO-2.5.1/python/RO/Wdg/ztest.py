#!/usr/bin/env python
import Tkinter
import Entry

def printWdgVals(wdg):
    print "Value=", wdg.getString()
    print "Default=", wdg.getDefault()

root = Tkinter.Tk()
e1 = Entry.StrEntry(
    master = root, 
    doneFunc = printWdgVals,
    autoSetDefault = True,
    defIfBlank = False,
)
e1.pack(side="top")
e2 = Entry.StrEntry(
    master = root, 
    doneFunc = printWdgVals,
    autoIsCurrent=True, 
    autoSetDefault = True,
    defIfBlank = False,
)
e2.pack(side="top")
e3 = Entry.StrEntry(
    master = root, 
    doneFunc = printWdgVals,
    autoIsCurrent=True, 
    autoSetDefault = True,
#    trackDefault = True,
    defIfBlank = False,
)
e3.pack(side="top")
e4 = Entry.StrEntry(
    master = root, 
    doneFunc = printWdgVals,
    autoIsCurrent=True, 
    autoSetDefault = True,
#    trackDefault = True,
    defIfBlank = True,
)
e4.pack(side="top")

def setDef(wdg=None):
    e1.setDefault("e1def")
    e2.setDefault("e2def")
    e3.setDefault("e3def")
    e4.setDefault("e4def")

def setVals(wdg=None):
    e1.set("e1")
    e2.set("e2")
    e3.set("e3")
    e4.set("e4")

def printAllVals(wdg=None):
    for wdg in (e1, e2, e3, e4):
        printWdgVals(wdg)

b1 = Tkinter.Button(root, text="Set Default", command=setDef)
b1.pack(side="top")
b2 = Tkinter.Button(root, text="Set Vals", command=setVals)
b2.pack(side="top")
b3 = Tkinter.Button(root, text="Print Vals", command=printAllVals)
b3.pack(side="top")

root.mainloop()
