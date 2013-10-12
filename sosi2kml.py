#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------------------
# This package is built using the following files:                    /
#                                                                     /
#  ->sosi2kml.py                                                      /
#    sosi2kml_lib.py                                                  /
#    sosi2kml.ini                                                     /
#    sosi2kml.sql                                                     /
#    readme.txt                                                       /
#                                                                     /
#                                                                     /
# sosi2kml imports a SOSI-file to a predefined database and exports   /
# the content to a kml-file upon request.                             /
#                                                                     /
# Information about SOSI is available on the Wikipedia:               /
#                  http://en.wikipedia.org/wiki/SOSI                  /
#                                                                     /
# Ragnvald Larsen, Direktoratet for Naturforvaltning, mars 2008       /
#                  Directorate for Nature Management, March 2008      /
#                  NORWAY                                             /
#                                                                     /
# This software is protected by the GPL: Gnu Public Licence           /
# GPL - http://www.gnu.org/copyleft/gpl.html                          /
#                                                                     /
# ---------------------------------------------------------------------
#                                                                     /
# ***** BEGIN GPL LICENSE BLOCK *****                                 /
#                                                                     /
# This program is free software; you can redistribute it and/or       /
# modify it under the terms of the GNU General Public License         /
# as published by the Free Software Foundation; either version 2      /
# of the License, or (at your option) any later version.              /
#                                                                     /
# This program is distributed in the hope that it will be useful,     /
# but WITHOUT ANY WARRANTY; without even the implied warranty of      /
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the       /
# GNU General Public License for more details.                        /
#                                                                     /
# You should have received a copy of the GNU General Public License   /
# along with this program; if not, write to the Free Software         /
# Foundation,                                                         /
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.     /
#                                                                     /
# ***** END GPL LICENCE BLOCK *****                                   /
#                                                                     /
#----------------------------------------------------------------------



#----------------------------------------------------------------------
# Imports necessary libraries
#
import os                            # Standard library 
import sys                           # Standard library 
import re                            # Standard library
import glob                          # Standard library 
import fileinput                     # Standard library 
import shutil                        # Standard library 
import fnmatch                       # Standard library
from   configobj import ConfigObj    # http://www.voidspace.org.uk/python/configobj.html
from   optparse  import OptionParser # Standard library for parsing of script options

import psycopg2                      # Psyco pg 2: www.initd.org/tracker/psycopg/wiki/PsycopgTwo

import sosi2kml_lib  as sosi         # functions library for this script


