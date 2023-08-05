#!/usr/bin/python
#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________
#

# Stefan Chakerian schake@sandia.gov
# Sandia National Labs
# Dec 2007

# a note for the weak:
# On software, /usr/bin/python is the RHN version, and has mysql db module installed
# /usr/local/bin/python is a higher version of python, but DOES NOT have mysql
# Yeah, you're right.  It is messed up.



import xml
import commands
import shutil
import re
import math
import os
import sys
import glob
import string
import time
import datetime
import MySQLdb
import getopt

#os.sys.path = os.sys.path + ['../pyacro'] + ['../fast/pyacro'] + ['../fast/server'] + ['..']
from fast import exact
import fast_utils

# db connect string
dbconnect = MySQLdb.connect(read_default_file="/home/sqe/src/fast/server/dbload/pyload.dbinc",db="acro")

# defaults
verbose=0
quiet=0
dryrun=0
force=0
dosetup=0
checkdirs = []
xmlfiles=[]

# file types (determined by checking name of file) used for "file" artifacts.
# try  "log", "output", "study", "analysis", "results"
# then try just .xml, then use None if cannot be determined
# (see db table "file")
typelist = []
typelist.append((".log","log"))
typelist.append((".out","output"))
typelist.append(("study.xml","study"))
typelist.append(("analysis.xml","analysis"))
typelist.append(("results.xml","results"))
typelist.append((".xml","xml"))



def printhelp():
	print "Usage: %s -[q][f][n][s] [-v[v][v]] [-d dir [-d dir]...] [scenario.xml ...]" % sys.argv[0]
	print """\t-v\tverbose, multiples for increased verbosity
\t-d dir\tsearch dir for scenario.xml and its associated files
\t-n\tno updates: do not modify database (expect errors if making new entries)
\t-s\tsetup: interactive setup of existing project information in database
\t-q\tquiet: suppress extra messages (nyi)
\t-f\tforce updating database even if it looks like an error (nyi)
"""

def printver():
	print "%s (%s) version %s" % ("FAST db loader", "schake@sandia.gov", "1.0")


def runsql(c,sql,sqlvars=(),prefix=""):
	"""runsql used for modifying the database
	Checks variable dryrun to prevent updating"""

	if vvverbose or dryrun:
	  print prefix + sql % sqlvars
	if not dryrun:
	  c.execute(sql, sqlvars)


def setup():
	"""setup called with -s argument
	Edits extra fields in database, not derived from scenarios.
	Calling routine should probably exit afterward"""

	c=dbconnect.cursor()
	done = 0
	while 1:
	  sql="""SELECT package_id,name,fullname,version,contact,urlbase,urlhome FROM package"""
	  package = []
	  c.execute(sql)
	  row = c.fetchone()
	  while row is not None:
	    package.append(row)
	    row = c.fetchone()
	  s = "%-3.3s  %-10.10s %-15.15s %-6.6s %-12.12s %-20.20s %-30.30s"
	  vals = ("Id","Name","Fullname","Ver","Contact","URLbase","URLhome")
	  print s % vals
	  dash = "--------------------------------------------"
	  print s % (dash,dash,dash,dash,dash,dash,dash)
	  for i in range(len(package)):
	    p1 = package[i]
	    # str(i+1) on following line is to get 1..n, instead of 0..n-1
	    p2 = (str(i+1)+":",)+ tuple(p1[1:])
	    print s % p2
	  try:
	    r = int(raw_input("Enter a package Id to modify: "))
	  except (ValueError,KeyboardInterrupt):
	    r = 0
	  if r > 0 and r <= len(package):
	    mods = []
	    p = package[r-1]			# need the original 0..n-1 now, so subtract
	    newvals = []
	    print """Changing values for package %s""" % p[1]
	    print """Default/current value is in parentheses (use "None" to delete a field)"""
	    for i in range(len(vals[2:])):
	      try:
		line = raw_input("Enter %s (%s) " % (vals[i+2], p[i+2]))
		line = line.rstrip()
		line = line.lstrip()
	      except:
		print "aborted"
	        sys.exit()
	      if line is None or line == "":
		newvals.append(p[i+2])
	      elif line.lower() == "none" or line.lower() == "null":
		newvals.append(None)
	      else:
	        newvals.append(line)
	    sql="""UPDATE package SET fullname=%s, version=%s, contact=%s, urlbase=%s, urlhome=%s WHERE package_id = %s"""
	    newvals.append(str(p[0]))
	    sqlvars = tuple(newvals)
	    runsql(c, sql, sqlvars)
	  else:
	    break
	  
	
