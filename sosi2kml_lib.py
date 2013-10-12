#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------------------
# This package is built using the following files:                    /
#                                                                     /
#    sosi2kml.py                                                      /
#  ->sosi2kml_lib.py                                                  /
#    sosi2kml.ini                                                     /
#    sosi2kml.sql                                                     /
#    readme.txt                                                       /
#                                                                     /
#                                                                     /
# sosi2kml imports a SOSI-file to a predefined database and exports   /
# the content to a kml-file upon request. This file contains the      /
# necessary libraries for the main program loop found in sosi2kml.py  /
#                                                                     /
# Information about SOSI is available on the Wikipedia:               /
#                  http://en.wikipedia.org/wiki/SOSI                  /
#                                                                     /
# Ragnvald Larsen, Direktoratet for Naturforvaltning, sept 2008       /
#                  Directorate for Nature Management, Sept 2008       /
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




# Import the conversion tool from UTM to Latitude/Longitude used in the
# function getCoordinateList. 
import LatLongUTMconversion    # http://pygps.org/#LatLongUTMconversion



#----------------------------------------------------------------------
# Functions related to database inserts
#
# D A T A B A S E
#
#----------------------------------------------------------------------



#----------------------------------------------------------------------
# Get a new id value from a sequence defined in the database
#
def new_seqid(f_dbConn,f_dbConnCursor):

	f_dbConnCursor.execute("select nextval('id_seq'::regclass)")

	return f_dbConnCursor.fetchone()[0]



#----------------------------------------------------------------------
# Resets the database completely removing all sosi data tables
#
def resetDatabase(f_dbConn,f_dbConnCursor):

	f_cur = f_dbConn.cursor()	

	f_cur.execute("DELETE from tbl_rel_sniv1_sniv2")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_rel_sniv2_sniv3")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_rel_geoobj_koordinat")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_rel_fil_sniv1")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_fil")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_koordinat")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_sniv1")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_sniv2")

	f_dbConn.commit()

	f_cur.execute("DELETE from tbl_sniv3")

	f_dbConn.commit()



#----------------------------------------------------------------------
# Adds the filename to tbl_fil and returns the id of the inserted file
#
def insertFile(f_dbConn,f_dbConnCursor,fileName):

	id_new = new_seqid(f_dbConn,f_dbConnCursor)

	f_dbConnCursor.execute("INSERT INTO tbl_fil (id, filnavn) VALUES (%s,'%s')" \
	                       % (id_new,fileName))

	f_dbConn.commit()

	return id_new



#----------------------------------------------------------------------
# Adds a connection between the file and a level 1 object
#
def insertRelateFileSniv1(f_dbConn,f_dbConnCursor,fileid,sniv1id):

	id_new = new_seqid(f_dbConn,f_dbConnCursor)

	f_dbConnCursor.execute("INSERT INTO tbl_rel_fil_sniv1 (ref_fil, ref_sniv1, rekkefolge) VALUES (%s,%s,%s)" \
	                       % (fileid, sniv1id,id_new))

	f_dbConn.commit()	

	return id_new



#----------------------------------------------------------------------
# Adds a coordinate for te correct object
#
def insertCoordinate(f_dbConn,f_dbConnCursor,x,y,z,objid):

	id_new = new_seqid(f_dbConn,f_dbConnCursor)

	f_cur = f_dbConn.cursor()	

	f_cur.execute("INSERT INTO tbl_koordinat (id,x,y,z) VALUES (%s,%s,%s,%s)" \
	              % (id_new,x,y,z))

	f_cur.execute("INSERT INTO tbl_rel_geoobj_koordinat (ref_geoobj,ref_koordinat,rekkefnr) VALUES (%s,%s,%s)" \
	              % (objid,id_new,id_new))

	f_dbConn.commit()	

	return id_new