def main():

	#----------------------------------------------------------------------
	# Get ini-values from the sosi2kml-file
	#
	config = ConfigObj('sosi2kml.ini')

	db_host                = config['db_host']
	db_name                = config['db_name']
	db_user                = config['db_user']
	db_password            = config['db_password']

	styleDefaultColour         = config['styleDefaultColour']
	styleDefaultPolyColorMode  = config['styleDefaultPolyColorMode']
	styleDefaultPolyOutline    = config['styleDefaultPolyOutline']
	styleDefaultLineWidth      = config['styleDefaultLineWidth']
	styleDefaultLineColour     = config['styleDefaultLineColour']
	styleDefaultPointIcon      = config['styleDefaultPointIcon']
	styleDefaultPointColor     = config['styleDefaultPointColor']
	styleDefaultPointScale     = config['styleDefaultPointScale']
	startDir                   = config['startDir']
	destDir                    = config['destDir']


	#----------------------------------------------------------------------
	#
	# Get command line arguments from the option parser
	#
	parser = OptionParser()

	parser.add_option("-f", "--file",      action="store", type="string",           dest="sosiFilename",  help="SOSI input file.",       metavar="FILE")
	parser.add_option("-o", "--out",       action="store", type="string",           dest="kmldest",       help="KML destination filename.",  metavar="FILE")
	parser.add_option("-c", "--colour",    action="store", type="string",           dest="colour",        help="Colour for kml-file objects. (-c AABBCC)")
	parser.add_option("-v", "--verbose",   action="store_const", const=1,           dest="verbose",       help="Show status messages")
	parser.add_option("-w", "--what",      action="store_const", const="what",      dest="action",        help="More help is on the way. What more to ask for?")
	parser.add_option("-i", "--import",    action="store_const", const="import",    dest="action",        help="Import a SOSI-file to the database")
	parser.add_option("-e", "--export",    action="store_const", const="export",    dest="action",        help="Export a SOSI file from the database")
	parser.add_option("-d", "--dir",       action="store_const", const="directory", dest="action",        help="All .sos or .SOS in the current directory")
	parser.add_option("-m", "--mass",      action="store_const", const="mass",      dest="action",        help="Recursive directory copy and conversion")
	parser.add_option("-r", "--reset",     action="store_const", const="reset",     dest="action",        help="Delete all data from the database")

	(options, args) = parser.parse_args()

	if options.verbose:
		verbose = True
	else:
		verbose = False

	if (options.sosiFilename and (options.action != 'reset')):
		sosiFilename = options.sosiFilename

		if verbose:
			print "Source file      : %s" % (sosiFilename)

	else:
		abort = 1
		if verbose:
			abortmessage = "Error: No entry for SOSI file name."


	# Source file defined. kmldest default is set.
	if options.sosiFilename:
		sosistring =  options.sosiFilename
		tempname   =  sosistring.split('.')
		kmldest    =  tempname[0]


	# Destination file name given in options
	if options.kmldest:
		kmldest = options.kmldest


	# Print destination file name when the file is being exported
	if (verbose and (options.action != 'reset') and (options.action != 'directory') and (options.action != 'import') and (options.action != 'mass')):
		print "Destination file : %s.kml" % (kmldest)


	# Decides which action the script should take.
	if options.action:
		action = options.action

		if verbose:
			print "Action           : %s" % (action)

	else:
		abort = 1

		if verbose:
			abortmessage = "Error: Action for script not indicated."


	# Decides which action the script should take.
	if options.colour:
		stylePolyColour = options.colour
	else:
		stylePolyColour = styleDefaultColour


	if (verbose and ((options.action != 'reset') and  (options.action != 'import') and  (options.action != 'mass'))):
		print "Colour           : %s" % (stylePolyColour)


	# # # # # # # # # #
	#
	# Assign leftover variables unattended by options
	# Todo: Make sure the system checks which variables are unattended or not.
	#
	styleLineWidth        = styleDefaultLineWidth
	styleLineColour       = styleDefaultLineColour
	stylePolyColorMode    = styleDefaultPolyColorMode
	stylePolyOutline      = styleDefaultPolyOutline
	stylePointIcon        = styleDefaultPointIcon
	stylePointColor       = styleDefaultPointColor
	stylePointScale       = styleDefaultPointScale


	#----------------------------------------------------------------------
	# Open the database connection. Well aware of the limititations of the 
	# script and will place the data connection details in an .ini-file
	# at a later stage.

	connectString = "dbname=%s user=%s host=%s password=%s" % (db_name, db_user, db_host, db_password)

	conn = psycopg2.connect(connectString);

	cur = conn.cursor()


	# # # # # # # # # # 
	#
	# Make sure only recognizable SOSI elements can be read from the
	# SOSI-file. Not all elements are acted upon in this conversion
	# system, but it might come later. 
	#
	# To avoid problems with regards to norwegian characters (utf8)
	# and database connections such characters are stripped from 
	# the input file and replaced accordingly:
	#
	#       æ -> a   Æ -> A
	#       ø -> ø   Ø -> O
	#       å -> å   Å -> A
	#
	# The object list below is according to the stripping.
	#

	list_geoobj = ["PUNKT", "KURVE", "BUE", "TEKST", "SIRKELP", "SVERM", "KLOTOIDE", "BEZIER", "TRASE", "FLATE", "LINJE"]

	list_sniv1  = ["HODE", "DEF", "OBJDEF", "PUNKT", "KURVE", "BUE", "TEKST", "SIRKELP", "SVERM", "KLOTOIDE", "BEZIER", "TRASE", "FLATE", "SLUTT", "LINJE"]

	list_sniv2  = ["TEGNSETT", "TRANSPAR", "OMRADE", "SOSI-VERSJON", "SOSI-NIVA", "PRODUSENT", "EIER", "INNHOLD", "PROSESS_HISTORIE", "METADATALINK", "NO", "NOH", "N", "OBJTYPE", "REF", "KOMM", "ID_LOKAL", "FTEMA", "IID", "NAVN"]

	list_sniv3  = ["KVALITET", "KOORDSYS", "ENHET", "ORIGO-NO", "MIN-NO", "MAX-NO"]



	# # # # # # # # # #
	#
	# Import a file resident in the database
	#
	if options.action == "import":  

		#----------------------------------------------------------------------
		# Cleaning up the SOSI-file
		# 
		# Some SOSI files contain level three objects on a line with a higher
		# level object. In a context where we expect either one sosi object per
		# line or a coordinate this makes the later parsing messy. So - we will
		# clean it up before proceeding.



		# Open the original file and prepare a temporary file
		sosifile_in  = open(sosiFilename,'r')

		sosiTempname = "%s.tmp" % (sosiFilename)

		sosifile_tmp = open(sosiTempname,'w')


		# Traverse the file line by line 
		for fileLine in sosifile_in:

			# Avoid charset problems when sending data to the database.
			# At all costs! A workaround balancing the character encoding
			# is possible, bot not now.


			#fileLine=unicode(fileLine,'ISO-8859-1')

			if (re.search("\xe6",fileLine)):
				fileLine = fileLine.replace('\xe6','a')
				print fileLine

				if (re.search("\xc6",fileLine)):
					fileLine = fileLine.replace('\xc6','A')

			if (re.search("\xf8",fileLine)):
				fileLine = fileLine.replace('\xf8','o')

			if (re.search("\xd8",fileLine)):
				fileLine = fileLine.replace('\xd8','O')

			if (re.search('\xe5',fileLine)):
				fileLine = fileLine.replace("\xe5",'a')

			if (re.search("\xc5",fileLine)):
				fileLine = fileLine.replace("\xc5",'A')



			# Each SOSI object level indicator (../...)is replaced with SOSINL.. 
			# and SOSINL...  The line is then split into a list based on NL and 
			# written line by line to the file.

			if ((re.search(" \.\.\.",fileLine)) or (re.search(" \.\.",fileLine))):


				if (re.search(" \.\.\.[A-Z]",fileLine)):

					fileLine = fileLine.replace("...","SOSINL\n...")


				if (re.search(" \.\.[A-Z]",fileLine)):

					fileLine = fileLine.replace("..","SOSINL\n..")

				fileLine = fileLine.split('SOSINL')

				for fileLinesegment in fileLine:

					sosifile_tmp.write(fileLinesegment)	

			# No splitting of the line. Just write the line and proceed.
			else:
				sosifile_tmp.write(fileLine)


		sosifile_in.close()
		sosifile_tmp.close()

		#Insert file into the tbl_file
		fileid=sosi.insertFile(conn,cur,sosiFilename)



		#----------------------------------------------------------------------
		# Transfer the SOSI content to the database
		# 
		# The next step is to write the SOSI data into a database. The database
		# credentials are indicated earlier in this script. Database structure
		# is not indicated in this version of the script.
		# 
		# Insertion of SOSI-data into the database is based on SOSI levels and 
		# related information. The below script should be fairly easy to read.
		# Time has not allowed for writing this part in an object oriented way, 
		# so for the time being we are stuck with procedural way of hadling the
		# data.


		#----------------------------------------------------------------------
		# Open SOSI file
		fileHandle = open(sosiTempname,'r')

		# Read the file into a list - per line
		fileList = fileHandle.readlines()

		# The file is closed
		fileHandle.close()


		# Find the list length
		fileListLength = len(fileList)

		# Declare the variable
		cur_koordid = ""

		# The list is read one line at a time. The SOSI standard is hierarchical
		# where the notation of dots (.) indicates the level - except for when 
		# coordinates are indicated. A level two SOSI controll (..) will allways be 
		# owned by a level one (.) controll. A Level three SOSI controll (...) will
		# allways be owned by a level two (..) controll. Because of this keeping a
		# memory of the latest parent sosi level id we can use this to insert the
		# relevant id's in the relation tables.

		for fileLine in fileList:

			# Find out if this is a SOSI level one line.
			if (re.match("\.[A-Z]",fileLine)):
				# If so -  work on it
				cur_sniv1id = sosi.manageSniv1(conn, cur, fileLine, list_sniv1, list_geoobj)

				sosi.insertRelateFileSniv1(conn,cur,fileid,cur_sniv1id)

			elif(re.match("\.\.[A-Z]",fileLine)):
				# If so -  work on it
				cur_sniv2id = sosi.manageSniv2(conn, cur, fileLine, cur_sniv1id, list_sniv2)

			elif(re.match("\.\.\.[A-Z]",fileLine)):
				# If so -  work on it
				cur_Sniv3id = sosi.manageSniv3(conn, cur, fileLine, cur_sniv2id, cur_koordid, list_sniv3)

				# Nulls the value for te last coordinate as we are 
				# likely to get a new round of coordinates at this point.
				cur_koordid == ""

			elif (re.match("![a-zA-Z0-9!_]",fileLine)):
				# Exclamation marks (!) indicates a comment line. Ignored for now.
				invalid=0

			elif (re.match("[0-9\s0-9]",fileLine)):
				# A line with two numerals are a coordinate (XY). SOSI files with 
				# three coordinates (XYZ) are not covered in this version of sosi2kml

				cur_koordid = sosi.manageCoordinate(conn, cur, fileLine, cur_sniv1id)

			else:
				# All other instances are ignored.
				invalid=0


		#delete the .tmp-file
		os.unlink(sosiTempname)

		print "Status           : OK"


	# # # # # # # # # #
	#
	# Export a file resident in the database
	#
	elif options.action =="export":

		headVariable = sosi.getSosiHeadVariables(conn,cur,sosiFilename)

		# Traverse HEAD variables for information about UNIT 
		# and coordinate system (KOORDSYS)
		for variable in headVariable:

			if variable[1]=="ENHET":
				sosiUnit = float(variable[2])

			if variable[1]=="KOORDSYS":
				sosiUTM = variable[2]
				
			if variable[1]=="ORIGO-NO":
				add_north = variable[2]
				add_east  = variable[3]


		# Recoding UTM reference to proper UTM standard
		#COnditional value set due to usual mess in SOSIfiles
		#Some denote Zone 33 22 and some denote it 33. Zone 44
		#is far away...
		if int(sosiUTM)>30:
			sosiUTM = "%sN" % (int(sosiUTM))
		else:
			sosiUTM = "%sN" % (int(sosiUTM)+10)

		print sosiUTM


		# Initiating KML-file
		kmlFilename=  "%s.kml" % (kmldest)

		kmlFile_temp = open(kmlFilename,'w')

		strKmlHead_tmp = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"\
				          "<kml xmlns=\"http://earth.google.com/kml/2.2\">\n"\
				          "   <Document>\n"\
				          "        <Folder>\n"\
				          "             <name>%s</name>\n"\
				          "             <open>1</open>\n"\
				          "             <Style id=\"definedStyle\">\n"\
				          "                  <PolyStyle>\n"\
				          "                     <color>%s</color>\n"\
				          "                     <colorMode>%s</colorMode>\n"\
				          "                     <outline>%s</outline>\n"\
				          "                  </PolyStyle>\n"\
				          "                  <LineStyle>\n"\
				          "                     <color>%s</color>\n"\
				          "                     <width>%s</width>\n"\
				          "                     </LineStyle>\n"\
				          "                  <IconStyle>\n"\
				          "                     <Icon><href>%s</href></Icon>\n"\
				          "                     <color>%s</color>\n"\
				          "                     <scale>%s</scale>\n"\
				          "                  </IconStyle>\n"\
				          "              </Style>\n") % (kmlFilename,stylePolyColour,stylePolyColorMode,stylePolyOutline,styleLineColour,styleLineWidth,stylePointIcon,stylePointColor,stylePointScale)


		kmlFile_temp.write(strKmlHead_tmp)

		# Get a list of all geographical objects in a given SOSI file
		objectList = sosi.getObjectlist(conn,cur,sosiFilename)


		# Get a list of all top level object references. These are objects not being reference
		# themselves. Remember that polygons could be built up of more than one polygon
		# (multipolygons) and that a polygon could also be used to "cut a hole" in an 
		# outer polygon.
		# Todo: Does not handle multipolygons properly... FIXME
		for object in objectList:


			# Build a list of referenced objects for this file
			listeoverallReferencedObjects = sosi.allReferencedObjects(conn,cur,sosiFilename)	


			# Check if the current object is found in the list of referenced object.
			# If this is not so we are dealing with a main object which is build up
			# by sub-objects. This is what we are looking for!
			if object[2] not in listeoverallReferencedObjects:

				# Get object name
				objectName = sosi.getObjectName(conn,cur,object[0])


				# Get the object description
				objectContent = sosi.getObjectContent(conn,cur,object[0])

				description = "<table>"

				for linje in objectContent:
					description = "%s<tr><td>%s</td><td>%s</td></tr>" % (description,linje[0],linje[1])

				description = "%s</table>" % (description)


				contentRef = sosi.getReferenceObjectString(conn,cur,object[2])

				innerBoundarylist = []


				# Evaluate object type
				if object[1]=="FLATE":

					# Nested object is drawn
					if len(contentRef)>0:

						allHits = re.compile("\(.*?\)", re.I)

						parantesListe = allHits.findall(contentRef[0])

						restcontentRef = contentRef[0]	    

						# Find all sub-objects to be deleted from the main object
						for groupPart in parantesListe:

							# Strip characters from the main string
							restcontentRef = restcontentRef.replace(groupPart,"")

							referencePart  = groupPart.lstrip("\(")

							referencePart  = referencePart.rstrip("\)")

							referencePart  = referencePart.strip(":")

							innerCurveList = referencePart.split()

							# Make a list containing coordinates for the inner limits of an outer object
							innerBoundarylist.append(sosi.buildInnerBoundaryObject(conn,cur,innerCurveList,sosiUTM,sosiUnit,sosiFilename))

						innerBoundary = ""

						# Add the inner objects
						for polygonObjekt in innerBoundarylist:
							innerBoundary = "%s %s" % (innerBoundary, polygonObjekt)


						# Prepare outer polygon
						outerCurveList = restcontentRef.split()

						outerBoundary = sosi.buildOuterBoundaryObject(conn,cur,outerCurveList,sosiUTM,sosiUnit,sosiFilename)


						#Comment code for KML
						strKMLpolygon ="<Placemark>\n"\
							"    <name>%s</name>\n"\
							"    <description>%s</description>\n"\
							"    <styleUrl>#definedStyle</styleUrl>\n"\
							"    <Polygon>\n"\
							"        <altitudeMode>clampToGround</altitudeMode>\n"\
							"        <description>An example of BalloonStyle</description>\n"\
							"    %s\n"\
							"    %s\n"\
							"    </Polygon>\n"\
							"</Placemark>\n" % (objectName,description,outerBoundary,innerBoundary)

						kmlFile_temp.write(strKMLpolygon)


				# Export curve objects ("KURVE").
				elif object[1]=="KURVE":

					#Get a list of coordinates for the curve/line
					currentCurveList = sosi.getCoordinateList(conn,cur,object[2],sosiUTM,sosiUnit,sosiFilename)


					currentCurveString = ""

					# Iterate through the curve list and write them in the according KML format
					for row in currentCurveList:

						#If z value matters:
						#currentCurveString = "%s%s,%s,%s\n" % (currentCurveString,row[1],row[0],row[2])
						
						#Two dimensions only - for now.
						currentCurveString = "%s%s,%s,%s\n" % (currentCurveString,row[1],row[0],row[2])

					#Write KML code for a line placemark
					strKMLpolygon ="<Placemark>\n"\
						"    <name>%s</name>\n"\
						"    <description>%s</description>\n"\
						"    <styleUrl>#definedStyle</styleUrl>\n"\
						"    <LineString>\n"\
						"        <altitudeMode>relativeToGround</altitudeMode>\n"\
						"        <coordinates>%s</coordinates>\n"\
						"    </LineString>\n"\
						"</Placemark>\n" % (objectName,description,currentCurveString)

					kmlFile_temp.write(strKMLpolygon)


				# Export curve objects ("LINJE").
				elif object[1]=="LINJE":

					# et a list of coordinates for the curve/line
					currentCurveList = sosi.getCoordinateList(conn,cur,object[2],sosiUTM,sosiUnit,sosiFilename)


					currentCurveString = ""

					# Iterate through the curve list and write them in the according KML format
					for row in currentCurveList:

						#If z value matters:
						#currentCurveString = "%s%s,%s,%s\n" % (currentCurveString,row[1],row[0],row[2])
						
						#Two dimensions only - for now.
						currentCurveString = "%s%s,%s\n" % (currentCurveString,row[1],row[0])

					#Write KML code for a line placemark
					strKMLpolygon ="<Placemark>\n"\
						"    <name>%s</name>\n"\
						"    <description>%s</description>\n"\
						"    <styleUrl>#definedStyle</styleUrl>\n"\
						"    <LineString>\n"\
						"        <altitudeMode>relativeToGround</altitudeMode>\n"\
						"        <coordinates>%s</coordinates>\n"\
						"    </LineString>\n"\
						"</Placemark>\n" % (objectName,description,currentCurveString)

					kmlFile_temp.write(strKMLpolygon)


				# Export  point objects ("PUNKT").
				elif object[1]=="PUNKT":

					# Get the coordinates for the current point
					currentPoint = sosi.getCoordinateList(conn,cur,object[2], sosiUTM,sosiUnit,sosiFilename)

					currentPointString = "%s,%s,0\n" % (currentPoint[0][1],currentPoint[0][0])

					# Write KML code for a point placemark
					strKMLpolygon ="<Placemark>\n"\
						"    <name>%s</name>\n"\
						"    <description>%s</description>\n"\
						"    <styleUrl>#definedStyle</styleUrl>\n"\
						"    <Point>\n"\
						"        <altitudeMode>relativeToGround</altitudeMode>\n"\
						"        <coordinates>%s</coordinates>\n"\
						"    </Point>\n"\
						"</Placemark>\n" % (objectName,description,currentPointString)

					kmlFile_temp.write(strKMLpolygon)


		kmlFile_temp.write("</Folder>\n</Document>\n"\
				           "</kml>")

		kmlFile_temp.close()

		if verbose:
			print "Status           : OK"


	# # # # # # # # # #
	#
	# Directory converts all files in a particular directory
	#
	elif options.action =="directory":

		path = ''

		for infile in glob.glob( os.path.join(path, '*.sos') ):

			if verbose:
				print "Processing       : %s" % (infile)


			if sys.platform == 'linux2':
				os.system("python sosi2kml.py -r")
			else:
				os.system("sosi2kml.py -r")

			if sys.platform == 'linux2':
				executestring = "python sosi2kml.py -f %s -i" % (infile)
			else:
				executestring = "sosi2kml.py -f %s -i" % (infile)

			os.system(executestring)


			if sys.platform == 'linux2':
				executestring = "python sosi2kml.py -f %s -e" % (infile)
			else:
				executestring = "sosi2kml.py -f %s -e" % (infile)

			os.system(executestring)


		if verbose:
			print "Status           : OK"


	# # # # # # # # # #
	#
	# Mass recursive directory copy and conversion
	#
	elif options.action =="mass":

		#Consider code for deleting data in the destination directory


		if verbose:
			print "Copying files"

		#make a copy of the source directory to a destination directory folder
		dirList=os.listdir(startDir)

		for file1 in dirList: #file the files
			if fnmatch.fnmatch(file1, '*.sos') | fnmatch.fnmatch(file1, '*.SOS'): #make sure they match the wildcard
				shutil.copy(startDir+file1, destDir+'/'+file1) # move the files from origin to destination


		if verbose:
			print "Working on files."


		#Traverse through the destination directory (newly copied with all .sos files)
		for root, subdirs, files in os.walk(destDir):

			#for each file in the list of files
			for onefile in files:

				# Out for now. Gives user/log information overload.
				#if verbose:
					#print "Location: [%s][%s][%s]" % (root,destDir,onefile)

				#For each file process the file. Filepattern is of course .sos
				if fnmatch.fnmatch(onefile, '*.sos') | fnmatch.fnmatch(onefile, '*.SOS'):

					#get string to the sosi file being processed
					sosiSubject =os.path.join(root,onefile)

					if verbose:
						print "Preparing %s" % (onefile)

					# reset database
					if sys.platform == 'linux2':
						os.system("python sosi2kml.py -r")
					else:
						os.system("sosi2kml.py -r")

					if verbose:
						print "Emptied database"

					# convert file to KML
					if sys.platform == 'linux2':
						executestring = "python sosi2kml.py -f %s -i" % (sosiSubject)
					else:
						executestring = "sosi2kml.py -f %s -i" % (sosiSubject)

					os.system(executestring)


					#export the converted file
					if sys.platform == 'linux2':
						executestring = "python sosi2kml.py -f %s -e" % (sosiSubject)
					else:
						executestring = "sosi2kml.py -f %s -e" % (sosiSubject)

					os.system(executestring)


					#delete sosi file in destination folder 
					os.unlink(sosiSubject)


	# # # # # # # # # #
	#
	# Empties the current databse    
	#
	elif options.action =="reset":

		sosi.resetDatabase(conn,cur)

		if verbose:
			print "Status           : OK"


	# # # # # # # # # #
	#
	# Prints all options as described in the library function showHelp()
	# This is a hardly ever option. Added just for fun - because I
	# practically am GOD in this system. It's gotta be usefull for 
	# something...
	#
	elif options.action =="what":

		sosi.showHelp()


	# # # # # # # # # #
	#
	# None of the actions described were called. Print an error message.
	#
	else:

		if verbose:
			print "Status           : Error?"


# # # # # # # # # #
#
# Only run code if not included as a library
#
if __name__ == '__main__':
	main()