############################################
##
##   program:  pyimgsortgui.py
##   author:  x.seeks
##   version:  0.10
##   date:  2010-08-13
##   description:  GUI frontend for PyImgSort
##
#############################################

## The imports

import pyimgsort
from Tkinter import *

# This is a slightly modified version of the default EasyGui.
# Get the original at http://easygui.sourceforge.net
from piseasygui import *

from tkFont import *

# Whenever a directory is selected, its string is added to a list.  In this
# Case, 'dirlist."  The list is used to rerieve whatever the current directory
# is by grabbing the last index ([-1]).
dirlist = ['nothin']



root = Tk()


# Set some StringVars to use later, for labels that show up or disappear
# depending on certain circumstances 
v = StringVar()
v2 = StringVar()
v3 = StringVar()

v.set('')
v2.set('')
v3.set('')


## Sets initial state of confirmchoice, which is potentially set later by
## piseasygui
confirmchoice = 0


step2text = """
Step 2:
If the directory chosen above is correct, 
click on "Confirm directory" to sort it."""

sorted_text = str("%s sorted." % dirlist[-1])

## Define the buttons!

def button_exit_command():
    exit()
    pass
    

def button_choose_command():   
    chosendir = str(diropenbox())
    dirlist.append(chosendir)
    dirname = str(chosendir)
    dirname2 = v.set(dirname)
    v2set = v2.set(step2text)
    return dirlist
    return dirname2
    
    
## First, this checks to make sure you've chosen a directory.  Then, if you
## Select confirm, it sends the data straight to pyimgsort.  It then pops
## up a dialog informing you that the directory has been sorted.  This is
## currently a "dumb" dialog; it doesn't actually check.

def button_confirm_command():
    """First, this checks to see if you've chosen a directory.  If yes, it sends the data to pyimgsort, then lets you know it's been sorted.  If not, it tells you.  You can also just cancel."""
    if dirlist != []:
        confirmchoice = int(ynbox(msg="You've chosen %s.  Is this correct?" % dirlist[-1], title="Confirm Directory", choices=("> Cancel",">> Confirm"), image=None))
        if confirmchoice == 1:
            try:
                dirname = str(dirlist[-1])
                pyimgsort.getfiles(dirname)
                v3.set(str("%s sorted." % dirlist[-1]))
                msgbox("Directory sorted.")
            except IOError:
                v3.set(str("Invalid directory, try again."))
                msgbox("Invalid directory:  nothing sorted.  Choose another directory.")

    else:
        msgbox("No directory chosen, yet.")
    pass

def button_about_command():
    about_text = """
    PyImgSort is a simple program that will automatically sort
    any given directory's images into subdirectories according
    to aspect ratio.  1440x900 images will be moved into 
    "16_10", 1920x1280 files gets put into a "16_9" folder,
    so on and so forth.
    
    This GUI (PyImgSortGUI) is a front-end for PyImgSort,
    meaning that you do not actually have to use this GUI.  If
    you'd prefer to use only the command-line version of
    PyImgSort, you can find that script in the same directory
    as this one.  Alternately, if you're using GNU/Linux, you
    can just type pyimgsort-cli into a terminal.
    
    This program is licensed under the GPLv3.
    See LICENSE.txt for more details.
    
    Bugs?  I'm sure you'll find some.  Contact me and I'll
    get around to them eventually.
    
    Author:  x.seeks (x.seeks@gmail.com)
    Project Page:  http://pypi.python.org/pypi/PyImgSort
     """
    msgbox("%s" % about_text)
    
    

step1text = """Step 1:
Click on the "Choose directory" 
button to select a directory:"""


## Create the labels, buttons, etc.

label_step1 = Label(root, height=3, width=40, text="%s" % step1text)
label_chosendir = Label(root, height=1, width=60, textvariable=v)
label_step2 = Label(root, height=4, width=40, textvariable=v2)
label_sorted = Label(root, height=1, width=40, textvariable=v3)
button_exit = Button(root, text = "Exit")
button_exit.configure(command = button_exit_command)
button_choose = Button(root, text = "1. > Choose directory")
button_choose.configure(command = button_choose_command)
button_confirm = Button(root, text = "2. >> Confirm directory")
button_confirm.configure(command = button_confirm_command)
button_about = Button(root, text = "About")
button_about.configure(command = button_about_command)


## Pack (place) the labels, buttons, etc.
label_sorted.pack(side=BOTTOM, padx=10, pady=10)
button_exit.pack(side=LEFT, anchor=NW, padx=10, pady=10)
button_about.pack(side=RIGHT, anchor=NE, padx=10, pady=10)
button_confirm.pack(side=BOTTOM, padx=10, pady=20)
label_step2.pack(side=BOTTOM, padx=10, pady=10)
label_chosendir.pack(side=BOTTOM, expand=1)
button_choose.pack(side=BOTTOM, padx=10, pady=10)
label_step1.pack(side=BOTTOM, pady=10)


## Special magic tkFont stuff.  I don't really know how it works.
f = Font(font=label_chosendir['font'])
f['weight'] = 'bold'

label_chosendir['font'] = f.name 

f2 = Font(font=label_sorted['font'])
f2['weight'] = 'bold'

label_sorted['font'] = f2.name 



## Run
mainloop()