#----------------------------------------------------------------------
# Objects on SOSI level 1 are added in a separate table
#
def insertSniv1(f_dbConn,f_dbConnCursor,sniv_kode,sniv_content):

	id_new = new_seqid(f_dbConn,f_dbConnCursor)

	f_dbConnCursor.execute("INSERT INTO tbl_sniv1 (id, main, content) VALUES (%s,'%s','%s')" \
	                       % (id_new,sniv_kode,sniv_content))

	f_dbConn.commit()	

	return id_new



#----------------------------------------------------------------------
# Relations between objects of SOSI level 1 and 2 are added. This 
# means an object on level 2 is effectively owned by a level 1 
# object - allways.
#
def insertrelSniv1Sniv2(f_dbConn,f_dbConnCursor,id_sniv1,id_sniv2):


	f_dbConnCursor.execute("INSERT INTO tbl_rel_sniv1_sniv2 (ref_sniv1, ref_sniv2) VALUES (%s,%s)" \
	                       % (id_sniv1,id_sniv2))

	f_dbConn.commit()



#----------------------------------------------------------------------
# Objects on SOSI level 2 are added in a separate table
#	
def insertSniv2(f_dbConn,f_dbConnCursor,sniv_kode,sniv_content):

	id_new = new_seqid(f_dbConn,f_dbConnCursor)

	f_dbConnCursor.execute("INSERT INTO tbl_sniv2 (id, main, content) VALUES (%s,'%s','%s')" \
	                       % (id_new,sniv_kode,sniv_content))

	f_dbConn.commit()	

	return id_new



#----------------------------------------------------------------------
# Relations between objects of SOSI level 2 and 3 are added. This 
# means an object on level 3 is effectively owned by a level 2 
# object - allways.
#
def insertrelSniv2Sniv3(f_dbConn,f_dbConnCursor,id_sniv2,id_sniv3):


	f_dbConnCursor.execute("INSERT INTO tbl_rel_sniv2_sniv3 (ref_sniv2, ref_sniv3) VALUES (%s,%s)" \
	                       % (id_sniv2,id_sniv3))

	f_dbConn.commit()



#----------------------------------------------------------------------
# Objects on SOSI level 3 are added in a separate table
#
def insertSniv3(f_dbConn,f_dbConnCursor,sniv_kode,sniv_content):

	id_new = new_seqid(f_dbConn,f_dbConnCursor)

	f_dbConnCursor.execute("INSERT INTO tbl_sniv3 (id, main, content) VALUES (%s,'%s','%s')" \
	                       % (id_new,sniv_kode,sniv_content))

	f_dbConn.commit()	

	return id_new



#----------------------------------------------------------------------
# Add KP data for a coordinate if such is defined. This introduces some
# redundancy to the table, but is necessary to retrieve the information
# at a later stage.
#
def getLastCoordinateKP(f_dbConn,f_dbConnCursor,cur_koordid,Koordniv):

	f_dbConnCursor.execute("UPDATE tbl_rel_geoobj_koordinat SET kp=%s WHERE ref_koordinat = %s" % (Koordniv,cur_koordid))

	f_dbConn.commit()



#----------------------------------------------------------------------
# Add KVALITET for a coordinate if such is defined. This introduces 
# some redundancy to the table, but is necessary to retrieve the 
# information at a later stage.
#
def getLastCoordinateKVALITET(f_dbConn,f_dbConnCursor,cur_koordid,kvalitet):

	f_dbConnCursor.execute("UPDATE tbl_rel_geoobj_koordinat SET kvalitet='%s' WHERE ref_koordinat = %s" % (kvalitet,cur_koordid))

	f_dbConn.commit()



#----------------------------------------------------------------------
# String handling functions
#
# S T R I N G S
#
#----------------------------------------------------------------------