# tests look like: package-subpackage-param
# e.g. acro-gcov-nightly
# these are separated by '-'

def get_packageid(c,package):
	sql = """SELECT package_id FROM package WHERE name = %s"""
	c.execute(sql, (package,))
	result = c.fetchone()
	if result is not None:
	  return result[0] + 0
	return None

def get_subpackageid(c, pid, subpackage):
	sql = """SELECT subpackage_id FROM subpackage WHERE package_id = %s AND name = %s"""
	c.execute(sql, (pid, subpackage))
	result = c.fetchone()
	if result is not None:
	  return result[0] + 0
	return None

def get_paramid(c, spid, paramname):
	sql = """SELECT param_id FROM param WHERE subpackage_id = %s AND name = %s"""
	c.execute(sql, (spid, paramname))
	result = c.fetchone()
	if result is not None:
	  return result[0] + 0
	return None

def get_machineid(c, hostname, kernel_name, kernel_release=None,
		kernel_version=None, machine=None, processor=None, os=None):
	"""Get machineid
	Requires host and kernel name, but full list is better
	Returns (machine_id, hostversion)"""

	if hostname is None or kernel_name is None:
	  print "Fatal: getmachine: null name or null kernel"
	  sys.exit(1)
	if os is None or kernel_release is None or kernel_version is None or machine is None or processor is None:
	  sql = """SELECT machine_id,host_ver FROM machine WHERE host_name=%s AND kernel_name=%s ORDER BY host_ver DESC LIMIT 1"""
	  c.execute(sql, (hostname, kernel_name))
	  result = c.fetchone()
	else:
	  sql = """SELECT machine_id,host_ver FROM machine WHERE host_name=%s AND kernel_name=%s AND kernel_ver=%s AND OSstring=%s"""
	  c.execute(sql, (hostname,kernel_name,kernel_version,os))
	  result = c.fetchone()

	if result is None:
	  return (None,None)
	return result

def get_scenario_id(c,pid,spid,parid,mid,o):
	"""Find a scenario based on <Key> and start/endtimes"""
	sql="""SELECT scenario_id FROM scenario WHERE package_id=%s AND subpackage_id=%s AND param_id=%s AND machine_id=%s AND start_time=%s AND end_time=%s"""
	c.execute(sql,(pid,spid,parid,mid,o.start_time,o.end_time))
	result = c.fetchone()
	if result is not None:
	  return result[0]+0
	return result


def add_artifact_file(c, artid, ftype, f, url=None, link=None):
	"""add_artifact_file
	Forced insert a new record into file table"""

	if url is None:
	  # strip slashes
	  url = os.path.basename(f)
	if link is None:
	  start = f.rfind("#")
	  if start >= 0:
	    link = f[start+1:]
	  else:
	    link = os.path.basename(f)
	if artid is None:
	  print "Fatal: need to define artifact_id for add_artifact_file"
	  sys.exit()
# artid should be valid or badness happens
	sql="""INSERT INTO file (artifact_id,name,type,url,linkname) VALUES (%s,%s,%s,%s,%s)"""
	sqlvars=(artid, f, ftype, url, link)
	runsql(c, sql, sqlvars,"add file: ")
	return artid


