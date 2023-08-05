#  _________________________________________________________________________
#
#  FAST: Python tools for software testing.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the FAST README.txt file.
#  _________________________________________________________________________

import os.path
from svn import *
import yaml
import pyutilib.misc.twzzle
import copy
import shutil


def get_revision(path):
    try:
        rev = int( svn_revision(path) )
        return rev
    except Exception, err:
        print "ERROR: bad revision "+str(svn_revision(path))+" for path "+str(path)
        raise err


class External(object):

    def __init__(self, dir=None, link=None, rev=None, edir=None):
        self.dir=dir
        self.link=link
        self.rev=rev
        self.auxdir=self._compute_auxdir()
        self.edir=edir
        self.name=self.dir[ len(self.edir):]

    def _compute_auxdir(self):
        tokens = self.link.split('/')
        i=-1
        auxdir = ""
        while i >= - len(tokens):
            if tokens[i] == "trunk":
                if i+1 < 0:
                    auxdir = "/".join(tokens[i+1:])
                break
            elif tokens[i] in ("stable","tags","releases","branches"):
                if i+2 < 0:
                    auxdir = "/".join(tokens[i+2:])
                break
            else:
                i=i-1
        if auxdir != "":
            auxdir = "/"+auxdir
        return auxdir



class SVNProject:

  def __init__(self,repos,name):
        self.repos=repos
        self.name=name
        self.revision = -1
        self.update(repos,name)

  def update(self,repos=None,name=None):
        if repos is None:
            repos=self.repos
            newaux=self.aux
        else:
            newaux=False
        if name is None:
            name=self.name

        #
        # Don't update unless the project revision is newer than the
        # last revision.
        #
        rev = get_revision(repos)
        if rev < self.revision:
            return
        self.revision = rev

        self.has_trunk=False
        self.has_releases=False
        self.has_tags=False
        self.has_branches=False
        self.has_stable=False

        self.trunk_dir = None

        self.stable_name = None
        self.stable_diffs = None
        self.stable_dir = None
        self.stable_rev = None

        self.release_name = None
        self.release_diffs = None
        self.release_dir = None
        self.release_rev = None

        self.tag_name = None
        self.tag_diffs = None
        self.tag_dir = None
        self.tag_rev = None

        self.aux = newaux
        if self.name is None:
           self.name_str = ""
        else:
           self.name_str = "/" + name 
        self.proj_root = repos + self.name_str
        subdir = commands.getoutput("svn ls " + self.proj_root)
        self.dirs = subdir.split("\n")
        self.init(self.dirs)

  def init(self,dlist):
        #
        # Get layout
        #
        self.has_trunk = "trunk/" in dlist
        if self.has_trunk:
            self.trunk_dir = self.proj_root+"/trunk"
        self.has_releases = "releases/" in dlist
        self.has_tags = "tags/" in dlist
        self.has_branches = "branches/" in dlist
        self.has_stable = "stable/" in dlist
        #
        # Guess release and stable version
        #
        if self.has_releases:
           (self.release_name,self.release_dir) = guess_release(self.repos,self.name_str,"releases")
           if self.release_dir is None:
              self.has_releases=False
        if self.has_tags:
           (self.tag_name,self.tag_dir) = guess_release(self.repos,self.name_str,"tags")
           if self.tag_dir is None:
              self.has_tags=False
        if self.has_stable:
           (self.stable_name,self.stable_dir) = guess_release(self.repos,self.name_str,"stable")
           if self.stable_dir is None:
              self.has_stable=False
        #
        # If have a trunk and stable directory, then summarize the number
        # of differences.
        #
        if self.has_trunk and self.stable_name is not None:
           output = commands.getoutput("svn diff --summarize " + self.repos+self.name_str+"/trunk " + self.stable_dir)
           if output == "":
              self.stable_diffs = 0
           else:
              diffs = output.split("\n")
              self.stable_diffs = len(diffs)
        #
        # If have a trunk and a release directory, then summarize the number
        # of differences.
        #
        if self.has_trunk and self.release_name is not None:
           output = commands.getoutput("svn diff --summarize " + self.repos+self.name_str+"/trunk " + self.release_dir)
           if output == "":
              self.release_diffs = 0
           else:
              diffs = output.split("\n")
              self.release_diffs = len(diffs)
        #
        # If have a trunk and a tag directory, then summarize the number
        # of differences.
        #
        if self.has_trunk and self.tag_name is not None:
           output = commands.getoutput("svn diff --summarize " + self.repos+self.name_str+"/trunk " + self.tag_dir)
           if output == "":
              self.tag_diffs = 0
           else:
              diffs = output.split("\n")
              self.tag_diffs = len(diffs)
        #
        # Get revision #'s
        #
        if not self.trunk_dir is None:
            self.revision = get_revision(self.trunk_dir)
        if not self.tag_dir is None:
            self.tag_rev = get_revision(self.tag_dir)
        if not self.stable_dir is None:
            self.stable_rev = get_revision(self.stable_dir)
        if not self.release_dir is None:
            self.release_rev = get_revision(self.release_dir)

           

  def write(self,format=""):
        if format=="text":
           print ""
           print "  Project         ",self.name
           print "  Project Root    ",self.proj_root
           print "  Trunk Branch    ",self.has_trunk
           print "  Normal Branches ",self.has_branches

           print "  Tag Branches    ",self.has_tags
           if self.has_tags:
                print "    Latest Tag    ",self.tag_name
                print "    Tag Diffs     ",self.tag_diffs
                print "    Tag Path      ",self.tag_dir
                print "    Tag Rev       ",self.tag_rev

           print "  Stable Branches ",self.has_stable
           if self.has_stable:
                print "    Latest Stable   ",self.stable_name
                print "    Stable Diffs    ",self.stable_diffs
                print "    Stable Path     ",self.stable_dir
                print "    Stable Rev      ",self.stable_rev

           print "  Release Branches",self.has_releases
           if self.has_releases:
                print "    Latest Release  ",self.release_name
                print "    Release Diffs   ",self.release_diffs
                print "    Release Path    ",self.release_dir
                print "    Release Rev     ",self.release_rev
        elif format=="xml" or format=="alerts":
           print "  <Project>"
           if self.name is None:
              print "    <Name>" + "" + "</Name>"
           else:
              print "    <Name>" + self.name + "</Name>"
           print "    <Root>" + self.proj_root + "</Root>"
           print "    <TrunkBranch>"+`self.has_trunk`+"</TrunkBranch>"
           print "    <NormalBranches>"+`self.has_branches`+"</NormalBranches>"

           print "    <TagBranches>"+`self.has_tags`+"</TagBranches>"
           print "    <LatestTag>"+str(self.tag_name)+"</LatestTag>"
           print "    <TagDiffs>"+`self.tag_diffs`+"</TagDiffs>"
           print "    <TagPath>"+str(self.tag_dir)+"</TagPath>"

           print "    <StableBranches>"+`self.has_stable`+"</StableBranches>"
           print "    <LatestStable>"+str(self.stable_name)+"</LatestStable>"
           print "    <StableDiffs>"+`self.stable_diffs`+"</StableDiffs>"
           print "    <StablePath>"+str(self.stable_dir)+"</StablePath>"

           print "    <ReleaseBranches>"+`self.has_releases`+"</ReleaseBranches>"
           print "    <LatestRelease>"+str(self.release_name)+"</LatestRelease>"
           print "    <ReleaseDiffs>"+`self.release_diffs`+"</ReleaseDiffs>"
           print "    <ReleasePath>"+str(self.release_dir)+"</ReleasePath>"

           print "  </Project>"



