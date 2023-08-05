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
# commit_summary - Summarize a repository commit history
#

import datetime
import sys
import commands
import time
from optparse import OptionParser
import fast
import pyutilib.misc
from pyutilib.misc import Bunch

debug=False

#
# Returns a datetime object for a given revision
#
def get_date(rev,reposdir):
  tmp_date = commands.getoutput("svnlook date -r " + `rev` + " " + reposdir)
  #print "W HERE",tmp_date
  s = "T".join( tmp_date.split(" ")[0:2] )
  #print "X HERE",s
  #foo = time.strptime(s, "%Y-%m-%dT%H:%M:%S")[0:6]
  #print "Y HERE",foo
  return datetime.datetime(*time.strptime(s, "%Y-%m-%dT%H:%M:%S")[0:6])

#
# Generate a list of time periods
#
def get_periods(reposdir,nperiods,dpp):
  #
  # Terminate if we can't get the youngest revision
  #
  periods = []
  (status,text) = commands.getstatusoutput("svnlook youngest " + reposdir)
  if status != 0:
     return periods
  #
  # Iteration counters
  #
  ## initial revision
  start_rev = eval(text)
  ## initial time
  start_time = datetime.datetime.now()
  ## current revision
  curr_rev = start_rev
  ## current time
  rev_time = get_date(curr_rev,reposdir)
  ## time after 'p' periods
  curr_time = start_time
  ## period counter
  period=1
  ## day counter
  day=1
  #
  # Iterate...
  #
  while True:
    #
    # The current revision for may not be in the next time period.  Add empty
    # periods until the current revision is in the next time period.
    #
    delta = start_time - rev_time
    #print "Iter:",(day+dpp),delta.days
    while (day+dpp-1) <= delta.days:
      periods.append( Bunch(period=period,day=day,curr_time=curr_time,curr_rev=None,rev_time=None,last_rev=None) )
      if debug:
         print "APPEND 1",period,day,curr_time,None,None
      period = period+1
      day = day+dpp
      curr_time = start_time + datetime.timedelta(-day+1)
      delta = start_time - rev_time
      #print "HERE",(day+dpp),delta.days
    #
    # Terminate the loop if we have enough periods, or if we're at the first revision
    # in the subversion repository.
    #
    # Note: this while loop can generate more than nperiod periods if there is a long stretch of
    # periods with no revisions.  However, this is necessary to get the 'last revision' in 
    # each period.
    #
    #print "X",period,curr_rev
    if period > nperiods or curr_rev == 1:
       break
    #
    # Bracket the next revision
    #
    offset=1
    while True:
      delta = curr_time - get_date(curr_rev-offset,reposdir)
      if delta.days >= dpp:
         break
      offset = offset*2
      if curr_rev-offset < 1:
         offset = curr_rev-1
         break
    #print "Y",period,curr_rev
    #
    # Check if we have reached the beginning of the repository...
    #
    if curr_rev-offset == 1:
       delta = curr_time - get_date(curr_rev-offset,reposdir)
       if delta.days < dpp:
          if debug:
                print "APPEND 3",period,day,curr_time,curr_rev,rev_time
          periods.append( Bunch(period=period,day=day,curr_time=curr_time,curr_rev=curr_rev,rev_time=rev_time,last_rev=1) )
          break
    #
    # Now use a binary search to find the offset that represents the
    # beginning of the next period
    #
    #print "Z",period,curr_rev
    tmp_rev = curr_rev
    while offset > 1:
      tmp_offset=offset/2
      delta = curr_time - get_date(tmp_rev-tmp_offset,reposdir)
      if debug:
         print "BinarySearch:", tmp_offset,tmp_rev-offset, get_date(tmp_rev-offset,reposdir), get_date(tmp_rev-tmp_offset,reposdir), get_date(tmp_rev,reposdir),curr_time,offset,tmp_rev-tmp_offset,tmp_rev,curr_rev,delta.days,dpp
      if delta.days >= dpp:
         offset=tmp_offset
      else:
         offset_rev=tmp_rev-offset
         tmp_rev = tmp_rev-tmp_offset
         offset = tmp_rev - offset_rev
      if debug:
         print "OFFSET",offset
    #
    # Add the current period
    #
    periods.append( Bunch(period=period,day=day,curr_time=curr_time,curr_rev=curr_rev,rev_time=rev_time,last_rev=tmp_rev-offset+1) )
    if debug:
       print "APPEND 2",period,day,curr_time,curr_rev,rev_time
    period = period+1
    day = day+dpp
    curr_time = start_time + datetime.timedelta(-day+1)
    #
    # Set the new revision number for the next period
    #
    curr_rev = tmp_rev-offset
    rev_time = get_date(curr_rev,reposdir)
    if debug:
        print "Iteration:"
        print " Day:  ",day
        print " CTime:",curr_time
        print " CRev: ",curr_rev
        print " CTime:",rev_time
        
  #
  # Debugging output
  #
  if debug:
     print ""
     print "  SUMMARIZING"
     for period in periods:
       print ""
       print "Period      ",period.period
       print "Day         ",period.day
       print "Period Date ",period.curr_time
       print "Rev         ",period.curr_rev
       print "Rev Date    ",period.rev_time
       print "Last Rev    ",period.last_rev
       if period.last_rev is not None:
          print "LastRev Date",get_date(period.last_rev,reposdir)
       if period.curr_rev is not None and period.curr_rev != start_rev:
          tmp = get_date(period.curr_rev+1,reposdir)
          print "PrevRev Date",tmp
  #
  # Return the list of periods
  #
  return periods