def add_unique_artifact_file(c, artid, ftype, f, url=None, link=None):
	"""Checks if file exists, if not add it
	artid must be a valid "file" artifact_id"""

	# strip off any series of "./" at the beginning
	while f[0:2] == "./" and len(f) > 2:
	    f = f[2:]
	sql="""SELECT file_id FROM file INNER JOIN artifact USING (artifact_id) WHERE artifact.artifact_id=%s and file.name=%s"""
	sqlvar=(artid, f)
	numresult = c.execute(sql,sqlvar) 
	if numresult == 0:		# not found
	  add_artifact_file(c, artid, ftype, f, url, link)
	elif numresult > 1:	# found more than one
	  print "Fatal: multiple unique artifacts found, check db integrity"
	  print "debug:", "artid",artid,"file", "("+f+")"
	  result = c.fetchone()
	  while result is not None:
	    print result
	  sys.exit()
	else:			# found it, so do nothing
	  if vvverbose:
	    print "File", f, "already in db"


def get_artifact_id(c,sid,type):
	"""Find artifact_id based on (scenario_id,type)
	(should only find 1 of any type of config/build/file for any scenario)"""

	# NOTE if you ever SELECT on run_time, you have to worry about rounding errors
	sql="""SELECT artifact_id FROM artifact WHERE scenario_id=%s AND type=%s"""
	sqlvars=(sid,type)
	if vvverbose:
	  print "Get_artifact_id:", sql % sqlvars
	numresult = c.execute(sql, sqlvars)
	if numresult == 0:
	  return None
	elif numresult == 1:
	  result = c.fetchone()
	  return result[0]+0
	else:
	  print "Fatal: found duplicate artifacts"
	  result = c.fetchone()
	  while result is not None:
	    print result
	    result = c.fetchone()
	  sys.exit()