#----------------------------------------------------------------------
# Reads a line identified as a SOSI level 1 line. The line is split up 
# and prepared for storage in the database.
#
def manageSniv1(conn,cur,fileLine,list_sniv1,list_geoobj):

	# Split the line using space as a separator
	splitfileLine = fileLine.split()

	# Count number of line parts
	numberofListObjects = len(splitfileLine)

	# Delete . in start of the line
	fileLine_0 = splitfileLine[0].lstrip('.')

	# If the line has more parts then add these
	if numberofListObjects>1:
		fileLine_1 = splitfileLine[1]
	else:
		fileLine_1 = ""

	# Find out if the first element is in the list of group types
	if fileLine_0 in list_sniv1:

		#Is this line of the "Gruppetyper"?
		if fileLine_0 in list_geoobj:


			fileLine_1 = fileLine_1.strip(':')

			# Database: insert a level 1 object
			id_svniv1 = insertSniv1(conn,cur, fileLine_0, fileLine_1)

			# Other objects are treated under one
		else:
			id_svniv1 = insertSniv1(conn,cur, fileLine_0, fileLine_1)

	else:
		id_svniv1=""

	# Returns an updated list
	return id_svniv1



#----------------------------------------------------------------------
# Reads a line identified as a SOSI level 2 line. The line is split up 
# and prepared for storage in the database.
#
def manageSniv2(conn,cur,fileLine,cur_sniv1id, list_sniv2):

	# Split the line using space as a separator
	splitfileLine = fileLine.split()

	# Count number of line parts
	numberofListObjects = len(splitfileLine)

	# Delete .. in start of the line
	fileLine_0 = splitfileLine[0].lstrip('..')

	# If the line has more parts then add these
	if numberofListObjects>1:
		fileLine_1 = splitfileLine[1]
	else:
		fileLine_1 = ""

	# Find out if the first element is in the list of group types
	if fileLine_0 in list_sniv2:

		if fileLine_0 == "NO":
			id_svniv2 = insertSniv2(conn,cur, fileLine_0, fileLine_1)

			insertrelSniv1Sniv2(conn,cur, cur_sniv1id, id_svniv2)	

		elif fileLine_0 == "NOH":
			id_svniv2 = insertSniv2(conn,cur, fileLine_0, fileLine_1)

			insertrelSniv1Sniv2(conn,cur, cur_sniv1id, id_svniv2)	

		elif fileLine_0 == "REF":

			refinfo =[]

			refinfostring = ""

			splitfileLine.pop(0)				

			for refinfo in splitfileLine:

				refinfostring += "%s " % (refinfo)

			id_svniv2 = insertSniv2(conn,cur, fileLine_0, refinfostring)

			insertrelSniv1Sniv2(conn,cur, cur_sniv1id, id_svniv2)			

		else:
			# Count parts of line 8split by space)
			countlineParts = len(splitfileLine)

			# Given many line elements these are drawn together to one string
			if (countlineParts > 1):
				splitfileLine.pop(0)

				lineRest = " ".join(splitfileLine)
			else:
				lineRest = ""

			id_svniv2 = insertSniv2(conn,cur, fileLine_0, lineRest)

			insertrelSniv1Sniv2(conn,cur, cur_sniv1id, id_svniv2)

	else:
		id_svniv2=""

	# Returns an updated list
	return id_svniv2



#----------------------------------------------------------------------
# Reads a line identified as a SOSI level 3 line. The line is split up 
# and prepared for storage in the database.
#
def manageSniv3(conn,cur,fileLine,cur_sniv2id,cur_koordid, list_sniv3):

	# Initializing variable
	id_svniv3 = ""	

	# Split the line using space as a separator
	splitfileLine = fileLine.split()

	# Count number of line parts
	numberofListObjects = len(splitfileLine)

	# Delete . in start of the line
	fileLine_0 = splitfileLine[0].lstrip('...')

	# If the line has more parts then add these
	if numberofListObjects>1:
		fileLine_1 = splitfileLine[1]
	else:
		fileLine_1 = ""


	# Find out if the first element is in the list of group types
	if fileLine_0 in list_sniv3:

		# Count number of line parts
		countlineParts = len(splitfileLine)

		# Given Dersom det er flere linjeelementer trekkes disse sammen til 
		# en streng med mellomrom
		if (countlineParts > 1):
			splitfileLine.pop(0)

			lineRest = " ".join(splitfileLine)

		else:
			lineRest = ""

		id_svniv3 = insertSniv3(conn,cur, fileLine_0, lineRest)	

		insertrelSniv2Sniv3(conn,cur,cur_sniv2id, id_svniv3)

		if fileLine_0 == "KP":

			getLastCoordinateKP(conn,cur,cur_koordid,lineRest)

		elif fileLine_0 == "KVALITET":

			getLastCoordinateKVALITET(conn,cur,cur_koordid,lineRest)

	else:
		id_svniv3 =""


	# Returns an updated list
	return id_svniv3



