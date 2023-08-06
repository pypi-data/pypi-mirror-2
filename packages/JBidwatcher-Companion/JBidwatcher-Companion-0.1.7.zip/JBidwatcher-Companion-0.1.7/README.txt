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

..  This text contains reStructuredText markup for the documentation generator
    Sphinx. It serves double duty: As ``readme.rst`` it contains the website's  
    section "Installation and Quickstart"; the release script copies it to 
    ``README.txt``.

    

.. ############################################################################
   #                                                                          #
   #                        JBidwatcher Companion                             #
   #                                                                          #
   #                                                                          #
   #     Analysis program for prices on Ebay, for use in conjunction with     #
   #                              JBidwatcher.                                #
   #                                                                          #
   ############################################################################

.. highlight:: bash



===============================================================================
                          Installation and Quickstart
===============================================================================

The program ``ebstat.py`` creates price vs. time diagrams, with moving median 
price over a configurable period of time. It is a command line program, but 
the diagram is displayed in an interactive window. The diagram can be scaled, 
moved and saved as an image. 

The program analyzes files created by the Ebay bidding program JBidwatcher.
For information on JBidwatcher go to: 

    http://www.jbidwatcher.com/



Installing Dependencies
===============================================================================

This program is written in the Python programming language, and uses 
additional libraries for numerical computations and drawing graphs. The 
dependencies are: 

    - **Python**: programming language (http://www.python.org/)
      The program has only been tested on **Python version 2.6**
    - **Numpy**: library for numerical computations (http://numpy.scipy.org/)
    - **Matplotlib**: library for drawing graphs (http://matplotlib.sourceforge.net/)


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

- Enter ``Matplotlib`` or ``Numpy`` into the search box. 
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



Installing JBidwatcher Companion
===============================================================================

There are several ways to install the program.

Easy
----

JBidwatcher Companion can be installed with the program **easy_install**,
which downloads the necessary package from the Pyhon Package Index
(http://pypi.python.org/pypi), and installs it.   

Get administrative privileges, then open a **shell window** / **DOS box** 
and type: ::

    easy_install jbidwatcher-companion

If you have already installed JBidwatcher Companion, you can upgrade to the 
latest version of by typing: ::

    easy_install -U jbidwatcher-companion

Classical
---------

The classical installation from sources is possible too.

    - Download a ``*.zip`` or ``*.tar.gz`` source archive/package from one of 
      the sites below:
        
      - https://launchpad.net/jbidwatcher-companion 
      - http://pypi.python.org/pypi?%3Aaction=search&term=JBidwatcher-Companion

    - Extract the contents of the archive.
    - Open a shell window / DOS box. 
    - Get administrator privileges.
    - Change to the folder that contains the archive's contents.
      (``JBidwatcher-Companion-*``). 
    - Type the following command: 
    
::
    
    python setup.py install

RPM
---------------

If you have an RPM based (Linux) system, you can click on a ``*.rpm`` package to 
install software. Currently only RPMs for my particular **openSuse** system
are built. They might work on other RPM based systems too. 

No Installation
---------------

The program consists only of the single file ``ebstat.py``, and therefore needs no 
installation to run. The file can be stored in any directory and run there.
To behave like a regular command, you must make the file executable, and 
put it into the path.

If you don't want to make the file executable, for example for a quick test, 
you can run it like so: ::

    python ebstat.py ls
    
For detailed usage instructions see section *Usage* below. 

To get the file download a source archive/package (``*.zip`` or ``*.tar.gz``)
from one of the sites below, and unpack it. 

    - https://launchpad.net/jbidwatcher-companion 
    - http://pypi.python.org/pypi?%3Aaction=search&term=JBidwatcher-Companion



Usage
===============================================================================

The program reads files from JBidwatcher in ``*.xml`` and ``*.csv`` format.
By default it reads ``~/.jbidwatcher/auctions.xml``, which is regularly updated 
by JBidwatcher (every 10 minutes).

Auctions can be selected for graphing based on two criteria: the tab where 
they reside (options ``-t``, ``-T``), and their comment (options ``-c``, ``-C``). 
The same criteria are also used to group the auctions into the lines of the 
diagram (option ``-g``). 


Command line
------------

::

    ebstat.py [gr] -t <tab name> [<options>]
    ebstat.py ls [<options>]

The program understands four commands: ``gr``, ``ls``, ``save-defaults`` and 
``clear-defaults``. If no command is given, ``gr`` is assumed.

``gr``, ``graph``
    Draw a time vs. price graph
    
``ls``             
    List the tabs, and show some minimal statistics.
    
``save-defaults``  
    Store the current options as default values for the ``gr`` command.
    
``clear-defaults`` 
    Remove the stored default values. 
    
    
Options
-------

  --version             Show program's version number and exit
  -h, --help            Show a help message and exit
  
  -t <tab name,...>, --include-tabs=<tab name,...>
                        Tabs that should be analyzed. Shell-style wildcards
                        can be used. For example ``"Nikon*"`` matches all names 
                        that start with "Nikon". 
                        Default: ``"*"`` (All tabs)
  -T <tab name,...>, --exclude-tabs=<tab name,...>
                        Tabs that should NOT be analyzed. Shell-style
                        wildcards can be used. 
                        Default: Exclude no auction.
  -c <comment name,...>, --include-comments=<comment name,...>
                        Comments that should be analyzed. Shell-style
                        wildcards can be used. 
                        Default: ``"*"``; (All comments)
  -C <comment name,...>, --exclude-comments=<comment name,...>
                        Comments that should NOT be analyzed. Shell-style
                        wildcards can be used. 
                        Default: Exclude no auction.
                        
  -u <column>, --analyze-column=<column>
                        Column that should be analyzed. 
                        Default: ``Total``
  -g <format string>, --group-auctions=<format string>
                        Group auctions into lines. 
                        
                        * ``t``: auctions from different tabs get into 
                          different lines
                        * ``c``: use comments to group auctions
                        * ``tc``: both criteria
                        * ``_``: all selected auctions get in one line. 
                            
                        Default: ``tc``
  -w <number of days>, --window=<number of days>
                        Length of the window for computing the moving median.
                        Default: 31
                        
  -i <file name>, --input-file=<file name>
                        Name of input file that contains price information.
                        Default: ``~/.jbidwatcher/auctions.xml``
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
  --double-click-command=<command>
                        Command that is executed when the user performs a
                        double click. The string ``{ID}`` is replaced by the
                        auction's Ebay ID.Default: (Start Firefox)
                        
                        ``firefox "http://cgi.ebay.de/ws/eBayISAPI.dll?ViewItem&item={ID}"`` 
                        

Graph Window
------------

The usage of the interactive graph window is mostly self explanatory. Some 
features however can't be discovered through the GUI. The most important
features are: 

* Clicking on an auction shows information about this auction in the bottom 
  right of the window. 
* Double clicking an auction runs an external program, which can be 
  configured. By default the auction is shown in Firefox.
* The buttons at the bottom of the window can be used to pan, zoom, and 
  save an image of the graph.
* Pressing the 'g' key switches a grid on and off.

A detailed description is in the documentation of Matplotlib:  

    http://matplotlib.sourceforge.net/users/navigation_toolbar.html


Examples
--------

List the tabs in ``~/.jbidwatcher/auctions.xml``: ::
    
    ebstat.py ls
    
Create a graph from the tab "Nikon SB": ::

    ebstat.py gr -t "Nikon SB"
    
Create a graph from all tabs that contain the word "Lens"; use only the 
comments to group auctions into lists; use a window of 50 days to compute the 
moving median: ::
    
    ebstat.py gr -t "*Lens*" -g c -w 50

Create a graph from a ``.csv`` file in the data directory; exclude auctions with 
the comments "SB 600" or "SB 800"; use a window of 50 days to compute the 
moving median. ::

    ebstat.py gr -i data/nikon-flash.csv -C "SB 600,SB 800" -w 50



Report Bugs and Ideas
===============================================================================

Bugs and feature requests (set importance to wishlist) can be reported on 
the development website:

    https://bugs.launchpad.net/jbidwatcher-companion

