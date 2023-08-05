#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

import re
import commands
from pyutilib.misc import Bunch
import sys
import os


def svn_revision(dir):
    #print "svn_revision","svn info "+dir
    output = commands.getoutput("svn info "+dir)
    for line in output.split("\n"):
        tokens = re.split("[ \t]+",line.strip())
        if len(tokens) == 4 and tokens[2] == "Rev:":
            return tokens[3]
    return None

def set_externals(externals,dir=None,latest_rev=True):
    if len(externals) == 0:
        return
    currdir = os.getcwd()
    if not dir is None:
        os.chdir(dir)
    OUTPUT = open("Externals","w")
    for ext in externals:
        if latest_rev:
            rev = "-r"+str(ext.rev)
        else:
            rev=""
        print >>OUTPUT, ext.name,rev,ext.link
    OUTPUT.close()
    commands.getoutput("svn propset -F Externals svn:externals .")
    if not dir is None:
        os.chdir(currdir)

def svn_checkout(dir,dest=None,options=""):
    if type(dir) is list:
        if len(dir) == 0:
            return
        dir = " ".join(dir)
    cmd = "svn checkout "+options+" "+dir
    if not dest is None:
        cmd += " "+dest
    print "Performing subversion checkout: '%s'" % cmd
    info = commands.getoutput(cmd)
    print info

def svn_copy(dir,dest,options="",message=None):
    if message is None:
        message = " -m \"Copying with fast/sqa/svn.py\" "
    else:
        message = " -m \""+message+"\" "
    cmd = "svn copy "+options+" "+message+dir+" "+dest
    info = commands.getoutput(cmd)

def svn_update(dir, options=""):
    info = commands.getoutput("svn update "+options+" "+dir)

def svn_ls(dir):
    #print "svn_ls","svn ls "+dir
    info = commands.getoutput("svn ls "+dir)
    if "request failed" in info or "non-existent" in info:
        return None
    lines=info.split("\n")
    files=[]
    for line in lines:
        tmp = line.strip()
        if tmp != "":
            files.append(tmp)
    return files

def svn_get_externals(dir):
    externals=[]
    #
    # Use propget to get externals for this directory
    #
    info = commands.getoutput("svn propget svn:externals "+dir)
    #
    # For each line, return a tuple containing the revision 
    #   number and the external definition.  If no revision is
    #   specified, the tuple contains an empty string.
    #
    lines=info.split("\n")
    for line in lines:
        if len(line) > 0 and line[0] == '#':
            continue
        token = re.split('[ \t]+',line.strip())
        if len(token) == 2:
            # <name> <external>
            externals.append( Bunch(name=token[0], rev="", link=token[1]) )
        elif len(token) == 3:
            # <name> -r<num> <external>
            externals.append( Bunch(name=token[0], rev=token[1][2:], link=token[2]) )
        elif len(token) == 3:
            # <name> -r <num> <external>
            externals.append( Bunch(name=token[0], rev=token[2], link=token[3]) )
    return externals



def path_type(dirpath):
    tokens = dirpath.split("/")
    i = len(tokens)-1
    while i>=0:
      if (tokens[i] == "trunk") or (tokens[i] == "releases") or (tokens[i] == "stable") or (tokens[i] == "branches") or (tokens[i] == "tags"):
         break
      i = i-1
    if (tokens[i] == "trunk") or (tokens[i] == "releases") or (tokens[i] == "stable") or (tokens[i] == "branches") or (tokens[i] == "tags"):
       return tokens[i]
    return "unknown"


def print_alert(type,file,alert,action="None"):
    if type == "Ignore":
       return
    if type == "OK":
       return
    print "  "+type
    print "      link: ",file
    print "      message: "+alert
    print "      action: "+action
    print ""

def find_externals(dir,prefix=""):
  res = []
  for name in os.listdir(dir):
    if os.path.isdir(dir+"/"+name):
       res = res + find_externals(dir+"/"+name, prefix+"/"+name)
    else:
       if name == "Externals": 
          res.append(prefix + "/" + name)
  return res 


