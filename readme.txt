SOSI to KML conversion Utility version 0.8
- - - - - - - - - - - - - - - - - - - - - -

sosi2kml imports a SOSI-file to a predefined database and exports the content to a Google kml-file upon request.


Information about SOSI is available on the Wikipedia:
 
 http://en.wikipedia.org/wiki/SOSI


The program has been built as part of internal work at the Norwegian Directorate for Nature Management by Ragnvald Larsen. Please report back bugs and suggestions for further development.

Ragnvald Larsen, Direktoratet for Naturforvaltning, mars 2008  til november 2011
                  Directorate for Nature Management, March 2008 to November 2011
                  NORWAY

The software was built in Python 2.6 and compiled using py2exe (see www.py2exe.org)
                 
The software is provided as is and comes with no warranties or moral/economical liability. This software is protected by the GPL: Gnu Public Licence

 GPL - http://www.gnu.org/copyleft/gpl.html
 



Todo
- - - - -

Although the program is currently functional there are still shortcomings:

* Consistent style handling
* Polygons:
    - Altitude for polygon coordinates
* Documentation is not good enough yet.
* Installer to handle the install process below.



Installing
- - - - - -

0. Unzip the sosi2kml_v0_5.zip-file to your system. 

1. Create the database using the script database.sql

2. Copy the code to your system

3. The following dll-files are necessary for running sosi2kml. Make sure 
   the files are in your system path:

   USER32.dll    - C:\WINDOWS\system32\USER32.dll
   SHELL32.dll   - C:\WINDOWS\system32\SHELL32.dll
   Secur32.dll   - C:\WINDOWS\system32\Secur32.dll
   ADVAPI32.dll  - C:\WINDOWS\system32\ADVAPI32.dll
   WS2_32.dll    - C:\WINDOWS\system32\WS2_32.dll
   KERNEL32.dll  - C:\WINDOWS\system32\KERNEL32.dll
   SHFOLDER.dll  - C:\WINDOWS\system32\SHFOLDER.dll

4. Update the path variable to point to the sosi2kml.exe file and the above mentioned dll-files.

5. Run the script according to the help text:
    
    sosi2kml.exe -h

    
Uninstalling
- - - - - -

Delete the distributions-folder and all it's contents.



Syntax
- - - - 

sosi2kml.exe -f [drive:][path][filename] -a [Action] -c [Colour]

[drive:][path][filename] Import SOSI file or Export KML-file.

[Action] 
    -a reset   Deletes all data stored in database.
    -a import  Import a specific SOSI file
    -a export  Exports a file to the current data directory.
    -a help    This information.

[Colour] 
    -c colour
                  
                  
usage: sosi2kml.py [options]

options:
  -h, --help            show this help message and exit

  -f FILE, --file=FILE  SOSI input file.

  -o FILE, --out=FILE   KML destination filename.

  -c COLOUR, --colour=COLOUR  	AABBGGRR explained this way:
                  		          AA: Alpha (opacity)
                  		          BB: Blue
                  		          GG: Green
                  		          RR: Red
                        Colour for kml-file objects. (-c AABBCC)

  -v, --verbose         Show status messages

  -i, --import          Import a SOSI-file to the database

  -e, --export          Export a SOSI file from the database

  -d, --dir             All .sos in the current directory

  -r, --reset           Delete all data from the database


  

Sample commands
- - - - - - - - -

Reset the database:

  sosi2kml.exe -r 

Import a file:

  sosi2kml.exe -f test_line.sos -i

Export a file to kml_
  
  sosi2kml.exe -f test_line.sos -e
    