#----------------------------------------------------------------------
# A coordinate is read and added to the database whilst related to an
# object on level 1
#
def manageCoordinate(conn,cur,fileLine,sniv1id):

	# Split the line using space as separator (default in split funct)
	splitfileLine = fileLine.split()

	# Find number of objects in the list
	numberofListObjects = len(splitfileLine)


	# If the lines has more parts then add these
	if numberofListObjects == 2:

		x = splitfileLine[0]
		y = splitfileLine[1]
		z = 0

		coordId = insertCoordinate(conn,cur,x,y,z,sniv1id)

	# z-value is included
	elif numberofListObjects == 3:

		x = splitfileLine[0]
		y = splitfileLine[1]
		z = splitfileLine[2]

		coordId = insertCoordinate(conn,cur,x,y,z,sniv1id)

	else:
		coordId = ""

	# Returns an updated list
	return coordId




#----------------------------------------------------------------------
#
# G E N E R A L   F U N C T I O N S
#
#----------------------------------------------------------------------



#----------------------------------------------------------------------
#
# The function receives a list and returns the list without duplicates
#
def unique(s):

	n = len(s)
	if n == 0:
		return []

	# Try dict first
	u = {}
	try:
		for x in s:
			u[x] = 1
	except TypeError:
		del u  # Try next method
	else:
		return u.keys()

	# Sorts the list and continously removes duplicates
	try:
		t = list(s)
		t.sort()

	except TypeError:
		del t  # Try next method
	else:
		assert n > 0
		last = t[0]
		lasti = i = 1
		while i < n:
			if t[i] != last:
				t[lasti] = last = t[i]
				lasti += 1
			i += 1
		return t[:lasti]

	# New list is made. Goes through the list and adds the elements not
	# already in the new list
	u = []
	for x in s:
		if x not in u:
			u.append(x)
	return u




#----------------------------------------------------------------------
#
# G E O G R AP H I C A L    O P E R A T I O N S 
#
#----------------------------------------------------------------------



#----------------------------------------------------------------------
#
# The coordinate list i read and converted to lonlat before being 
# returned. Only UTM is currently supported.
#
def getCoordinateList(conn,cur, sniv1_id, sosiUTM,sosiUnit,sosiFilename):

	sortOrder =""

	if float(sniv1_id)<0:
		sortOrder = "ASC"

	# Query to read the coordinates into a list.
	cur.execute("SELECT public.tbl_koordinat.x, public.tbl_koordinat.y , public.tbl_koordinat.z \
				FROM  public.tbl_rel_fil_sniv1 \
	            INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_fil_sniv1.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_fil ON (public.tbl_rel_fil_sniv1.ref_fil=public.tbl_fil.id) \
	            INNER JOIN public.tbl_rel_geoobj_koordinat ON (public.tbl_rel_geoobj_koordinat.ref_geoobj=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_koordinat ON (public.tbl_rel_geoobj_koordinat.ref_koordinat=public.tbl_koordinat.id) \
	            WHERE ((public.tbl_sniv1.content = '%s') \
	            AND (public.tbl_fil.filnavn = '%s')) \
	            ORDER BY \
	            public.tbl_rel_geoobj_koordinat.rekkefnr %s " \
	            % (sniv1_id,sosiFilename,sortOrder))

	rows = cur.fetchall()

	#initiate
	koordliste = []

	for row in rows:

		# find integer value and establish unit
		y = int(row[0])
		y = y*sosiUnit

		# find integer value and establish unit
		x = int(row[1])
		x = x*sosiUnit

		# find integer value and establish unit
		if (row[2]):
			z = int(row[2])
			z = z*sosiUnit
		else:
			z=0

		(lat,lon) = LatLongUTMconversion.UTMtoLL(23, int(y), int(x), sosiUTM)

		koordliste.append ([lat,lon,z])

	return koordliste



