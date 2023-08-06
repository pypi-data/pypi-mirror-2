############################################################################
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


Analysis program for prices on Ebay; for use in conjunction with JBidwatcher. 

The program creates price vs. time diagrams, with moving median price over a 
configurable period of time. It is a command line program, but the diagram is 
displayed in an interactive window. There the diagram can scaled, moved and 
saved as an image. 

Look at the example image `Nikon SB.png`.

The program reads files from JBidwatcher in ".xml" and ".csv" format.
By default it reads "~/.jbidwatcher/auctions.xml", which is regularly updated 
by JBidwatcher (every 10 minutes).

Auctions can be selected for graphing based on two criteria: the tab where 
they reside, and their comment. These same criteria are also used to group 
the auctions into lines that appear in the diagram. 

For information on JBidwatcher go to: http://www.jbidwatcher.com/',



Dependencies
------------

This program is written in the Python programming language, and needs a Python
interpreter to run. Additionally it uses two additional libraries: Numpy for 
numerical computations, and Matplotlib for the graph window.

Windows
.......

Python is usually not present on Windows. The most easy way for Windows 
users to install all dependencies is "Python XY" a (giant) Python distribution 
for scientists:

    http://www.pythonxy.com/

Linux
.....

Python is usually installed on all Linux distributions. Numpy and Matplotlib 
are usually not installed, but they are supplied by most distributions. 
To install these libraries, start your distribution's installation program, 
and search for Numpy and Matplotlib. Click the installation button. 

If you can't find Numpy and Matplotlib look at these (somewhat cryptic) 
directions:

     http://www.scipy.org/Installing_SciPy/Linux

Mac
...

Hm... ?
 


Installation
------------

This program consists only of the single file `ebstat.py`, and needs no 
installation. The file can be stored in any directory and run there. If used 
frequently `ebstat.py` should be made executable and put into the path.

If you don't want to make the file executable, for example for a quick test, 
you can run it like so:

    `python ebstat.py ls`
    
For detailed usage instructions see section "Usage" below. 

Download from here:

    http://bazaar.launchpad.net/~eike-welk/+junk/jbidwatcher-companion/files/head:/src/



Usage
-----

Command line:
.............

    `read_xml.py [graph] -t <tab name> [<options>]`
    `read_xml.py ls [<options>]`

The program understands two commands: "graph" and "ls". If no command is given,
"graph" is assumed.

* "graph", "gr" : Draw a time vs. price graph
* "ls"          : List the tabs, and show some minimal statistics.
    
    
Options:
........

  --version             show program's version number and exit
  -h, --help            show this help message and exit
  
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
                        column that should be analyzed. 
                        Default: "Total"
  -g <format string>, --group-auctions=<format string>
                        group auctions into lines. 
                            * "t": auctions from different tabs get into 
                              different lines
                            * "c": use comments to group auctions
                            * "tc": both criteria
                            * "_": all selected auctions get in one line. 
                        Default: "tc"
                        
  -i <file name>, --input-file=<file name>
                        name of input file that contains price information.
                        Default: "~/.jbidwatcher/auctions.xml"
  -o <file name>, --output-image=<file name>
                        store generated graph as (PNG) image in the current
                        directory. 
                        Default: do not store image.
                        
  -b, --batch           batch operation. Do not show any graph windows.
                        Default: False
  -l, --long-output     show more information. 
                        Default: False
  --title=<title string>
                        Title of the chart. 
                        Default: Program creates title.
  -w <number of days>, --window=<number of days>
                        length of the window for computing the moving median.
                        Default: 31


Examples:
.........

List the tabs in `~/.jbidwatcher/auctions.xml`:
    
    `./ebstat.py ls`
    
Create a graph from the tab "Nikon SB":

    `./ebstat.py gr -t "Nikon SB"`
    
Create a graph from all tabs that contain the word "Lens"; use only the 
comments to group auctions into lists; use a window of 50 days to compute the 
moving median:
    
    `./ebstat.py gr -t "*Lens*" -g c -w 50 `

Create a graph from a ".csv" file in the data directory; exclude auctions with 
the comments "SB 600" or "SB 800"; use a window of 50 days to compute the 
moving median. (Used to create the example image):

    `./ebstat.py gr -i ../data/nikon-flash.csv -C "SB 600,SB 800" -w 50`



Testing / Hacking
-----------------

The program is currently developed on Linux (Opensuse). Windows and Mac 
knowledge is very welcome! I use the IDE Eclipse and its extension Pydev. 
Bazaar is used for version control.

To get all development files type:

    `bzr branch lp:~eike-welk/+junk/jbidwatcher-companion`

Testing is done with the "py.test" framework. All tests are in the file 
`test_ebstat.py`. To run the tests: go to the `src` directory and type:

    `py.test`
    
The test framework will then (find and) run the tests. In case of any errors it
will create (overwhelmingly many) colored messages that point to the error. 
"py.test" is Unfortunately not integrated into Eclipse, therefore there are no
click-able error messages.

See:
    http://pytest.org/
    http://pydev.org/
    http://www.eclipse.org/
    http://bazaar.canonical.com/en/