def guess_projroot(external):
    tokens = external.split("/")
    if "" in tokens:
       ndx = tokens.index("")
       if ndx > 0 and (tokens[ndx-1] == "https:" or tokens[ndx-1] == "http:"):
                 tokens[ndx-1] = tokens[ndx-1] + "/"
       tokens.remove("")
       while "" in tokens:
         ndx = tokens.index("")
         if ndx > 0 and (tokens[ndx-1] == "https:" or tokens[ndx-1] == "http:"):
                   tokens[ndx-1] = tokens[ndx-1] + "/"
         tokens.remove("")
    num = len(tokens)
    i = num-1
    while i>=0:
      if (tokens[i] == "trunk") or (tokens[i] == "releases") or (tokens[i] == "stable") or (tokens[i] == "branches") or (tokens[i] == "tags"):
         break
      i = i-1
    if i == -1:
       ans = "/".join(tokens)
    else:
       ans = "/".join(tokens[0:i])
    if ans[-1] == "/":
       return ans[0:-1]
    return ans


def guess_release(repos,name,subdir):
    output = commands.getoutput("svn ls " + repos+name+"/"+subdir)
    if output=="":
       return (None,None)
    dirs=output.split("\n")
    ans_path=""
    ans_rev=-1
    ans_dir=""
    for release_dir in dirs:
      #print release_dir
      curr=""
      dir=""
      info = commands.getoutput("svn info " + repos+name+"/"+subdir + "/" + release_dir)
      lines=info.split("\n")
      for line in lines:
        token = re.split('[ \t]+',line.strip())
        if token[0] == "Path:":
           curr=token[1]
        elif token[0] == "URL:":
           dir = token[1]
        elif token[0] == "Last" and token[1] == "Changed" and token[2] == "Rev:":
           tmp = eval(token[3])
           if tmp > ans_rev:
              ans_path=curr
              ans_rev=tmp
              ans_dir=dir
    #print repos+name+"/"+subdir,ans_path,ans_dir
    return (ans_path,ans_dir)


def validate_dir(dir, svn_projects, referenced_projects, debug=False, etype="trunk"):
    if debug:
        print " Processing repository", dir
    if dir[-1] != "/":
        dir = dir + "/"
    #
    # See if there are externals
    # 
    externals = svn_get_externals(dir)
    for external in externals:
        projroot = guess_projroot(external.link)
        if debug:
            print "  LINK: " + external.link
            print "  ROOT: " + projroot
        if projroot not in svn_projects.keys():
            #
            # The external may exist in an old revision...
            #
            if external.rev != "":
                info = commands.getoutput("svn info "+external.link+"@"+external.rev)
                if info[0:5] == "Path:":
                    continue
            print_alert("Error",dir,"Project root not found: " + projroot + " for link " + external.link)
            if debug:
                print projroot
                print svn_projects.keys()
        else:
            referenced_projects[projroot] = 1
            proj = svn_projects[ projroot ]
            ptype = path_type(external.link)
            #
            # Check if the link is missing, or if it is out of date
            #
            if ptype == "trunk":
               if not proj.has_trunk:
                  print_alert("Error",dir ,"External missing: " + external.link)
               else:
                  print_alert("OK",dir ,"External OK: " + external.link)
                  if etype == "stable" or etype == "tag" or etype == "release":
                     print_alert("Error",dir ,"External to a trunk from a " + etype + " branch: " + external.link)

            elif ptype == "branches":
               if not proj.has_branches:
                  print_alert("Error",dir ,"External missing: " + external.link)
               else:
                  #
                  # Branch externals are not verified, but that shouldn't
                  # generate a warning that we need to investigate.
                  #
                  print_alert("OK",dir ,"External not verified: " + external.link)

            elif ptype == "tags":
               if not proj.has_tags:
                  print_alert("Error",dir ,"External missing: " + external.link)
               elif etype=="trunk" and not external.link.startswith(proj.tag_dir.strip()):
                  print_alert("LinkUpdate",dir ,"Update for link " + external.link + " : " + proj.tag_dir)
               else:
                  print_alert("OK",dir ,"External OK: " + external.link)

            elif ptype == "releases":
               if not proj.has_releases:
                  print_alert("Error",dir ,"External missing: " + external.link)
               else:
                  print_alert("OK",dir ,"External OK: " + external.link)

            elif ptype == "stable":
               if not proj.has_stable:
                  print_alert("Error",dir ,"External missing: " + external.link)
               else:
                  if etype=="trunk" and not external.link.startswith(proj.stable_dir.strip()):
                     print_alert("LinkUpdate",dir ,"Update for link " + external.link + " : " + proj.stable_dir)
                  else:
                     print_alert("OK",dir ,"External OK: " + external.link)
                     if etype == "tag" or etype == "release":
                        print_alert("Error",dir ,"External to a stable branch from a " + etype + " branch: " + external.link)
            else:
               print_alert("NonStandard",dir ,"External not verified: " + external.link)
            if etype in ("tags","releases") and external.rev == "":
                print_alert("Error",dir ,"External does not have a revision specified: " + external.link)
    #
    # Recurse into subdirectories
    #
    for file in svn_ls(dir):
        if file[-1] == "/":
            if file[:-1] in ("tags","branches","releases","stable","trunk"):
                etype = file[:-1]
            validate_dir(dir+file, svn_projects, referenced_projects, debug, etype)
            