#----------------------------------------------------------------------
#
# Get variables from the SOSI head
#
def getSosiHeadVariables(conn,cur,fileName):

	cur.execute("SELECT public.tbl_sniv3.id,  public.tbl_sniv3.main,  public.tbl_sniv3.content \
				FROM   public.tbl_rel_sniv2_sniv3 \
	            INNER JOIN public.tbl_sniv3 ON (public.tbl_rel_sniv2_sniv3.ref_sniv3=public.tbl_sniv3.id) \
	            INNER JOIN public.tbl_sniv2 ON (public.tbl_rel_sniv2_sniv3.ref_sniv2=public.tbl_sniv2.id) \
	            INNER JOIN public.tbl_rel_sniv1_sniv2 ON (public.tbl_rel_sniv1_sniv2.ref_sniv2=public.tbl_sniv2.id) \
	            INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_sniv1_sniv2.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_rel_fil_sniv1 ON (public.tbl_rel_fil_sniv1.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_fil ON (public.tbl_fil.id=public.tbl_rel_fil_sniv1.ref_fil) \
	            WHERE (public.tbl_sniv1.main = 'HODE') \
	            AND (public.tbl_fil.filnavn = '%s')" % (fileName))

	rows = cur.fetchall()

	variabelliste = []

	for row in rows:

		variabelliste.append ([row[0],row[1],row[2]])

	return variabelliste



#----------------------------------------------------------------------
#
# Returns a list of all SOSI level 1 objects bound to a file with a
# given name. Using the file name as a key is fine when we have no 
# duplicated file names. This should be handeled in a better way at a
# later stage using a search routine to find duplicate file names and 
# use this information to give the user alternatives.
#
def getObjectlist(conn,cur,filename):

	cur.execute("SELECT public.tbl_sniv1.id, \
				public.tbl_sniv1.main, \
				public.tbl_sniv1.content \
				FROM public.tbl_rel_fil_sniv1 \
	            INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_fil_sniv1.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_fil ON (public.tbl_rel_fil_sniv1.ref_fil=public.tbl_fil.id) \
	            INNER JOIN public.tbl_type_geoobj ON (public.tbl_type_geoobj.navn=public.tbl_sniv1.main) \
	            WHERE (public.tbl_fil.filnavn = '%s') \
	            ORDER BY public.tbl_sniv1.main, public.tbl_sniv1.content " % (filename))

	rows = cur.fetchall()

	objectlist = []

	for row in rows:

		objectlist.append ([row[0],row[1],row[2]])

	return objectlist



#----------------------------------------------------------------------
#
# Returns a string to be used as an object name
#
def getObjectName(conn,cur,objid):

	cur.execute("SELECT   public.tbl_sniv2.main,  public.tbl_sniv2.content \
				FROM \
public.tbl_rel_sniv1_sniv2 \
INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_sniv1_sniv2.ref_sniv1=public.tbl_sniv1.id) \
INNER JOIN public.tbl_sniv2 ON (public.tbl_rel_sniv1_sniv2.ref_sniv2=public.tbl_sniv2.id) \
WHERE \
(public.tbl_sniv2.main = 'NAVN' OR \
public.tbl_sniv2.main ='OBJTYPE') AND \
(public.tbl_sniv1.id = %s)" % (objid))

	rows = cur.fetchall()

	objectName = ""

	for row in rows:

		if row[0] == "NAVN":
			objectName = "%s%s " % (objectName,row[1])

		elif row[0] == "OBJTYPE":
			objectName = "%s%s" % (objectName,row[1])

	return objectName	    



