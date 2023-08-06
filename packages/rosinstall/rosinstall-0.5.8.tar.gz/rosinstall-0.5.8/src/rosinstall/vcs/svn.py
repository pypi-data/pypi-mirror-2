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
svn vcs support.

New in ROS C-Turtle.
"""

import subprocess
import os
import vcs_base

class SVNClient(vcs_base.VCSClientBase):
    def get_url(self):
        """
        @return: SVN URL of the directory path (output of svn info command), or None if it cannot be determined
        """
        if self.detect_presence():
            output = subprocess.Popen(['svn', 'info', self._path], stdout=subprocess.PIPE).communicate()[0]
            matches = [l for l in output.split('\n') if l.startswith('URL: ')]
            if matches:
                return matches[0][5:]
        return None

    def detect_presence(self):
        return self.path_exists() and os.path.isdir(os.path.join(self._path, '.svn'))

    def exists(self, url):
        """
        @return: True if url exists in repo
        """
        cmd = ['svn', 'info', url]
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return bool(output[0])

    def checkout(self, url, version=''):
        if self.path_exists():
            print >>sys.stderr, "Error: cannot checkout into existing directory"
            return False
            
        cmd = "svn co %s %s %s"%(version, url, self._path)
        if subprocess.call(cmd, shell=True) == 0:
            return True
        return False

    def update(self, version=''):
        if not self.detect_presence():
            return False
        cmd = "svn up %s %s"%(version, self._path)
        if subprocess.call(cmd, shell=True) == 0:
            return True
        return False
        
    def get_vcs_type_name(self):
        return 'svn'


    def get_version(self):
        output = subprocess.Popen(['svn', 'info', self._path], stdout=subprocess.PIPE).communicate()[0]
        matches = [l for l in output.split('\n') if l.startswith('Revision: ')]
        if len(matches) == 1:
            split_str = matches[0].split()
            if len(split_str) == 2:
                return '-r'+split_str[1]
        return None

class SVNConfig(object):
    """
    Configuration information about an SVN repository for a component
    of code. The configuration we maintain is specific to ROS
    toolchain concepts and is not a general notion of SVN configuration.

     * dev: where the code is developed
     * distro_tag: a tag of the code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
    """
    
    def __init__(self):
        self.type = 'svn'
        self.dev = None
        self.distro_tag = None
        self.release_tag = None

        # anonymously readable version of URLs above. Some repos have
        # separate URLs for read-only vs. writable versions of repo
        # and many tools need to be able to read repos without
        # providing credentials.
        self.anon_dev         = None
        self.anon_distro_tag  = None
        self.anon_release_tag = None

    def __eq__(self, other):
        return self.dev == other.dev and \
            self.distro_tag == other.distro_tag and \
            self.release_tag == other.release_tag and \
            self.anon_dev == other.anon_dev and \
            self.anon_distro_tag == other.anon_distro_tag and \
            self.anon_release_tag == other.anon_release_tag

    def __repr__(self):
        return "{dev: '%s', distro-tag: '%s', 'release-tag': '%s', anon-dev: '%s', anon-distro-tag: '%s', anon-release-tag: '%s'}"%(self.dev, self.distro_tag, self.release_tag, self.anon_dev, self.anon_distro_tag, self.anon_release_tag)
