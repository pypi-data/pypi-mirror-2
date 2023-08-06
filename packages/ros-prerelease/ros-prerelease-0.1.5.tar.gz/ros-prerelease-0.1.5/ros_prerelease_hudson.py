#!/usr/bin/env python
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
# Revision $Id: hudson.py 11053 2010-09-15 01:30:56Z kwc $
# $Author: kwc $

"""
Python API for Hudson

Examples:

    hudson.create_job('empty', EMPTY_CONFIG_XML)
    hudson.disable_job('empty')
    hudson.copy_job('empty', 'empty_copy')
    hudson.enable_job('empty_copy')
    hudson.reconfig_job('empty_copy', RECONFIG_XML)

    hudson.delete_job('empty')
    hudson.delete_job('empty_copy')

    # build a parameterized job
    hudson.build_job('api-test', {'param1': 'test value 1', 'param2': 'test value 2'})
"""

import sys
import urllib2
import urllib
import base64
import traceback

JOB_INFO     = 'job/%(name)s/api/python?depth=0'
Q_INFO       = 'queue/api/python?depth=0'
CREATE_JOB   = 'createItem?name=%(name)s' #also post config.xml
RECONFIG_JOB = 'job/%(name)s/config.xml'
DELETE_JOB   = 'job/%(name)s/doDelete'
ENABLE_JOB   = 'job/%(name)s/enable'
DISABLE_JOB  = 'job/%(name)s/disable'
COPY_JOB     = 'createItem?name=%(to_name)s&mode=copy&from=%(from_name)s'
BUILD_JOB    = 'job/%(name)s/build'
BUILD_WITH_PARAMS_JOB = 'job/%(name)s/buildWithParameters'

#for testing only
EMPTY_CONFIG_XML = """<?xml version='1.0' encoding='UTF-8'?>
<project>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class="vector"/>
  <concurrentBuild>false</concurrentBuild>
  <builders/>
  <publishers/>
  <buildWrappers/>
</project>"""

#for testing only
RECONFIG_XML = """<?xml version='1.0' encoding='UTF-8'?>
<project>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class="vector"/>
  <concurrentBuild>false</concurrentBuild>
<builders> 
    <hudson.tasks.Shell> 
      <command>export FOO=bar</command> 
    </hudson.tasks.Shell> 
  </builders> 
  <publishers/>
  <buildWrappers/>
</project>"""

class HudsonException(Exception): pass

def auth_headers(username, password):
    """
    Simple implementation of HTTP Basic Authentication. Returns the 'Authentication' header value.
    """
    return 'Basic ' + base64.encodestring("%s:%s" % (username, password))[:-1]

class Hudson(object):
    
    def __init__(self, url, username=None, password=None):
        """
        Create handle to Hudson instance.

        @param url: URL of Hudson server
        @type  url: str
        """
        if url[-1] == '/':
            self.server = url
        else:
            self.server = url + '/'
        if username is not None and password is not None:            
            self.auth = auth_headers(username, password)
        else:
            self.auth = None
        
    def get_job_info(self, name):
        try:
            return eval(urllib2.urlopen(self.server + JOB_INFO%locals()).read())
        except:
            raise HudsonException("job[%s] does not exist"%name)
        
    def debug_job_info(self, job_name):
        """
        Print out job info in more readable format
        """
        for k, v in self.get_job_info(job_name).iteritems():
            print k, v

    def hudson_open(self, req):
        """
        Utility routine for opening an HTTP request to a Hudson server. 
        """
        try:
            if self.auth:
                req.add_header('Authorization', self.auth)
            return urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            # Hudson's funky authentication means its nigh impossible to distinguish errors.
            if e.code in [401, 403, 500]:
                raise HudsonException("Error in request. Possibly authentication failed [%s]"%(e.code))
            # right now I'm getting 302 infinites on a successful delete
    
    def get_queue_info(self):
        """
        @return: list of job dictionaries
        """
        return eval(urllib2.urlopen(self.server + Q_INFO).read())['items']

    def copy_job(self, from_name, to_name):
        """
        Copy a Hudson job

        @param from_name: Name of Hudson job to copy from
        @type  from_name: str
        @param to_name: Name of Hudson job to copy to
        @type  to_name: str
        """
        self.get_job_info(from_name)
        self.hudson_open(urllib2.Request(self.server + COPY_JOB%locals(), ''))
        if not self.job_exists(to_name):
            raise HudsonException("create[%s] failed"%(to_name))

    def delete_job(self, name):
        """
        Delete Hudson job permanently.
        
        @param name: Name of Hudson job
        @type  name: str
        """
        self.get_job_info(name)
        self.hudson_open(urllib2.Request(self.server + DELETE_JOB%locals(), ''))
        if self.job_exists(name):
            raise HudsonException("delete[%s] failed"%(name))
    
    def enable_job(self, name):
        """
        Enable Hudson job.

        @param name: Name of Hudson job
        @type  name: str
        """
        self.get_job_info(name)
        self.hudson_open(urllib2.Request(self.server + ENABLE_JOB%locals(), ''))

    def disable_job(self, name):
        """
        Disable Hudson job. To re-enable, call enable_job().

        @param name: Name of Hudson job
        @type  name: str
        """
        self.get_job_info(name)
        self.hudson_open(urllib2.Request(self.server + DISABLE_JOB%locals(), ''))

    def job_exists(self, name):
        """
        @param name: Name of Hudson job
        @type  name: str
        @return: True if Hudson job exists
        """
        try:
            self.get_job_info(name)
            return True
        except:
            return False

    def create_job(self, name, config_xml):
        """
        Create a new Hudson job

        @param name: Name of Hudson job
        @type  name: str
        @param config_xml: config file text
        @type  config_xml: str
        """
        if self.job_exists(name):
            raise HudsonException("job[%s] already exists"%(name))

        headers = {'Content-Type': 'text/xml'}
        self.hudson_open(urllib2.Request(self.server + CREATE_JOB%locals(), config_xml, headers))
        if not self.job_exists(name):
            raise HudsonException("create[%s] failed"%(name))
    
    def reconfig_job(self, name, config_xml):
        """
        Change configuration of existing Hudson job.

        @param name: Name of Hudson job
        @type  name: str
        @param config_xml: New XML configuration
        @type  config_xml: str
        """
        self.get_job_info(name)
        headers = {'Content-Type': 'text/xml'}
        reconfig_url = self.server + RECONFIG_JOB%locals()
        self.hudson_open(urllib2.Request(reconfig_url, config_xml, headers))

    def build_job_url(self, name, parameters=None, token=None):
        """
        @param parameters: parameters for job, or None.
        @type  parameters: dict
        """
        if parameters:
            if token:
                parameters['token'] = token
            return self.server + BUILD_WITH_PARAMS_JOB%locals() + '?' + urllib.urlencode(parameters)
        elif token:
            return self.server + BUILD_JOB%locals() + '?' + urllib.urlencode({'token': token})
        else:
            return self.server + BUILD_JOB%locals()

    def build_job(self, name, parameters=None, token=None):
        """
        @param parameters: parameters for job, or None.
        @type  parameters: dict
        """
        if not self.job_exists(name):
            raise HudsonException("no such job[%s]"%(name))
        return self.hudson_open(urllib2.Request(self.build_job_url(name, parameters, token), ''))        
    