#----------------------------------------------------------------------
#
# Returns a string to be used as a name on the object.
#
def getObjectContent(conn,cur,objid):

	cur.execute("SELECT   public.tbl_sniv2.main,  public.tbl_sniv2.content \
				FROM \
	            public.tbl_rel_sniv1_sniv2 \
	            INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_sniv1_sniv2.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_sniv2 ON (public.tbl_rel_sniv1_sniv2.ref_sniv2=public.tbl_sniv2.id) \
	            WHERE \
	            (public.tbl_sniv2.main = 'IID' OR \
	            public.tbl_sniv2.main = 'ID_LOKAL' OR \
	            public.tbl_sniv2.main = 'KOMM' OR \
	            public.tbl_sniv2.main = 'FTEMA') AND \
	            (public.tbl_sniv1.id = %s)" % (objid))

	rows = cur.fetchall()

	objectList = []

	for row in rows:

		objectList.append ([row[0],row[1]])

	return objectList	



#----------------------------------------------------------------------
#
# Builds a list of attributes for a given object (level 1) and sub-
# sequently returns it as an array.
# 
def getAttributeList(conn,cur,sniv1_id):

	cur.execute("SELECT   public.tbl_sniv2.id,  public.tbl_sniv2.main,  public.tbl_sniv2.content \
				FROM public.tbl_rel_sniv1_sniv2 \
	            INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_sniv1_sniv2.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_sniv2 ON (public.tbl_rel_sniv1_sniv2.ref_sniv2=public.tbl_sniv2.id) \
	            WHERE (public.tbl_sniv1.id = %s)" % (sniv1_id))

	rows = cur.fetchall()

	attributelist = []

	for row in rows:

		attributelist.append ([row[0],row[1],row[2]])

	return attributelist



#----------------------------------------------------------------------
# Gets a REF string for a given SOSI level 1 object.
# 
def getReferenceObjectString(conn,cur,objectReference):

	cur.execute("SELECT public.tbl_sniv2.content \
				FROM public.tbl_rel_sniv1_sniv2 \
INNER JOIN public.tbl_sniv2 ON (public.tbl_rel_sniv1_sniv2.ref_sniv2=public.tbl_sniv2.id) \
INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_sniv1_sniv2.ref_sniv1=public.tbl_sniv1.id) \
WHERE \
(public.tbl_sniv2.main = 'REF') AND \
(public.tbl_sniv1.content = '%s')" % (objectReference))

	rows = cur.fetchall()

	reference = []

	for row in rows:

		reference.append (row[0])

	return reference



#----------------------------------------------------------------------
#
# Returns a list of all objects referred from some other object in the
# SOPSI-file.
#
def allReferencedObjects(conn,cur,fileName):

	cur.execute("SELECT public.tbl_sniv2.content \
				FROM public.tbl_rel_sniv1_sniv2 \
	            INNER JOIN public.tbl_sniv2 ON (public.tbl_rel_sniv1_sniv2.ref_sniv2=public.tbl_sniv2.id) \
	            INNER JOIN public.tbl_sniv1 ON (public.tbl_rel_sniv1_sniv2.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_rel_fil_sniv1 ON (public.tbl_rel_fil_sniv1.ref_sniv1=public.tbl_sniv1.id) \
	            INNER JOIN public.tbl_fil ON (public.tbl_fil.id=public.tbl_rel_fil_sniv1.ref_fil) \
	            WHERE public.tbl_sniv2.main = 'REF' AND \
	            (public.tbl_fil.filnavn = '%s')" % (fileName))

	rows = cur.fetchall()

	referanse = []

	for row in rows:

		referenceList =row[0]

		# Remove string parts: ( and )
		referenceList = referenceList.replace("(","")
		referenceList = referenceList.replace(")","")

		# Remove string parts: -
		referenceList = referenceList.replace("-","")

		# Remove string parts: :
		referenceList = referenceList.replace(":","")

		# Split()
		referenceList = referenceList.split()

		for subrow in referenceList:
			referanse.append (subrow)


	# Remove duplicates
	referanse = unique(referanse)

	referanse.sort()

	return referanse



