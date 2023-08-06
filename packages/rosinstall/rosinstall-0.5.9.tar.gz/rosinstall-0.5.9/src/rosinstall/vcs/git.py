# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
"""
git vcs support.

New in ROS C-Turtle.
"""

import subprocess
import os
import vcs_base
import base64 
import sys

branch_name = "rosinstall_tagged_branch"

class GITClient(vcs_base.VCSClientBase):
    def __init__(self, path):
        """
        Raise LookupError if git not detected
        """
        vcs_base.VCSClientBase.__init__(self, path)
        with open(os.devnull, 'w') as fnull:
            if subprocess.call("git help".split(), stdout=fnull, stderr=fnull) != 0:
                raise LookupError("git not installed, cannnot create a git vcs client")

    def get_url(self):
        """
        @return: GIT URL of the directory path (output of git info command), or None if it cannot be determined
        """
        if self.detect_presence():
            output = subprocess.Popen(["git", "config",  "--get", "remote.origin.url"], cwd=self._path, stdout=subprocess.PIPE).communicate()[0]
            return output.rstrip()
        return None

    def detect_presence(self):
        return self.path_exists() and os.path.isdir(os.path.join(self._path, '.git'))


    def checkout(self, url, version='master'):
        if self.path_exists():
            print >>sys.stderr, "Error: cannnot checkout into existing directory"
            return False
            
        cmd = "git clone %s %s"%(url, self._path)
        if not subprocess.call(cmd, shell=True) == 0:
            return False
        if self.get_branch_parent() == version:
            # short circuit in default case
            return True
        elif self.is_remote_branch(version):  # remote branch
            cmd = "git checkout remotes/origin/%s -b %s"%(version, version)
        else:  # tag or hash
            cmd = "git checkout %s -b %s"%(version, branch_name)
        if not self.is_hash(version):
            cmd = cmd + " --track"
        #print "Git Installing: %s"%cmd
        if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
            return False
        # Ticket #3146
        #cmd = "git submodule update --init --recursive"
        #if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
        #    return False
        return True

    def update(self, version='master'):
        if not self.detect_presence():
            return False
        
        # shortcut if version is the same as requested
        if self.is_hash(version) :
            if self.get_version() == version:
                return True

            cmd = "git checkout -f -b rosinstall_temp" 
            if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
                return False
            cmd = "git fetch"
            if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
                return False
            cmd = "git branch -D %s"%branch_name
            if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
                pass # OK to fail return False
            cmd = "git checkout %s -f -b %s"%(version, branch_name)
            if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
                return False
            cmd = "git branch -D rosinstall_temp"
            if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
                return False
        else:     # must be a branch name
            if self.get_branch_parent() != version:
                #cannot update if branch has changed
                return False
            cmd = "git pull"
            if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
                return False
            # #3146 commented 
            #cmd = "git submodule update --init --recursive"
            #if not subprocess.call(cmd, cwd=self._path, shell=True) == 0:
            #    return False
        return True
        
    def get_vcs_type_name(self):
        return 'git'

    def get_version(self):
        output = subprocess.Popen(['git', 'log', "-1", "--format='%H'"], cwd= self._path, stdout=subprocess.PIPE).communicate()[0]
        return output.strip().strip("'")


    def is_remote_branch(self, branch_name):
        output = subprocess.Popen(['git', "branch", '-r'], cwd= self._path, stdout=subprocess.PIPE).communicate()[0]
        for l in output.split('\n'):
            elems = l.split()
            if len(elems) == 1:
                br_names = elems[0].split('/')
                if len(br_names) == 2 and br_names[0] == 'origin' and br_names[1] == branch_name:
                    return True
        return False

    def is_local_branch(self, branch_name):
        output = subprocess.Popen(['git', "branch"], cwd= self._path, stdout=subprocess.PIPE).communicate()[0]
        for l in output.split('\n'):
            elems = l.split()
            if len(elems) == 1:
                if elems[0] == branch_name:
                    return True
            elif len(elems) == 2:
                if elems[0] == '*' and elems[1] == branch_name:
                    return True
        return False

    def get_branch(self):
        output = subprocess.Popen(['git', "branch"], cwd= self._path, stdout=subprocess.PIPE).communicate()[0]
        for l in output.split('\n'):
            elems = l.split()
            if len(elems) == 2 and elems[0] == '*':
                return elems[1]
        return None

    def get_branch_parent(self):
        output = subprocess.Popen(['git', "config", "--get", "branch.%s.merge"%self.get_branch()], cwd= self._path, stdout=subprocess.PIPE).communicate()[0].strip()
        if not output:
            print "No output of get branch.%s.merge"%self.get_branch()
            return None
        elems = output.split('/')
        if len(elems) != 3 or elems[0] != 'refs' or elems[1] != 'heads':
            print "elems improperly formatted", elems
            return None
        else:
            return elems[2]

    def is_hash(self, hashstr):
        """
        Determine if the hashstr is a valid sha1 hash
        """
        if len(hashstr) == 40:
            try:
                base64.b64decode(hashstr)
                return True
            except Exception, ex:
                pass
        return False


class GITConfig(object):
    """
    Configuration information about an SVN repository for a component
    of code. The configuration we maintain is specific to ROS
    toolchain concepts and is not a general notion of SVN configuration.

     * repo_uri: base URI of repo
     * dev_branch: git branch the code is developed
     * distro_tag: a tag of the latest released code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
     """

    def __init__(self):
        self.type = 'git'
        self.repo_uri      = None
        self.dev_branch    = None
        self.distro_tag    = None
        self.release_tag   = None

    def __eq__(self, other):
        return self.repo_uri == other.repo_uri and \
            self.dev_branch == other.dev_branch and \
            self.release_tag == other.release_tag and \
            self.distro_tag == other.distro_tag
