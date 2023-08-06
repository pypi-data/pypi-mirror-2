#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla Corporation Code.
#
# The Initial Developer of the Original Code is
# Samuel C Liu
#
# Contributor(s): Sam Liu <sam@ambushnetworks.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****


"""
Known Issues:
  1) Multi-core compilation on Windows not supported
"""

from optparse import OptionParser, OptionGroup #note: deprecated in Python27, use argparse
from mozrunner import Runner, FirefoxRunner
from mozrunner import FirefoxProfile
from types import *
from utils import hgId, captureStdout
import os, sys, subprocess, string, re, tempfile, shlex, glob, shutil,datetime
import simplejson, urllib



#Global Variables
showMakeData = 0
progVersion="0.3.4"

class Builder():
  def __init__(self, makeCommand=["make","-f","client.mk","build"] , shellCacheDir=os.path.join(os.path.expanduser("~"), "moz-commitbuilder-cache"), cores=1, repoURL="http://hg.mozilla.org/mozilla-central"):
    #Generate cache, test for mercurial, update or download trunk

    self.makeCommand = makeCommand
    self.shellCacheDir = shellCacheDir
    self.cores = cores
    self.repoURL = repoURL
    self.confDir = os.path.join(shellCacheDir, "mozconf")
    self.repoPath = os.path.join(shellCacheDir,"mozbuild-trunk")
    self.hgPrefix = ['hg', '-R', self.repoPath]

    if not os.path.exists(shellCacheDir):
      os.mkdir(shellCacheDir)
    if not os.path.exists(self.confDir):
      os.mkdir(self.confDir)

    try:
      testhgInstall = subprocess.Popen(["hg","--version"],stdout=subprocess.PIPE)
      testresult = testhgInstall.communicate()
    except OSError as err:
      print "hg not installed on this system."
      quit()

    self.getTrunk()

  def getTip(self):
    #Parse output of hg for tip's changeset identifier hash
    try:
      tiprev = subprocess.Popen(self.hgPrefix+["tip"],stdout=subprocess.PIPE)
      capturedString = tiprev.communicate()
      try:
        changesetTip = capturedString[0].split("\n")[0].split(" ")[3].split(":")[1]
      except:
        pass
    except:
      print "Woops, something went wrong!"
      quit()
    if changesetTip:
      return changesetTip
    else:
      print "Couldn't get the tip changeset."

  def increment_day(self, date):
    s = date.split("-")
    delta = datetime.timedelta(days=1)
    nextDate = datetime.date(int(s[0]),int(s[1]),int(s[2])) + delta
    return str(nextDate)

  def changesetFromDay(self, date, oldest=True):
    #Gets first changeset from a given date
    nextDate = self.increment_day(date)
    pushlog_url = "http://hg.mozilla.org/mozilla-central/json-pushes?startdate="+date+"&enddate="+nextDate
    pushlog_json = simplejson.load(urllib.urlopen(pushlog_url))
    sorted_keys = sorted(map(int,pushlog_json.keys()))

    changesetString = None
    if oldest:
        try:
            pushlog_first = str(sorted_keys.pop(0))
            changesetString = pushlog_json[pushlog_first]['changesets']
        except:
            pass
    else:
        try:
            pushlog_last = str(sorted_keys.pop(-1))
            changesetString = pushlog_json[pushlog_last]['changesets']
        except:
            pass

    if changesetString != None:
      return changesetString

    return False

  def getTrunk(self, makeClean=False):
    if makeClean:
        try:
            shutil.rmtree(self.repoPath)
        except:
            pass
    #Gets or updates our cached repo for building
    if os.path.exists(os.path.join(self.repoPath,".hg")):
      print "Found a recent trunk. Updating it to head before we begin..."
      updateTrunk = subprocess.call(self.hgPrefix + ["pull","-u"])
      print "Update successful."
    else:
      print "Trunk not found."
      makeClean = subprocess.call(["rm","-rf", self.repoPath])
      print "Removed old mozbuild-trunk directory. Downloading a fresh repo from mozilla-central..."
      #downloadTrunk = os.popen("hg clone http://hg.mozilla.org/mozilla-central mozbuild-trunk")
      downloadTrunk = subprocess.call(["hg", "clone", self.repoURL, "mozbuild-trunk"], cwd=self.shellCacheDir)

  def bisect(self,good,bad):
    #Call hg bisect with initial params, set up building environment (mozconfig)
    good = hgId(good, self.hgPrefix)
    bad = hgId(bad, self.hgPrefix)
    if good and bad and self.validate(good, bad): #valid commit numbers, do the bisection!
        subprocess.call(self.hgPrefix+["bisect","--reset"])
        subprocess.call(self.hgPrefix+["up",bad])
        subprocess.call(self.hgPrefix+["bisect","--bad"])
        subprocess.call(self.hgPrefix+["bisect","--good",good])

        #Prebuild stuff here!!

        #Make mozconfig
        os.chdir(self.confDir)
        if os.path.exists("config-default"):
          os.unlink("config-default")

        f=open('config-default', 'w')
        #Ensure we know where to find our built stuff by using a custom mozconfig
        f.write('mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-ff-dbg\n')

        #HACK :/
        if sys.platform == "win32" or sys.platform == "cygwin":
          f.write("ac_add_options --with-windows-version=600\n")
          f.write("ac_add_options --enable-application=browser\n")
        else:
          f.write('mk_add_options MOZ_MAKE_FLAGS="-s -j'+str(self.cores)+'"')

        f.close()

        #export MOZCONFIG=/path/to/mozilla/mozconfig-firefox
        os.environ['MOZCONFIG']=self.confDir+"/config-default"

        self.bisectRecurse()
    else:
      print "Invalid values. Please check your changeset revision numbers."

  def bisectRecurse(self):
    #Recursively build and prompt

    self.build()

    #Run the built binary
    if sys.platform == "darwin":
      runner = FirefoxRunner(binary=os.path.join(self.shellCacheDir,"mozbuild-trunk","obj-ff-dbg","dist","Nightly.app","Contents","MacOS")+"/firefox-bin")
      runner.start()
    elif sys.platform == "linux2":
      runner = FirefoxRunner(binary=os.path.join(self.shellCacheDir,"mozbuild-trunk","obj-ff-dbg","dist","bin") + "/firefox")
      runner.start()
    elif sys.platform == "win32" or sys.platform == "cygwin":
      runner = FirefoxRunner(binary=os.path.join(self.shellCacheDir,"mozbuild-trunk","obj-ff-dbg","dist","bin") + "/firefox.exe")
      runner.start()
    else:
      print "Your platform is not currently supported."
      quit()

    verdict = ""
    while verdict != 'good' and verdict != 'bad' and verdict != 'b' and verdict != 'g':
      verdict = raw_input("Was this commit good or bad? (type 'good' or 'bad' and press Enter): ")

    #do hg bisect --good or --bad depending on whether it's good or bad
    retval = 0;
    if verdict == 'good':
      retval = captureStdout(self.hgPrefix+["bisect","--good"])
    else:
      retval = captureStdout(self.hgPrefix+["bisect","--bad"])

    print str(retval)

    # HACK
    if retval[1] == 'h': #if retval starts with "the" then we can quit
      quit()
    elif retval[1] == 'e': #if retval starts with "testing" then it needs to keep going
      print "\n"
    else:
      print "Something went wrong! :("
      quit()

    self.bisectRecurse()

  def build(self, changeset=0):
    #Build a binary and return the file path
    #Binary file named by changeset number
    if changeset != 0:
      print "Switching to revision "+changeset[:8]+"..."
      subprocess.call(self.hgPrefix+["update",changeset]) #switch to a given directory
    #Call make on our cached trunk
    print "Building..."
    makeData = captureStdout(self.makeCommand, ignoreStderr=True,
                            currWorkingDir=self.repoPath)
    if showMakeData == 1:
      print makeData

    print "Build complete!"

  def getBinary(self, revision):
    #Return path of binary for a given changeset
    #mozbuildserver uses this to build revisions
    self.build(changeset=revision)

    #run make package
    print "Making binary..."
    makeData = captureStdout(["make","package"], ignoreStderr=True,
                            currWorkingDir=os.path.join(self.repoPath,"obj-ff-dbg"))

    binary = None
    renamedBinary = None
    distFolder = os.path.join(self.repoPath,"obj-ff-dbg","dist")
    #return path to package
    if sys.platform == "darwin":
        try:
            binary = glob.glob(distFolder+"/firefox-*.dmg")[0]
        except:
            binary = None
        renamedBinary = str(revision[:8]) + ".dmg" #Don't want the filename to be too long :)
    elif sys.platform == "linux2":
        try:
            binary = glob.glob(distFolder+"/firefox-*.tar.gz")[0]
        except:
            binary = None
        renamedBinary = str(revision[:8]) + ".tar.gz"
    elif sys.platform == "win32" or sys.platform == "cygwin":
        try:
            binary = glob.glob(distFolder+"/firefox-*.zip")[0]
        except:
            binary = None
        renamedBinary = str(revision[:8]) + ".zip"
    else:
      print "ERROR: This platform is unsupported."
      quit()

    if binary != None:
        print "Binary build successful!"
        print renamedBinary + " is the binary:"
        #print "Move binary from " + binary
        #print " to " + os.path.join(self.shellCacheDir,renamedBinary)

        #Move the binary into the correct place.
        try:
            os.remove(os.path.join(self.shellCacheDir,renamedBinary))
        except:
            pass

        shutil.move(binary, os.path.join(self.shellCacheDir,"builds",renamedBinary))

        #Return binary path
        return (os.path.join(self.shellCacheDir,"builds",renamedBinary), renamedBinary)

    print "ERROR: Binary not found."
    quit()

  def validate(self, good, bad):
    #Check that given changeset numbers aren't wonky
    if (good == bad):
      return False
    return True

