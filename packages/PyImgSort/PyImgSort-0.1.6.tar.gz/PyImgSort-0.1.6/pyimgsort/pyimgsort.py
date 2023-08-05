#######################################
#   program:  pyimgsort.py
#   author:  x.seeks
#   version:  0.15
#   date:  2010-08-12
#   description:  Sorts images into
#   separate directories by apect ratio
########################################


##  These bad boys do all the work.  Image is the only one that's not a
##  default Python library.  Find it at http://www.pythonware.com/products/pil
import sys
import os
import Image
import shutil
import platform




# These are used later
countlist = []
badcountlist = []

## Some color code initially borrowed from linux-image-writer.py
##  These are all bolded

# First, it detects if the platform is Windows.  If it is, the colors are
# set to nothing because the "DOS prompt" (cmd) can't display these colors.

platformname = platform.system()

if platformname == "Windows":
    COLOR_BLACK = ''
    COLOR_RED =   ''
    COLOR_LG = ''
    COLOR_LC = ''
    COLOR_LB = ''
    COLOR_YELLOW = ''
    COLOR_DG = ''
else:
    COLOR_BLACK = "\033[00m"
    COLOR_RED =   "\033[1;31m"
    COLOR_LG = "\033[1;32m"
    COLOR_LC = "\033[1;36m"
    COLOR_LB = "\033[1;34m"
    COLOR_YELLOW = "\033[1;33m"
    COLOR_DG = "\033[1;30m"

## The following makes a list of the files in 'x', then sets the
## the current working directory to 'workdir'.  It then sends the files list
## to 'validate(x)', and then tells imgcount to print.  This function is
## probably the main go-to guy for the module.
     
def getfiles(x):
    """ Makes a list of files in 'x', then changes the cwd to 'workdir' """
    workdir = str(x)
    os.chdir(workdir)
    filelist = os.listdir(os.getcwd())
    for x in filelist:
        validate(x)
    count = countlist.count(1)
    badcount = badcountlist.count(1)
    imgcount(count, badcount)
    #print badcount


## The following tries tries opening whatever file was sent to it by
## by getfiles(x).  If the file is valid, it's sent to filer(x)  This function
## also tallies the number of valid and invalid files processed.

def validate(x):
    """ 
    This sends valid files to be processed in filer(x), and passes over files  that aren't images.  It also tallies the number of either type processed.
    """
    validfiles = []
    try:
        imgfile = open(x, "rb")
        im = Image.open(imgfile)
        validfiles.append(x)
        countlist.append(1)
        imgfile.close()
        del im
    except IOError:
        badcountlist.append(1)
        pass
    if validfiles != []:
        filer(x)

            
##  The following checks for the existence of directory 'x'.  If 'x' does
##  exist, it passes.  If not, directory 'x' is created.  Basically, for
##  each image, it checks to see if the appropriate directory for it exists.

def dir_check(x):
    """ 
    Checks for the existence of 'x'.  If 'x' exists, it passes.  If 'x' does not exist, it will be created
     """
    if os.path.isdir(x):
        pass
    else:
        os.mkdir(x)
        

##  This sorts the image files according to their dimensions, and then sends
##  them on their way to the mover function.

def filer(x):
    """
     Sorts images according to orientation, sending them to their respective filer:  filer_landscape(x), filer_portrait(x), or filer_square(x). 
     """
    portrait = []
    landscape = []
    imgfile = open(x, "rb")
    img = Image.open(imgfile)
    w,h = img.size
    w = float(w)
    h = float(h)
    ratio = w / h
    del img
    imgfile.close()
    if ratio > 1:
        filer_landscape(x)
    elif ratio < 1:
        filer_portrait(x)
    elif ratio == 1:
        filer_square(x)
  

##  This prints the number of images successfully processed.  'x' was counted
##  in 'filer(x)'  It also prints the number of non-images that were ignored.

def imgcount(x,y):
    """ Prints the number of images processed, and non-images ignored """
    print '\n' * 2
    print '-' * 15
    print COLOR_LG, '%d images sorted.' % x, COLOR_BLACK
    print '-' * 15
    print COLOR_YELLOW, '%d files ignored.' % y, COLOR_BLACK
    print '-' * 15
    print '\n' * 2
    

    
        

##  This is the function that does the actual moving (and also runs the
##  'dir_check' function) as specified in 'filer_landscape(x)' or
##  'filer_portrait(x)'.

def mover(x, ratio, w, h, res):
    """ 
    This runs the dir_check(x) function, then moves the files as specified in either filer_landscape(x) or filer_portrait(x)
     """
    print COLOR_LB, '%s : ' % x, COLOR_YELLOW, '[%d x %d]' % (int(w), int(h)), COLOR_BLACK + '=', '%s' % res, COLOR_BLACK,'=' * 5 + '>', COLOR_LC, '%s' % ratio, COLOR_BLACK
    dir_check(ratio)
    shutil.move(x, './%s/%s' % (ratio, x))
    


## This files square images, sending them to the mover.

def filer_square(x):
    """
    This files square images, sending them to the mover.
    """
    imgfile = open(x, "rb")
    img = Image.open(imgfile)
    w,h = img.size
    w = float(w)
    h = float(h)
    ratio = '1-1'
    res = '1:1 (Square)'
    del img
    imgfile.close()
    mover(x, ratio, w, h, res)
    
    
##  This is the filer for landscape-oriented images.  If the image meets
##  certain criteria, it's sent to 'mover(image, ratio, w, h, res)', along
##  with the appropriate arguments.