#----------------------------------------------------------------------
#
# A list of coordinates is rewritten in KML style
#
def returnerKMLpolygon(coordinateList):	

	strKMLpolygon = ""

	for row in coordinateList:

		strKMLpolygon = "%s%s,%s,0\n" % (strKMLpolygon,row[1],row[0])

	return strKMLpolygon



#----------------------------------------------------------------------
#
# The functin receives a list of curces and serves to build inner
# polygons to be deducted from the outer polygon.
#
def buildInnerBoundaryObject(conn,cur,curveList,sosiUTM,sosiUnit,sosiFilename):

	for curveObject in curveList:

		coordinateString =  ""

		curveReference = curveObject

		polygonString = returnerKMLpolygon(getCoordinateList(conn,cur,curveReference, sosiUTM,sosiUnit,sosiFilename))

		coordinateString =  "%s %s" % (coordinateString,polygonString)

	strInnerBoundary ="        <innerBoundaryIs>\n"\
	    "        <LinearRing>\n"\
	    "            <coordinates>\n"\
	    "                %s\n"\
	    "            </coordinates>\n"\
	    "        </LinearRing>\n" \
	    "         </innerBoundaryIs>\n" % (coordinateString)

	return strInnerBoundary



#----------------------------------------------------------------------
#
# The functin receives a list of curves and serves to build the outer 
# polygon.
#
def buildOuterBoundaryObject(conn,cur,curveList,sosiUTM,sosiUnit,sosiFilename):

	coordinateString =  ""

	for curveObject in curveList:

		curveReference = curveObject

		curveReference = curveReference.strip(":")

		polygonString = returnerKMLpolygon(getCoordinateList(conn,cur,curveReference, sosiUTM,sosiUnit,sosiFilename))

		coordinateString =  "%s %s" % (coordinateString,polygonString)

	strOuterBoundary ="        <outerBoundaryIs>\n"\
	    "        <LinearRing>\n"\
	    "            <coordinates>\n"\
	    "                %s\n"\
	    "            </coordinates>\n"\
	    "        </LinearRing>\n"\
	    "        </outerBoundaryIs>\n"	 % (coordinateString)

	return strOuterBoundary



#----------------------------------------------------------------------
#
# Help text
#
def showHelp():
	print '''NAME
SOSI to KML conversion Utility version 0.9

FILE
     sosi2kml.exe

LICENSE
     GNU GPL

DESCRIPTION
     The program imports a SOSI version 4 file to a database
     and allows exports of the data to a KML-file.

     Sosi2kml puts all data into a PostgreSQL non spatial data-
     base and exports the data to a kml-file upon request.

     The program has been built as part of internal work at the
     Norwegian Directorate for Nature Management by Ragnvald
     Larsen. Please report back bugs and suggestions for further
     development.

     The software was built in Python 2.4 and compiled using py2exe
     (see www.py2exe.org)

     The software is provided as is and comes with no warranties
     or economical liability.

SYNTAX
     sosi2kml.exe -f [drive:][path][filename] -a [Action] -c [Colour]

     [Options]
								-r         Deletes all data stored in 
                                           database.
								-i         Import a specific SOSI file 
								-e         Exports a file to the current 
                                           directory. 
								-d         Converts all files in described 
                                           directory. 
								-m         Mass conversion of all files in
                                           a directory.
								-h         This information.
								-v         Write messages indicating progress.
								-c colour  AABBGGRR explained this way:
                                           AA: Alpha (opacity)
                                           BB: Blue
                                           GG: Green
                                           RR: Red

	The switches may be thrown in any order.

EXAMPLES
    A precondition for using the sosi2kml utility is that the 
    system is set up to communicate with a PostgreSQL database.
    Once this is done you may use the following commands to 
    convert files:

	sosi2kml.py -f yourfile.sos -i -v
	(imports yourfile.sos and prints progress)

	sosi2kml.py -f yourfile.sos -e -v
	(eksports yourfile.sos and prints progress)

	sosi2kml.py -r
	(resets the database and removes all former data)


	'''