class Twzzl(object):

    def moveOn(self):
        pass

    def getStart(self, str):
        pass


class ExternalsDB(object):

    def __init__(self):
        self.clear()
        
    def clear(self):
        self.DB = {}
        self.revision = {}
        self.projects = {}
        self.repository = {}
        
    def reset(self):
        tmp = copy.copy(self.repository)
        self.clear()
        for url in tmp:
            aux = tmp[url]
            self.add(repository=url, aux=aux)
        self.update()

    def read(self, filename):
        print "Reading file '%s'" % filename
        INPUT=open(filename)
        (self.repository,self.revision,self.DB,self.projects) = yaml.load_all(INPUT)
        INPUT.close()

    def write(self, filename=None, stream=None):
        if stream is None:
            print "Writing file '%s'" % filename
            OUTPUT=open(filename, 'w')
        else:
            OUTPUT=stream
        #
        print >>OUTPUT, "# All repositories added to this database"
        yaml.dump(self.repository, OUTPUT, default_flow_style=False)
        #
        print >>OUTPUT, "---"
        print >>OUTPUT, "# Revisions for subversion repositories"
        yaml.dump(self.revision, OUTPUT, default_flow_style=False)
        #
        print >>OUTPUT, "---"
        print >>OUTPUT, "# Externals found in subversion repositories"
        yaml.dump(self.DB, OUTPUT, default_flow_style=False)
        #
        print >>OUTPUT, "---"
        print >>OUTPUT, "# Information about projects"
        yaml.dump(self.projects, OUTPUT, default_flow_style=False)
        #
        if stream is None:
            OUTPUT.close()
        
    def print_projects(self, format="text", aux=False):
        keys = self.projects.keys()
        keys.sort()
        for key in keys:
            if self.projects[key].aux is aux:
                self.projects[key].write(format)

    def add(self, repository=None, aux=False):
        if repository[-1] == '/':
           repository = repository[0:-1]
        if repository in self.revision:
            return
        print "Adding repository %s ..." % str(repository)
        self.repository[repository] = aux
        if aux == False:
            self.revision[repository] = -1
            self.DB[repository] = {}
        #
        # Process this repository and add associated projects
        #
        dir = commands.getoutput("svn ls " + repository)
        dirs = dir.split("\n")
        has_trunk = "trunk/" in dirs
        if has_trunk:
            proj = SVNProject(repository,None)
            proj.aux = aux
            key = repository
            if proj.name is not None:
                key = key+"/"+proj.name
            self.projects[ key ] = proj
        else:
            for file in dir.split("\n"):
                file = file.strip()
                if file[-1] == "/":
                    proj = SVNProject(repository,file[:-1])
                    proj.aux = aux
                    self.projects[ proj.proj_root ] = proj

    def update(self, filename=None, truncate=True, filter=None):
        """
        Update the externals for all repositories
        """
        print "Performing update ..."
        if not filename is None:
            if os.path.exists(filename):
                self.read(filename)
        keys = self.DB.keys()
        #
        print "Updating externals ..."
        for repository in keys:
            print "  "+repository,
            self._progress = pyutilib.misc.twzzle.progress()
            self._progress.getStart("")
            if repository in self.revision:
                rev = self.revision[repository]
            else:
                rev = 0
            self.DB[repository] = self._update_repository(repository, revision=rev, externals=self.DB[repository], first=True, truncate=truncate, filter=filter)
            rev = get_revision(repository)
            self.revision[repository] = rev
            self._progress = None
            print ""
        #
        print "Updating projects ...",
        self._progress = pyutilib.misc.twzzle.progress()
        self._progress.getStart("")
        for proj in self.projects:
            self._progress.moveOn()
            self.projects[proj].update()
        self._progress = None
        print ""
        #
        if not filename is None:
            self.write(filename)
        print "... done."

    def _update_repository(self, repository, revision=0, externals=None, dir="/", first=False, truncate=True, filter=None):
        """
        Update the externals in a subversion repository.

        The 'externals' data is a dictionary:  directory -> Bunch()
        """
        self._progress.moveOn()
        if externals is None:
            externals = {}
        path=repository+dir
        if not filter is None and not (path.startswith(filter) or filter.startswith(path)):
            return externals
        #
        # See if there are externals in the current path
        # 
        tmp = []
        if path in externals:
            # Delete the externals history, since these may have been removed.
            del externals[path]
        for ext in svn_get_externals(path):
            tmp.append( External(link=ext.link, rev=ext.rev, dir=dir+ext.name, edir=dir) )
        if len(tmp) > 0:
            externals[path] = tmp
        #
        # Recurse into subdirectories, but only if the subdirectory
        # has a more recent revision than 'revision'
        #
        for file in svn_ls(path):
            if file[-1] == "/":
                tpath = path+file
                rev = get_revision(tpath)
                if not truncate or (truncate and rev >= revision):
                    externals = self._update_repository(repository, revision=revision, externals=externals, dir=dir+file, truncate=truncate, filter=filter)
        #
        # If we are starting recursion, then we go through the externals dictionary to validate
        # that all directories exist.
        #
        if first:
            #
            # NOTE: we might be able to optimize this computation, but that doesn't
            # seem necessary right now.
            #
            tmp = {}
            for path in externals:
                self._progress.moveOn()
                if not svn_revision(path) is None:
                    tmp[path] = externals[path]
            externals = tmp
        #
        # Return the externals data
        #
        return externals

    def validate(self, filter=None):
        """
        Validate the externals
        """
        if not filter is None:
            froot = guess_projroot(filter)
        for repository in self.DB:
            if filter is None or froot.startswith(repository):
                print "Validating links in repository", repository
                keys = self.DB[repository].keys()
                keys.sort()
                for edir in keys:
                    if not filter is None and not edir.startswith(filter):
                        continue
                    projroot = guess_projroot(edir)
                    proj = self.projects[projroot]
                    etype = path_type(edir)
                    latest = (\
                        (proj.has_trunk and edir.startswith(proj.trunk_dir)) or \
                        (proj.has_tags and edir.startswith(proj.tag_dir)) or \
                        (proj.has_stable and edir.startswith(proj.stable_dir)) or \
                        (proj.has_releases and edir.startswith(proj.release_dir)) or \
                        (etype == "branches"))
                    if latest:
                        for ext in self.DB[repository][edir]:
                            self._validate_link(repository, ext)
            
    def _validate_link(self, repository, external):
            projroot = guess_projroot(external.link)
            if not projroot in self.projects:
                print_alert("Error",repository+external.dir ,"External points to an unknown repository: "+external.link)
                return
            proj = self.projects[ projroot ]
            etype = path_type(repository+external.dir)
            print ".",repository+external.dir
            ptype = path_type(external.link)
            #print "X",etype,external.link
            dir = repository+external.dir
            #print "HERE -------------------------------"
            #print "HERE",projroot
            #print "HERE",dir
            #print "HERE",external.dir
            #print "HERE",etype
            #print "HERE",external.link
            #print "HERE",ptype
            if ptype in ("branches","tags","releases") and etype in ("tags","releases") and external.rev == "":
                print_alert("Error",dir ,"External does not have a revision specified: " + external.link)
            #
            # Check if the link is missing, or if it is out of date
            #
            if ptype == "trunk":
                if not proj.has_trunk:
                    print_alert("Error",dir ,"External missing: " + external.link)
                else:
                    print_alert("OK",dir ,"External OK: " + external.link)
                    if (etype == "stable" or etype == "tag" or etype == "release") and external.rev == "":
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
                elif not external.link.startswith(proj.tag_dir.strip()):
                    if external.rev == "":
                        print_alert("LinkUpdate",dir ,"Update","Replace link " + external.link + " with " + proj.tag_dir)
                else:
                    print_alert("OK",dir ,"External OK: " + external.link)

            elif ptype == "releases":
                if not proj.has_releases:
                    print_alert("Error",dir ,"External missing: " + external.link)
                elif not external.link.startswith(proj.release_dir.strip()):
                    if external.rev == "":
                        print_alert("LinkUpdate",dir ,"Update","Replace link " + external.link + " with " + proj.release_dir)
                else:
                    print_alert("OK",dir ,"External OK: " + external.link)

            elif ptype == "stable":
                 if not proj.has_stable:
                    print_alert("Error",dir ,"External missing: " + external.link)
                 elif (etype=="trunk" or etype=="stable") and not external.link.startswith(proj.stable_dir.strip()):
                    print_alert("LinkUpdate",dir ,"Update","Replace link " + external.link + " with " + proj.stable_dir)
                 elif etype == "tags" or etype == "releases":
                    if external.rev == "":
                        print_alert("Error",dir ,"External to a stable branch from a " + etype + " branch: " + external.link)
                 else:
                    print_alert("OK",dir ,"External OK: " + external.link)
            else:
                print_alert("NonStandard",dir ,"External not verified: " + external.link)

    def update_externals(self, url, trunk=False, stable=False, tags=False, releases=False, latest_rev=False, dest=None):
        if svn_revision(url) is None:
            print "ERROR: must specify a valid subversion URL"
            sys.exit(1)
        etype = path_type(url)
        if trunk+stable+tags+releases == 0:
            if etype == "stable":
                stable=True
            elif etype == "trunk":
                trunk=True
            elif etype == "releases":
                releases=True
            elif etype == "tags":
                tags=True
        if trunk+stable+tags+releases != 1:
            print "ERROR: confusing update options: trunk=%d stable=%d tags=%d releases=%d" % (trunk, stable, tags, releases)
            sys.exit(1)
        updated_repos=None
        updated = set()
        for repository in self.DB:
            for dir in self.DB[repository]:
                for external in self.DB[repository][dir]:
                    path = repository+external.dir
                    if path.startswith(url):
                        updated_repos = repository
                        updated.add(dir)
                        print "  Updating %s" % path
                        projroot = guess_projroot(external.link)
                        if not projroot in self.projects:
                            print "    ERROR: unknown repository"
                            continue
                        if external.rev == "":
                            print "    From %s " % external.link
                        else:
                            print "    From -r %s %s " % (external.rev, external.link)
                        #
                        # Update links to the latest stable branch
                        #
                        if stable:
                            if self.projects[projroot].has_stable:
                                external.rev = self.projects[projroot].stable_rev
                                external.link = self.projects[projroot].stable_dir + external.auxdir
                            elif self.projects[projroot].has_tags:
                                external.rev = self.projects[projroot].tag_rev
                                external.link = self.projects[projroot].tag_dir + external.auxdir
                            elif self.projects[projroot].has_releases:
                                external.rev = self.projects[projroot].release_rev
                                external.link = self.projects[projroot].release_dir + external.auxdir
                            else:
                                print "    CANNOT UPDATE: no stable branches"
                                continue
                        elif trunk:
                            if self.projects[projroot].has_trunk:
                                external.rev = ""
                                external.link = self.projects[projroot].trunk_dir + external.auxdir
                            elif self.projects[projroot].has_stable:
                                external.rev = self.projects[projroot].stable_rev
                                external.link = self.projects[projroot].stable_dir + external.auxdir
                            elif self.projects[projroot].has_tags:
                                external.rev = self.projects[projroot].tag_rev
                                external.link = self.projects[projroot].tag_dir + external.auxdir
                            elif self.projects[projroot].has_releases:
                                external.rev = self.projects[projroot].release_rev
                                external.link = self.projects[projroot].release_dir + external.auxdir
                            else:
                                print "    CANNOT UPDATE: no trunk branches"
                                continue
                        elif tags or releases:
                            if self.projects[projroot].has_tags:
                                external.rev = self.projects[projroot].tag_rev
                                external.link = self.projects[projroot].tag_dir + external.auxdir
                            elif self.projects[projroot].has_releases:
                                external.rev = self.projects[projroot].release_rev
                                external.link = self.projects[projroot].release_dir + external.auxdir
                            else:
                                print "    CANNOT UPDATE: no tags or releases branches"
                                continue
                        if latest_rev and exernal.rev != "":
                            print "    To -r %s %s " % (external.rev, external.link)
                        else:
                            print "    To %s " % external.link
        print ""
        if dest is None:
            dest = 'svnem_update'
        if os.path.exists(dest):
            print "Removing directory %s" % dest
            shutil.rmtree(dest)
        print "Checking out %s in %s" % (url, dest)
        svn_checkout(url, dest=dest, options="--ignore-externals -q")
        message="Commit message created by svnem:\n\nUpdating externals in the following directories:\n"
        for dir in updated:
            path = dest + "/"+dir[ len(url): ]
            set_externals(self.DB[updated_repos][dir], dir=path, latest_rev=latest_rev)
            message += "  "+path+"\n"
        OUTPUT = open(dest+os.sep+"svn_message.txt","w")
        print >>OUTPUT, message
        OUTPUT.close()
        print ""
        print "Finished updating externals for",url
        print "See",dest+os.sep+"svn_message.txt","for details."

    def status(self, filter=None):
        """
        Summarize the status of the database
        """
        #if not filter is None:
            #froot = guess_projroot(filter)
        plist = self.projects.keys()
        plist.sort()
        for projroot in plist:
                    #print "HERE",projroot,self.projects[projroot].name
                    proj = self.projects[projroot]
                    if not proj.has_trunk:
                        continue
                    #if proj.has_stable and proj.revision <= proj.stable_rev:
                        #continue
                    if proj.has_stable:
                        if proj.has_releases and proj.stable_rev <= proj.release_rev and proj.revision <= proj.stable_rev:
                            continue
                        if proj.has_tags and proj.stable_rev <= proj.tag_rev and proj.revision <= proj.stable_rev:
                            continue
                    if proj.has_releases and proj.revision <= proj.release_rev:
                        continue
                    if proj.has_tags and proj.revision <= proj.tag_rev:
                        continue
                    if proj.name is None:
                        print "  Status of package", proj.repos
                    else:
                        print "  Status of package", proj.name
                    if proj.has_trunk:
                        highlight='*'
                        if proj.has_stable and proj.revision < proj.stable_rev:
                            highlight=''
                        if proj.has_releases and proj.revision < proj.release_rev:
                            highlight=''
                        if proj.has_tags and proj.revision < proj.tag_rev:
                            highlight=''
                        print "    Trunk revision:  ", proj.revision, highlight
                    if proj.has_stable:
                        highlight='*'
                        if proj.has_trunk and proj.stable_rev < proj.revision:
                            highlight=''
                        if proj.has_releases and proj.stable_rev < proj.release_rev:
                            highlight=''
                        if proj.has_tags and proj.stable_rev < proj.tag_rev:
                            highlight=''
                        print "    Stable revision: ", proj.stable_rev, highlight
                    if proj.has_releases:
                        highlight='*'
                        if proj.has_trunk and proj.release_rev < proj.revision:
                            highlight=''
                        if proj.has_stable and proj.release_rev < proj.stable_rev:
                            highlight=''
                        if proj.has_tags and proj.release_rev < proj.tag_rev:
                            highlight=''
                        print "    Release revision:", proj.release_rev
                    if proj.has_tags:
                        highlight='*'
                        if proj.has_trunk and proj.tag_rev < proj.revision:
                            highlight=''
                        if proj.has_stable and proj.tag_rev < proj.stable_rev:
                            highlight=''
                        if proj.has_releases and proj.tag_rev < proj.release_rev:
                            highlight=''
                        print "    Tag revision:    ", proj.tag_rev
                    print ""
            

