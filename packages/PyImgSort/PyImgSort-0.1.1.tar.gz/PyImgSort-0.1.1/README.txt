===========
PyImgSort
===========

PyImgSort is a simple utility that automatically organizes a directory of image files into subdirectories by their aspect ratio.  Its intended use is the sorting of large 'wallpaper' directories.::

    $ python pyimgsort */absolute/path/to/directory*
    
    **or**
    
    $ python pyimgsort
    ``>>> Enter a directory you'd like to sort:`` *absolute/path/to/directory*
    
    **In Windows:**
    
    Open a command prompt and type:
    
    C:\path\to\python.exe C:\path\to\pyimgsort.py



Requirements:
=============

* Python 2.6 or later

* The Python Imaging Library >= 1.1.6 (http://www.pythonware.com/products/pil/)

Notes
-------------

I'm very new to Python.

This is an ugly, barely-functional script.  It's not really meant for general consumption, but you're more than welcome to use it if you think you can get some use out of it.  For that matter, you're also more than welcome to modify it, copy it, distribute it (free of charge), etc. to your heart's content.

While this script does *work* on Windows, it errors out at the end.  The pictures are all still moved, though.


Author
-------------

* x.seeks (x -dot- seeks _at_ gmail -dot- com)



Thanks also to
---------------

From the Penny Arcade forums (http://forums.penny-arcade.com)

*MKR*
*quietjay*
*End*
*JHunz*

For fixing my broken code.


License
-------------

GPL version 3.  See LICENSE.txt for more info.