def add_artifact(c,sid, start_time,run_time,end_time,status,status_exec,type):
	"""Add new artifact
	Return: artifact_id"""

	sql="""INSERT INTO artifact (scenario_id,start_time,run_time,end_time,status,status_exec,type) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
	sqlvars=(sid, start_time, run_time, end_time, status, status_exec, type)
	runsql(c,sql,sqlvars, "> add artifact: ")
	artid = get_artifact_id(c, sid, type)
	if artid is None:
	  print "Fatal (add_artifact): no artifact_id after insert?"
	  print c,sid,start_time, run_time, status, type
	  sys.exit()
	return artid


def add_unique_artifact(c,sid,type, start_time=None, run_time=None, end_time=None,
			status=None, status_exec=None, file=None, log=None, flags=None, warnings=[]):
	"""Add artifact
	do not duplicate existing sid/type of artifact
	Return: artifact_id"""

	artid = get_artifact_id(c,sid,type)
	if artid is None:
	  artid=add_artifact(c,sid,start_time,run_time,end_time,status,status_exec,type)

    # check/add file (for build and config artifacts)
	# add files
	if file is not None:
	  # basefile is for the url ... get rid of the extra /paths/
	  # a null link will use everything after the last '#'
	  basefile = os.path.basename(file)
	  add_unique_artifact_file(c, artid, "xml", file, basefile)
	if log is not None:
	  basefile = os.path.basename(log)
	  # this is really a .out file, not a log
	  # currently in Exact, this is /a/local/file.out from the test machine,
	  # and wont be found on a webserver.  It is also added to the <files>
	  # section of the study, though.
	  add_unique_artifact_file(c, artid, "output", log, basefile)
	if flags:
	  add_unique_artifact_note(c, artid, "flag", flags)
	if len(warnings) > 0:
	  for w in warnings:
	    add_unique_artifact_note(c, artid, "warning", w)
	return artid


def add_artifact_note(c,artid,type,data):
	sql="""INSERT INTO artnote (artifact_id,type,data) VALUES (%s,%s,%s)"""
	sqlvars=(artid,type,data)
	runsql(c,sql,sqlvars)


def add_unique_artifact_note(c,artid,type,data):
	sql="""SELECT artnote_id FROM artnote WHERE artifact_id=%s AND type=%s AND data=%s"""
	sqlvar=(artid,type,data)
	numrows = c.execute(sql, sqlvar)
	if numrows == 0:
	  add_artifact_note(c,artid,type,data)

def get_study_id(c,sid,name):
	if not name:
	  print "Warning: get_study failed (null argument)", sid
	  return None
	sql="""SELECT study_id FROM study WHERE scenario_id=%s AND name=%s"""
	numrows = c.execute(sql, (sid,name))
	if numrows == 0:
	  return None
	row = c.fetchone()
	return row[0]+0

def add_study(c,sid,name):
	if not sid or not name:
	  print "Fatal: add_study failed (null argument)", sid, name
	  sys.exit(1)
	sql="""INSERT INTO study (scenario_id, name) VALUES (%s,%s)"""
	sqlvars = (sid,name)
	runsql(c,sql,sqlvars, "> add study:")
	study = get_study_id(c,sid,name)
	if study is None:
	  print "Fatal: get_study_id failed after insert"
	  sys.exit(1)
	return study


def get_test_id(c, aid, expname, comb):
	sql="""SELECT tstatus_id FROM tstatus WHERE analysis_id=%s AND experiment=%s AND comb=%s"""
	sqlvars = (aid, expname, comb)
	numrows = c.execute(sql, sqlvars)
	if numrows == 0:
	  return None
	row = c.fetchone()
	return row[0]+0

def add_unique_test(c, aid, testkey, comb, status):
	tid = get_test_id(c,aid, testkey, comb)
	if tid == None:
	  sql="""INSERT INTO tstatus (analysis_id, experiment, comb, status) VALUES (%s,%s,%s,%s)"""
	  if status:
	    s="Pass"
	  else:
	    s="Fail"
	  sqlvars = (aid, testkey, comb, s)
	  runsql(c,sql,sqlvars,"tstatus:")
	# return value will be None on an insert
	return tid

def get_analysis_id(c,study,name,type):
	if not study or not name:
	  print "Warning: get_analysis failed (null argument)", study, name
	  return None
	sql="""SELECT analysis_id FROM analysis WHERE study_id=%s AND type=%s AND name=%s"""
	numrows = c.execute(sql, (study,type,name))
	if numrows == 0:
	  return None
	row = c.fetchone()
	return row[0]+0


def add_analysis(c,study,name,type):
	if not study or not name or not type:
	  print "Fatal: add_analysis failed (null argument)", study, name, type
	  sys.exit(1)
	sql="""INSERT INTO analysis (study_id, name, type) VALUES (%s,%s,%s)"""
	sqlvars = (study,name,type)
	runsql(c,sql,sqlvars, "> add analysis:")
	analysis = get_analysis_id(c,study,name,type)
	if analysis is None:
	  print "Fatal: get_analysis_id failed after insert"
	  sys.exit(1)
	return analysis


def check_scenario(c, pid,spid,parid,mid,o):
	if o.start_time is None or o.start_time == "" or o.end_time is None or o.end_time == "":
	  return None
	s = get_scenario_id(c, pid,spid,parid,mid,o)
	if s is None:
	  sql="""INSERT INTO scenario (package_id,subpackage_id,param_id,machine_id,start_time,end_time) VALUES (%s,%s,%s,%s,%s,%s)"""
	  sqlvars=(pid,spid,parid,mid,o.start_time,o.end_time)
	  runsql(c,sql,sqlvars)
	s = get_scenario_id(c, pid,spid,parid,mid,o)
	return s


def check_key(c, o):
	"""Use ScenarioKey to find or add packages, subpackages, parameters,
	and also find/add machines.  Return (pid, spid, paramid, machineid)
	"""

# first check package, subpackage, params
	s = o.scenario.lower()
	if not len(s):
	  s="unknown-unknown"
	(package, subpackage) = s.split('-', 1)
	paramname = ""
	if subpackage.count('-') > 0:
	  (subpackage,paramname) = subpackage.split('-',1)
	if vverbose:
	  print "Package %s, subpackage %s, params %s" % (package, subpackage, paramname)

	pid = get_packageid(c,package)
	if pid is None:		# need to add to db
	  sql = """INSERT INTO package (name,fullname) VALUES (%s,%s)"""
	  runsql(c,sql,(package, package.title()))
	  pid = get_packageid(c,package)
	if vvverbose:
	  print "Package_ID =", pid

	spid = get_subpackageid(c,pid,subpackage)
	if spid is None:
	  sql = """INSERT INTO subpackage (package_id, name) VALUES (%s,%s)"""
	  runsql(c,sql,(pid, subpackage))
	  spid = get_subpackageid(c,pid,subpackage)
	if vvverbose:
	  print "Subpackage_ID =", spid

	paramid = get_paramid(c,spid,paramname)
	if paramid is None:
	  sql = """INSERT INTO param (subpackage_id, name) VALUES (%s,%s)"""
	  runsql(c,sql,(spid, paramname))
	  paramid = get_paramid(c,spid,paramname)
	if vvverbose:
	  print "Param_ID =", paramid

	if pid is None or spid is None or paramid is None:
	  print "Fatal: Package or subpackage not found and could not be added"
	  sys.exit(1)

# Find or add machine

	(mid,hver) = get_machineid(c, o.hostname, o.kernel_name, o.kernel_release,
		o.kernel_version, o.machine, o.processor, o.os)
	if mid is None:
	  (mid,hver) = get_machineid(c, o.hostname, o.kernel_name)
	  if mid is None:	# still not found, so do a full insert
	    sql = """INSERT INTO machine (host_name,kernel_name,kernel_rel,kernel_ver,machine,processor,OSstring) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
	    sqlvars = (o.hostname, o.kernel_name, o.kernel_release, o.kernel_version, o.machine, o.processor, o.os)
	    runsql(c, sql, sqlvars, "add machine: ")
	  else:			# found older version, so insert a new one
	    sql = """INSERT INTO machine (host_name,host_ver,kernel_name,kernel_rel,kernel_ver,machine,processor,OSstring) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
	    sqlvars= (o.hostname, str(hver+1), o.kernel_name, o.kernel_release, o.kernel_version, o.machine, o.processor, o.os)
	    runsql(c, sql, sqlvars, "machine +ver: ")
	  # search again... this time it better find it!
	  (mid,hver) = get_machineid(c, o.hostname, o.kernel_name, o.kernel_release,
		o.kernel_version, o.machine, o.processor, o.os)
        if vvverbose:
	  print "MachineID =", mid, "ver", hver

	return (pid,spid,paramid,mid)


#############    MAIN    ###########

# parse command line
try:
  opts, pargs = getopt.getopt(sys.argv[1:], 'Vvqfnhsd:')
except getopt.GetoptError,e:
  print e
  printhelp()
  sys.exit()

while len(opts) > 0:
  k,val = opts.pop()
  if (k == '-h'):
    printhelp()
    sys.exit()
  if (k == '-s'):
    dosetup=1
  elif (k == '-v'):
    verbose += 1
  elif (k == '-q'):
    quiet = 1
  elif (k == '-f'):
    force = 1
  elif (k == '-n'):
    dryrun = 1
  elif (k == '-V'):
    printver()
    sys.exit()
  elif (k == '-d'):
    checkdirs.append(val)

# verbosity levels: short info, print concepts, print data
vverbose=verbose > 1
vvverbose=verbose > 2

if dosetup:
  setup()
  sys.exit()

checkfiles = pargs
for d in checkdirs:
  if vverbose:
    print "Searching dir %s" % d
  checkfiles += (glob.glob(d + '/*scenario.xml'))

if len(checkfiles) == 0:
  printhelp()
  sys.exit()

for s in checkfiles:
  sf = os.path.basename(s)
  d = os.path.dirname(s)
  if d == "":
    d = "."
  if os.path.exists(d + '/' + sf):
    if vverbose:
      print "Found scenario %s in %s" % (sf, d)
    xmlfiles.append({"dir":d, "xml":sf})
  else:
    print "Warning: cannot find %s/%s ... skipping" % (d, sf)

if vvverbose:
  print xmlfiles

cwd = os.getcwd()
db = dbconnect.cursor()

for x in xmlfiles:
  dir = x["dir"]
  xml = x["xml"]

  # Have to look for local files where each scenario file is located
  os.chdir(dir)
  object = fast.FASTInterface(dir+'/'+xml, xml)
  
  if vvverbose:
    object.pprint("dump: ")

# check <Key> and add or find elements as necessary

  if object.key is None:
    print "Warning: no key in %s ... skipping" % xml
    continue
  else:
    (pid, spid, parid, mid) = check_key(db, object.key)

# check for existing scenario and add if not exist
  scenario = check_scenario(db, pid,spid,parid,mid,object)
  if scenario is None:
    print "Warning: missing start or endtime in %s - skipping..." % xml
    continue


# add in build/config info from object.config_info first
# these are also included in object.files, so don't load them twice
  skipfiles=[]
  if object.config_info is not None:
    oc = object.config_info
    if vvverbose:
      print "CONFIG INFO:", oc
    add_unique_artifact(db,scenario, "config",
		oc.start_time, oc.run_time, None, oc.integrity_status,
		oc.execution_status, oc.filename, oc.log_file, oc.flags, oc.warnings)
    # add_unique_artifact_file(db,artid,ftype,f)
    skipfiles += os.path.basename(oc.log_file)
    skipfiles += os.path.basename(oc.filename)
  if object.build_info is not None:
    oc = object.build_info
    if vvverbose:
      print "BUILD INFO:", oc
    add_unique_artifact(db,scenario, "build",
    		oc.start_time, oc.run_time, None, oc.integrity_status,
		oc.execution_status, oc.filename, oc.log_file, oc.flags, oc.warnings)
    skipfiles += os.path.basename(oc.log_file)
    skipfiles += os.path.basename(oc.filename)


  artid=get_artifact_id(db,scenario,"file")
  for f in object.files:
    if vvverbose:
      print "Checking file", f
# determine type to add based on filename (only way, unfortunately)
    ftype = None
    for t in typelist:
      if f.rfind(t[0]) >= 0:
        ftype=t[1]
	break
    if ftype is not None:
      if f not in skipfiles:
	if artid is None:
	  artid=add_unique_artifact(db,scenario,"file")
	add_unique_artifact_file(db,artid,ftype,f)
    else:
      print "Warning:", f, "has no type? ... skipping"

  for study in object.studies.keys():
    studyid = get_study_id(db, scenario, study)
    if studyid is None:
      studyid = add_study(db, scenario, study)

    for analysis in object.studies[study].analyses.keys():
      atype = object.studies[study].analyses[analysis]._type
      aid = get_analysis_id(db, studyid, analysis, atype)
      if aid is None:
        aid = add_analysis(db, studyid, analysis, atype)
      if vvverbose:
        object.studies[study].analyses[analysis].pprint(prefix="  ")
	print "num_tests(T/F)", object.studies[study].analyses[analysis].num_tests(True), object.studies[study].analyses[analysis].num_tests(False)
	print "test_status", object.studies[study].analyses[analysis].test_status
	o = object.studies[study].analyses[analysis]
	for testkey in o.test_status.keys():
	  for comb in o.test_status[testkey].keys():
	    add_unique_test(db, aid, testkey, comb, o.test_status[testkey][comb])
	  



#	print "results", object.studies[study].analyses[analysis].results

#   for e in object.studies[study].experiments.keys():
#     print "::::: study",study,object.studies[study].experiments[e].name
#     print object.studies[study].experiments[e].pprint("::::: ")


  # Directories can also be relative, so we have to reset to our starting
  # location before processing each scenario
  os.chdir(cwd)

