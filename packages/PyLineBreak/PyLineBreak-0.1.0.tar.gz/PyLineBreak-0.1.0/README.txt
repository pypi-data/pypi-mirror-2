===========
PyLineBreak
===========

PyLineBreak is a small utility that breaks very long lines into smaller ones.  More specifically, it limits a line to 80 characters in length and will 'fix' text files that do not conform to that limitation.  This allows for easier reading in terminal shells or a TTY console.

    ----------
    ON *NIX
    ----------

    $ pylinebreak
    
    OR
    
    $ python /path/to/pyimgsort.py path/to/file
    
    
    -----------
    ON WINDOWS:
    -----------
    
    Open a command prompt and type:
    
    C:\path\to\python.exe C:\path\to\pylinebreak.py C:\path\to\file
    
    OR
    
    C:\path\to\python.exe C:\path\to\pyimgsort.py
    



Requirements:
==============

* Python 2.6 or later



Installation:
==============

* In GNU/Linux:  Unpack the tarball, open a terminal, navigate to the directory into which you unpacked the tarball, and type (as admin, i.e., "su" or "sudo") ``python setup.py install``

* In Windows, just run the .exe as normal.  The script will be installed to C:\\Pythondir\\Lib\\site-packages

Notes
-------------

This program will format text files to fit inside an 80-character margin.  Chances are, if you edit inside a GUI text editor (or copy/paste into one), the lines won't be broken the same way they are with programs like Emacs or Vim.  Consequently, they can be unpleasant to edit or read inside a shell or TTY terminal.

This program alleviates the problem somewhat.  There will be a few short lines every here and there, but the resultant file is still quite a lot easier to deal with than before.

By default, the program creates backups in the same directory and sets the margin at 80 characters.  You can change these settings by editing their values near the top of the source file (pylinebreak.py).



Author
-------------

* x.seeks (x -dot- seeks _at_ gmail -dot- com)




License
-------------

GPL version 3.  See LICENSE.txt for more info.