def update_externals(dir, svn_projects, options, etype=None):
    if dir[-1] != "/":
        dir = dir + "/"
    #
    # See if there are externals
    # 
    externals = svn_get_externals(dir)
    new_externals = []
    for external in externals:
        projroot = guess_projroot(external.link)
        if options.debug:
            print "  LINK: " + external.link
            print "  ROOT: " + projroot
        if projroot not in svn_projects.keys():
            #
            # The external may exist in an old revision...
            #
            if external.rev != "":
                info = commands.getoutput("svn info "+external.link+"@"+external.rev)
                if info[0:5] == "Path:":
                    continue
            print_alert("Error",dir,"Project root not found: " + projroot + " for link " + external.link)
            #
            # If we see a bad link, we still keep it, but we flag it
            #
            new_externals.append( Bunch( name="BAD_"+external.name, rev="", link=external.link) )
            if options.debug:
                print projroot
                print svn_projects.keys()
        else:
            proj = svn_projects[ projroot ]
            ptype = path_type(external.link)
            target_type = None
            #
            # Determine the target update type
            #
            target_type = "current"
            if ptype == "trunk":
                if proj.has_stable:
                    target_type = "stable"
                elif proj.has_releases:
                    target_type = "releases"
                elif proj.has_tags:
                    target_type = "tags"
            elif ptype == "trunk":
                if proj.has_tags:
                    target_type = ptype
            elif ptype == "releases":
                if proj.has_releases:
                    target_type = ptype
            elif ptype == "stable":
                if proj.has_stable:
                    target_type = ptype
            #
            # Figure out the auxdir
            #
            if target_type != "current":
                tokens = external.link.split('/')
                i=-1
                auxdir = ""
                while True:
                    if tokens[i] == "trunk":
                        if i+1 < 0:
                            auxdir = "/".join(tokens[i+1:])
                        break
                    elif tokens[i] in ("stable","tags","releases"):
                        if i+2 < 0:
                            auxdir = "/".join(tokens[i+2:])
                        break
                    else:
                        i=i-1
                if auxdir != "":
                    auxdir = "/"+auxdir
            #
            # Perform update
            #
            if target_type == "stable":
                new_externals.append( Bunch( name=external.name, rev=proj.stable_rev, link=proj.stable_dir+auxdir) )
            elif target_type == "tags":
                new_externals.append( Bunch( name=external.name, rev=proj.tag_rev, link=proj.tag_dir+auxdir) )
            elif target_type == "releases":
                new_externals.append( Bunch( name=external.name, rev=proj.release_rev, link=proj.release_dir+auxdir) )
            elif target_type == "current":
                print_alert("Warning",dir ,"Cannot update external for directory: " + external.link+".  Will use the latest revision on this directory")
                new_externals.append( Bunch( name=external.name, rev=svn_revision(external.link), link=external.link) )
    set_externals(new_externals, dir)
    #
    # Recurse into subdirectories
    #
    for file in svn_ls(dir):
        if file[-1] == "/":
            update_externals(dir+file, svn_projects, options, etype)
            

