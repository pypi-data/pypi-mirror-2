.. ############################################################################
   #    Copyright (C) 2011 - 2011 by Eike Welk                                #
   #    eike.welk@gmx.net                                                     #
   #                                                                          #
   #    License: GPL                                                          #
   #                                                                          #
   #    This program is free software; you can redistribute it and#or modify  #
   #    it under the terms of the GNU General Public License as published by  #
   #    the Free Software Foundation; either version 2 of the License, or     #
   #    (at your option) any later version.                                   #
   #                                                                          #
   #    This program is distributed in the hope that it will be useful,       #
   #    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
   #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
   #    GNU General Public License for more details.                          #
   #                                                                          #
   #    You should have received a copy of the GNU General Public License     #
   #    along with this program; if not, write to the                         #
   #    Free Software Foundation, Inc.,                                       #
   #    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
   ############################################################################

.. This text contains reStructuredText markup. Convert it to HTML with:
    rst2html.py README.txt README.html



==========================================
Installing and using JBidwatcher-Companion
==========================================

-----------------------------------------------------------------------------
Analysis program for prices on Ebay; for use in conjunction with JBidwatcher. 
-----------------------------------------------------------------------------

The program creates price vs. time diagrams, with moving median price over a 
configurable period of time. It is a command line program, but the diagram is 
displayed in an interactive window. The diagram can be scaled, moved and 
saved as an image. 

The program reads files from JBidwatcher in `*.xml` and `*.csv` format.
By default it reads `~/.jbidwatcher/auctions.xml`, which is regularly updated 
by JBidwatcher (every 10 minutes).

Auctions can be selected for graphing based on two criteria: the tab where 
they reside, and their comment. These same criteria are also used to group 
the auctions into lines that appear in the diagram. 

For information on JBidwatcher go to: http://www.jbidwatcher.com/',


.. figure:: Nikon-SB.png

    The example image `Nikon-SB.png` (which is in the source packages) 
    shows prices for old Nikon flashes in Germany.



Installing Dependencies
=======================