#
# Summarize the commit and change history for nperiods that have length dpp
#
def summarize(reposdir,nperiods,dpp,format):
  period_info = get_periods(reposdir,nperiods,dpp)
  if len(period_info)==0:
     print "ERROR processing",reposdir
     return
  #
  # Collect statistics
  #
  authors = set()
  stats = []
  periods=[]
  i=0
  for period in period_info:
    commits={}
    changes={}
    rev=period.curr_rev
    if rev is not None:
       #print "HERE",rev,period.last_rev
       while rev >= period.last_rev:
         author = commands.getoutput("svnlook author -r " + `rev` + " " + reposdir)
         if author=="":
            author="unknown"
         authors.add(author)
         changed = commands.getoutput("svnlook changed -r " + `rev` + " " + reposdir)
         if author not in commits.keys():
            commits[author] = 1
            changes[author] = len(changed.split("\n"))
         else:
            commits[author] = commits[author]+1
            changes[author] = changes[author]+len(changed.split("\n"))
         rev=rev-1
       stats.append( (commits,changes) )
       periods.append( period )
    else:
       stats.append( ({},{}) )
    i=i+1
    if len(periods)>=nperiods:
       break
  if len(periods) > nperiods:
    print "Error: expected at most "+str(nperiods)+" periods"
    sys.exit(1)
  ##print "HERE",stats,nperiods,len(periods)
  #
  # Generate output
  #
  author_list = list(authors)
  author_list.sort()
  if format=="text":
     flag=False
     i=0
     if min(nperiods,len(periods)) == 0:
        print "No commits"
        return
     while i < min(nperiods,len(periods)):
       ncommits=0
       nchanges=0
       if periods[i].curr_rev is not None:
          for author in author_list:
            if author in stats[i][0].keys():
               ncommits=ncommits + stats[i][0][author]
          for author in author_list:
            if author in stats[i][1].keys():
               nchanges=nchanges + stats[i][1][author]
       if i>0:
           print ".................................."
       print "Period      ",periods[i].period
       print "Period Date ",periods[i].curr_time
       print "Rev         ",periods[i].curr_rev
       if periods[i].curr_rev is not None:
           print "Rev Date    ",periods[i].rev_time
       print "Last Rev    ",periods[i].last_rev
       if periods[i].last_rev is not None:
           print "LastRev Date",get_date(periods[i].last_rev,reposdir)
       print "Num Commits ",ncommits
       print "Num Changes ",nchanges
       if periods[i].curr_rev is not None:
           print "Commits by Author"
       for author in author_list:
           if author in stats[i][0].keys():
               val = stats[i][0][author]
           else:
               val = 0
           print "  %-15s %8d" % (author,val)
       print "Changes by Author"
       for author in author_list:
           if author in stats[i][1].keys():
               val = stats[i][1][author]
           else:
               val = 0
           print "  %-15s %8d" % (author,val)
       print ""
       i = i+1

  elif format=="xml":
     i=0
     while i< min(nperiods,len(periods)):
       print "    <Period>"
       print "      <PeriodNum>%d</PeriodNum>" % (periods[i].period)
       print "      <PeriodDate>%s</PeriodDate>" % (periods[i].curr_time)
       print "      <FirstRevisionNum>%s</FirstRevisionNum>" % (`periods[i].curr_rev`)
       if periods[i].curr_rev is not None:
          print "      <FirstRevisionDate>%s</FirstRevisionDate>" % (periods[i].rev_time)
       print "      <LastRevisionNum>%s</LastRevisionNum>" % (`periods[i].last_rev`)
       if periods[i].last_rev is not None:
          print "      <LastRevisionDate>%s</LastRevisionDate>" % (get_date(periods[i].last_rev,reposdir))
       ncommits=0
       nchanges=0
       if periods[i].curr_rev is not None:
          for author in author_list:
            if author in stats[i][0].keys():
               ncommits=ncommits + stats[i][0][author]
          for author in author_list:
            if author in stats[i][1].keys():
               nchanges=nchanges + stats[i][1][author]
       print "      <NumCommits>%d</NumCommits>" % (ncommits)
       print "      <NumChanges>%d</NumChanges>" % (nchanges)
       if periods[i].curr_rev is not None:
          for author in author_list:
            if author in stats[i][0].keys():
               val = stats[i][0][author]
            else:
               val = 0
            print "      <Commits author=\"%s\">%d</Commits>" %(author,val)
          for author in author_list:
            if author in stats[i][1].keys():
               val = stats[i][1][author]
            else:
               val = 0
            print "      <Changes author=\"%s\">%d</Changes>" %(author,val)
       print "    </Period>"
       i = i+1