def cli():
  #Command line interface
  usage = "usage: %prog --good=[changeset] --bad=[changeset] [options]"

  parser = OptionParser(usage=usage,version="%prog "+progVersion)
  parser.add_option("-g", "--good", dest="good",
                    help="Last known good revision",
                    metavar="changeset#")
  parser.add_option("-b", "--bad", dest="bad",
                    help="Broken commit revision",
                    metavar="changeset#")
  parser.add_option("-c", "--cores", dest="cores",
                    help="Number of cores to compile with",
                    metavar="numcores")

  parser.add_option("-f", "--freshtrunk", dest="makeClean",
                    help="Delete old trunk and use a fresh one",
                    metavar="1", default=0)

  group = OptionGroup(parser, "Unstable Options",
                    "Caution: use these options at your own risk.  "
                    "They aren't recommended.")

  group.add_option("-r", "--repo", dest="repoURL",
                    help="alternative mercurial repo to bisect",
                    metavar="valid repository url")

  group.add_option("-m", "--altmake", dest="alternateMake",
                    help="alternative make command for building",
                    metavar="make command, in quotes")

  parser.add_option_group(group)
  (options, args) = parser.parse_args()

  # Run it
  if not options.good or not options.bad:
    print "Use -h flag for available options. You must specify both a good and a bad date."
  else:

    print "Begin interactive commit bisect!"

    commitbuilder = Builder()

    if options.cores:
      commitbuilder.cores = options.cores
      print "Compiling with "+options.cores+ " cores."
    if options.repoURL:
      commitbuilder.repoURL = options.repoURL
      print "Using alternative repository "+options.repoURL
    if options.alternateMake:
      commitbuilder.makeCommand = shlex.split(options.alternateMake)

    commitbuilder.bisect(options.good,options.bad)

if __name__ == "__main__":
  cli()