This program is written in the Python programming language, and uses 
additional libraries for numerical computations and drawing graphs. The 
dependencies are: 

    - **Python** programming language (http://www.python.org/)
      The program has only been tested on **Python version 2.6**
    - **Numpy** library for numerical computations (http://numpy.scipy.org/)
    - **Matplotlib** library for drawing graphs (http://matplotlib.sourceforge.net/)


Windows
-------

Python is usually not present on Windows. The most easy way for Windows 
users to install all dependencies at once, is **Python XY** a (giant) Python 
distribution for scientists:

    http://www.pythonxy.com/


Linux
-----

*Python* is usually installed on all Linux distributions, *Numpy* and 
*Matplotlib* are not. However packages for *Numpy* and *Matplotlib* exist for 
most distributions. To install these libraries, use the installation program(s) 
for your Linux distribution. 

openSuse
~~~~~~~~

The most easy way to install *Numpy* and *Matplotlib* on openSuse, is through 
openSuse's website:

    http://software.opensuse.org/search

- Enter `Matplotlib` or `Numpy` into the search box. 
- Look for packages from the **science** repository. 
  (I successfully tested those packages some years ago.) 
- Install the packages by clicking on **1-Click Install**. 
- An installation program will start, that guides you through the details.

You need to install: **python-matplotlib**, **python-matplotlib-tk**, and 
**python-numpy** all from the same repository.

The **science** repository can also be added to the package management with the
administration program **Yast**. Open the **Software Repositories** dialog
and add the repository that matches your version of openSuse. The repositories 
are here: 

    http://download.opensuse.org/repositories/science/

The packages (*python-matplotlib*, *python-matplotlib-tk*, *python-numpy*)
will then appear in the **Software Management** dialog.

Ubuntu
~~~~~~

Numpy and Matplotlib are in the **Universe** component. Universe must be 
enabled, for Matplotlib and Numpy to appear in the package manager 
(*Add/Remove Applications* or *Synaptic*). This is explained here:
https://help.ubuntu.com/community/Repositories/Ubuntu

Red Hat
~~~~~~~

There are packages for Fedora on the Internet. I don't know any details though. 
Look here:

    http://rpmfind.net/linux/rpm2html/search.php?query=python-matplotlib&submit=Search+...&system=Fedora&arch=

Mandriva
~~~~~~~~

Similarly there are packages for Mandriva on the Internet:

    http://rpmfind.net/linux/rpm2html/search.php?query=python-matplotlib&submit=Search+...&system=mandriva&arch=

Other
~~~~~

If you can't find Numpy and Matplotlib for your operating system, 
look at these (somewhat cryptic) directions:

    http://www.scipy.org/Installing_SciPy/Linux


Mac
---

Hm... ?



Installation
============

There are several ways to install the program.

Easy
----

JBidwatcher-Companion can be installed with the program **easy_install**,
which downloads the necessary package from the Pyhon Package Index
(http://pypi.python.org/pypi), and installs it.   

Get administrative privileges, then open a **shell window** / **DOS box** 
and type: ::

    easy_install jbidwatcher-companion

Classical
---------

The classical installation from sources is possible too.
    - Download the `*.zip` or `*.tar.gz` source archive/package. 
    - Extract the contents of the archive.
    - Open a shell window / DOS box. 
    - Get administrator privileges.
    - Change to the folder that contains the archive's contents.
      (`JBidwatcher-Companion-*`). 
    - Type the following command: 
    
::
    
    python setup.py install

No Installation
---------------

The program consists only of the single file `ebstat.py`, and therefore needs no 
installation to run. The file can be stored in any directory and run there.
To behave like a regular command, you must make the file executable, and 
put it into the path.

If you don't want to make the file executable, for example for a quick test, 
you can run it like so: ::

    python ebstat.py ls
    
For detailed usage instructions see section *Usage* below. 



Usage
=====

Command line
------------

::

    ebstat.py [gr] -t <tab name> [<options>]
    ebstat.py ls [<options>]

The program understands two commands: "gr" and "ls". If no command is given,
"gr" is assumed.

* "graph", "gr" : Draw a time vs. price graph
* "ls"          : List the tabs, and show some minimal statistics.
    
    
Options
-------

  --version             Show program's version number and exit
  -h, --help            Show a help message and exit
  
  -t <tab name,...>, --include-tabs=<tab name,...>
                        Tabs that should be analyzed. Shell-style wildcards
                        can be used. For example "Nikon*" matches all names that
                        start with "Nikon". 
                        Default: ""
  -T <tab name,...>, --exclude-tabs=<tab name,...>
                        Tabs that should NOT be analyzed. Shell-style
                        wildcards can be used. 
                        Default: No default
  -c <comment name,...>, --include-comments=<comment name,...>
                        Comments that should be analyzed. Shell-style
                        wildcards can be used. 
                        Default: "*"; (All comments)
  -C <comment name,...>, --exclude-comments=<comment name,...>
                        Comments that should NOT be analyzed. Shell-style
                        wildcards can be used. 
                        Default: No default
                        
  -u <column>, --analyze-column=<column>
                        Column that should be analyzed. 
                        Default: "Total"
  -g <format string>, --group-auctions=<format string>
                        Group auctions into lines. 
                        
                        * "t": auctions from different tabs get into 
                          different lines
                        * "c": use comments to group auctions
                        * "tc": both criteria
                        * "_": all selected auctions get in one line. 
                            
                        Default: "tc"
  -w <number of days>, --window=<number of days>
                        Length of the window for computing the moving median.
                        Default: 31
                        
  -i <file name>, --input-file=<file name>
                        Name of input file that contains price information.
                        Default: "~/.jbidwatcher/auctions.xml"
  -o <file name>, --output-image=<file name>
                        Store generated graph as (PNG) image in the current
                        directory. 
                        Default: do not store image.
                        
  -b, --batch           Batch operation. Do not show any graph windows.
                        Default: False
  -l, --long-output     Show more information. 
                        Default: False
  --title=<title string>
                        Title of the chart. 
                        Default: Program creates title.
  --legend-position=<position>
                        Position of the legend. Possible values are: 
                        upper-left,  upper-center, upper-right, 
                        center-left, center,       center-right, 
                        lower-left,  lower-center, lower-right,
                        best. 
                        Default: best (Best position is chosen automatically.)


Graph Window
------------

The usage of the interactive graph window is mostly self explanatory, the 
main features are: 

* Clicking on an auction shows information about this auction in the bottom 
  right of the window. 
* The buttons at the bottom of the window can be used to pan, zoom, and 
  save an image of the graph.
* Pressing the 'g' key switches a grid on and off.

A detailed description is in the documentation of Matplotlib:  

    http://matplotlib.sourceforge.net/users/navigation_toolbar.html


Examples
--------

List the tabs in `~/.jbidwatcher/auctions.xml`: ::
    
    ebstat.py ls
    
Create a graph from the tab "Nikon SB": ::

    ebstat.py gr -t "Nikon SB"
    
Create a graph from all tabs that contain the word "Lens"; use only the 
comments to group auctions into lists; use a window of 50 days to compute the 
moving median: ::
    
    ebstat.py gr -t "*Lens*" -g c -w 50

Create a graph from a ".csv" file in the data directory; exclude auctions with 
the comments "SB 600" or "SB 800"; use a window of 50 days to compute the 
moving median. ::

    ebstat.py gr -i data/nikon-flash.csv -C "SB 600,SB 800" -w 50



Report Bugs
===========

Bugs and feature requests (set importance to wishlist) can be reported on 
the development website:

    https://bugs.launchpad.net/jbidwatcher-companion
    
     
     
Hacking / Contributing
======================

The program is currently developed on Linux (openSuse). Windows and Mac 
knowledge is very welcome! I use the IDE **Eclipse** and its extension 
**Pydev**. **Bazaar** is used for version control.
**Launchpad** is used for code hosting and to organize the coding effort. 
The project website is here:

    https://launchpad.net/jbidwatcher-companion

To get all development files type: ::

    bzr branch lp:jbidwatcher-companion

Testing is done with the "py.test" framework. All tests are in the file 
`test_ebstat.py`. To run the tests: change to the `src` directory and type: ::

    py.test
    
The test framework will then (find and) run the tests. In case of any errors it
will create (overwhelmingly many) colored messages that point to the error. 
"py.test" is Unfortunately not integrated into Eclipse, therefore there are no
click-able error messages.

See:
    - http://pytest.org/
    - http://pydev.org/
    - http://www.eclipse.org/
    - http://bazaar.canonical.com/en/