def main_summarize(reposdir, options, format):
    if format=="xml":
        print "<SVNCommitSummary>"
        print "  <Repository>%s</Repository>" % (reposdir)
    #
    # Summarize commits for the last ndays
    #
    if options.ndays > 0:
        if format=="xml":
            print "  <DailyStatistics>"
        else:
            print ""
            print "---------------------------------"
            print "       Daily Statistics"
            print "---------------------------------"
            print ""
        summarize(reposdir,options.ndays,1,format)
        if format=="xml":
            print "  </DailyStatistics>"
    #
    # Summarize commits for the last nweeks
    #
    if options.nweeks > 0:
        if format=="xml":
            print "  <WeeklyStatistics>"
        else:
            print ""
            print "---------------------------------"
            print "       Weekly Statistics"
            print "---------------------------------"
            print ""
        summarize(reposdir,options.nweeks,7,format)
        if format=="xml":
            print "  </WeeklyStatistics>"
    #
    # Summarize commits for the last nmonths
    #
    if options.nmonths > 0:
        if format=="xml":
            print "  <MonthlyStatistics>"
        else:
            print ""
            print "---------------------------------"
            print "       Monthly Statistics"
            print "---------------------------------"
            print ""
        summarize(reposdir,options.nmonths,30,format)
        if format=="xml":
            print "  </MonthlyStatistics>"
    #
    # Summarize commits for the last nquarters
    #
    if options.nquarters > 0:
        if format=="xml":
            print "  <QuarterlyStatistics>"
        else:
            print ""
            print "---------------------------------"
            print "       Quarterly Statistics"
            print "---------------------------------"
            print ""
        summarize(reposdir,options.nquarters,90,format)
        if format=="xml":
            print "  </QuarterlyStatistics>"
    #
    # Finalize output
    #
    if format=="xml":
        print "</SVNCommitSummary>"


def main(argv, command="commit_summary"):
    #
    # Parse options
    #
    parser = OptionParser()
    parser.add_option("-d", "--debug",
        help="Print debugging information",
        action="store_true",
        dest="debug",
        default=False)
    parser.add_option("--version",
        help="Print the version number, then exit",
        action="store_true",
        dest="version",
        default=False)
    parser.add_option("-x","--xml",
        help="Specifies the generation of output in XML format.",
        action="store_true",
        dest="xml_format",
        default=False)
    parser.add_option("--ndays",
        help="Summarize commits for the specified number of days",
        action="store",
        dest="ndays",
        default=1)
    parser.add_option("--nweeks",
        help="Summarize commits for the specified number of weeks",
        action="store",
        dest="nweeks",
        default=1)
    parser.add_option("--nmonths",
        help="Summarize commits for the specified number of months",
        action="store",
        dest="nmonths",
        default=1)
    parser.add_option("--nquarters",
        help="Summarize commits for the specified number of quarters",
        action="store",
        dest="nquarters",
        default=1)
    parser.add_option("-o", "--output",
        help="Write output to this file",
        action="store",
        dest="output",
        default=None)
    parser.usage=command+" [options] <svn-directory> [<svn-directory> ...]"
    parser.description="A utility to summarize the commit history for one or more subversion repositories."
    #
    # Process options
    #
    (options, args) = parser.parse_args(args=argv)
    if options.version:
        print command + " (FAST version "+fast.__version__+")"
        print ""
        print "Copyright (2008) Sandia Corporation. Under the terms of Contract "
        print "DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government "
        print "retains certain rights in this software."
        sys.exit(0)
    global debug
    debug=options.debug
    if options.xml_format:
        format="xml"
    else:
        format="text"
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    options.ndays=int(options.ndays)
    options.nweeks=int(options.nweeks)
    options.nmonths=int(options.nmonths)
    options.nquarters=int(options.nquarters)
    #
    # setup redirect
    #
    if not options.output is None:
        pyutilib.misc.setup_redirect(options.output)
    #
    # Process list of subversion repositories
    #
    for file in args[1:]:
        main_summarize(file, options, format)
    #
    # Reset redirect
    #
    if not options.output is None:
        pyutilib.misc.reset_redirect()