def filer_landscape(x):
    """ 
    Sorts landscape-oriented images according to aspect ratio, sending the results to mover(image, ratio, w, h, res) to do the actual moving. 
    """
    imgfile = open(x, "rb")
    img = Image.open(imgfile)
    w,h = img.size
    w = float(w)
    h = float(h)
    ratio = w / h
    del img
    imgfile.close()
    if ratio == 1.6:
        ratio = '16-10'
        res = '16:10'
        mover(x, ratio, w, h, res)
    elif ratio > 1.7 and ratio <= 1.79:
        ratio = '16-9'
        res = '16:9'
        mover(x, ratio, w, h, res)
    elif ratio >= 1.3 and ratio < 1.4:
        ratio = '4-3'
        res = '4:3'
        mover(x, ratio, w, h, res)
    elif ratio > 1.48 and ratio <= 1.5:
        ratio = '3-2'
        res = '3:2'
        mover(x, ratio, w, h, res)
    elif ratio == 1.25:
        ratio = '5-4'
        res = '5:4'
        mover(x, ratio, w, h, res)
    elif ratio > 1.64 and ratio < 1.66:
        ratio = '1_66-1'
        res = '1.66:1'
        mover(x, ratio, w, h, res)
    elif ratio > 1.66 and ratio < 1.7:
        ratio = '5-3'
        res = '5:3'
        mover(x, ratio, w, h, res)
    elif ratio > 1.8 and ratio <= 1.85:
        ratio = '1_85-1'
        res = '1.85:1'
        mover(x, ratio, w, h, res)
    elif ratio > 2.37 and ratio <= 2.4:
        ratio = '2_39-1'
        res = '2.39:1'
        mover(x, ratio, w, h, res)
    else:
        ratio = 'misc_landscape'
        res = 'misc (landscape)'
        mover(x, ratio, w, h, res)
			

##  This is the filer for portrait-oriented images.  If the image meets
##  certain criteria, it's sent to 'mover(image, ratio, w, h, res)', along
##  with the appropriate arguments.

def filer_portrait(x):

    """ 
    Sorts landscape-oriented images according to aspect ratio, sending the results to mover(image, ratio, w, h, res) to do the actual moving. 
    """
    
    imgfile = open(x, "rb")
    img = Image.open(imgfile)
    w,h = img.size
    w = float(w)
    h = float(h)
    ratio = h / w
    del img
    imgfile.close()
    if ratio == 1.6:
        ratio = '16-10_p'
        res = '16:10 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio > 1.7 and ratio <= 1.79:
        ratio = '16-9_p'
        res = '16:9 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio >= 1.3 and ratio < 1.4:
        ratio = '4-3_p'
        res = '4:3 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio > 1.48 and ratio <= 1.5:
        ratio = '3-2_p'
        res = '3:2 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio == 1.25:
        ratio = '5-4_p'
        res = '5:4 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio > 1.64 and ratio < 1.66:
        ratio = '1_66-1_p'
        res = '1.66:1 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio > 1.66 and ratio < 1.7:
        ratio = '5-3_p'
        res = '5:3 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio > 1.8 and ratio <= 1.85:
        ratio = '1_85-1_p'
        res = '1.85:1 (portrait)'
        mover(x, ratio, w, h, res)
    elif ratio > 2.37 and ratio <= 2.4:
        ratio = '2_39-1_p'
        res = '2.39:1 (portrait)'
        mover(x, ratio, w, h, res)
    else:
        ratio = 'misc_portrait'
        res = 'misc (portrait)'
        mover(x, ratio, w, h, res)
			
			
##  This asks the user for a directory to sort if no argument was
##  provided on the command-line.  It sends the result to 'confirmworkdir(x)'.

def getworkdir():
    """ 
    If no valid argument was provided on the command-line, this asks the user for a directory to sort 
    """
    print "\n" * 2
    userin = raw_input("Enter a directory you'd like to sort (or 'q' to quit) :  ")
    workdir = str(userin)
    if os.path.isdir(workdir):
        confirmworkdir(workdir)
    elif workdir == 'q' or workdir == 'quit' or workdir == 'exit' or workdir == 'x' or workdir == 'Q' or workdir == 'QUIT' or workdir == 'EXIT' or workdir == 'X':
        quit()
    else:
        print "\n"
        print COLOR_RED, "That's not a valid directory.", COLOR_BLACK, "Try again."
        print "\n"
        getworkdir()


##  This confirms the choice the user makes in 'getworkdir()'.
      
def confirmworkdir(x):
    """ This confirms the choice the user makes in getworkdir() """
    workdir = str(x)
    print ''
    print COLOR_DG, '=' * 10, COLOR_BLACK
    print "You've chosen:"
    print COLOR_LC, workdir
    print COLOR_DG, '=' * 10, COLOR_BLACK
    print ''
    uin = raw_input("Is this correct?  (y.es, n.o, q.uit)  :  ")
    ua = str(uin)
    if ua == 'y' or ua == 'yes' or ua == 'Y' or ua == 'YES':
        getfiles(workdir)
    elif ua == 'n' or ua == 'no' or ua == 'N' or ua == 'NO':
        print "\n" * 3
        print "Then let's try again."
        print '-' * 10
        print "\n" * 3
        getworkdir()
    elif ua == 'q' or ua == 'quit' or ua == 'exit' or ua == 'x' or ua == 'Q' or ua == 'QUIT' or ua == 'EXIT' or ua == 'X':
        quit()
    else:
        print "\n" * 2
        print COLOR_RED, "YES, NO, or QUIT,", COLOR_BLACK, "please."
        confirmworkdir(workdir)
        

##  This is the code that runs when started from a command-line.

if __name__ == '__main__':

    try:
        start_dir = sys.argv[1]
        workdir = str(start_dir)
        getfiles(workdir)
    except:
        getworkdir()

