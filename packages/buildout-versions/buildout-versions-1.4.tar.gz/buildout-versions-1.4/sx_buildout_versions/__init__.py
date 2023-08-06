# Copyright (c) 2010 Simplistix Ltd
# See license.txt for license details.

import os
import pkg_resources

from datetime import datetime
from zc.buildout import easy_install
from zc.buildout.easy_install import Installer
from zc.buildout.easy_install import logger
from zc.buildout.easy_install import IncompatibleVersionError

required_by = {}
picked_versions = {}

# code to patch in
def _log_requirement(ws, req):
    for dist in sorted(ws):
        if req in dist.requires():
            req_ = str(req)
            if req_ not in required_by:
                required_by[req_] = set()
            required_by[req_].add(str(dist.as_requirement()))

original_get_dist = Installer._get_dist
def _get_dist(self, requirement, ws, always_unzip):
    dists = original_get_dist(self, requirement, ws, always_unzip)
    for dist in dists:
        if not (dist.precedence == pkg_resources.DEVELOP_DIST or \
                  (len(requirement.specs) == 1 and \
                       requirement.specs[0][0] == '==')):
            picked_versions[dist.project_name] = dist.version
    return dists

def _constrain(self, requirement):
    version = self._versions.get(requirement.project_name.lower())
    if version:
        if version not in requirement:
            logger.error("The version, %s, is not consistent with the "
                         "requirement, %r.", version, str(requirement))
            raise IncompatibleVersionError("Bad version", version)

        requirement = pkg_resources.Requirement.parse(
            "%s[%s] ==%s" % (requirement.project_name,
                           ','.join(requirement.extras),
                           version))

    return requirement

file_name = None

def start(buildout):
    global file_name

    # normalise version case
    current = Installer._versions
    Installer._versions = {}
    for key,value in current.items():
        Installer._versions[key.lower()]=value

    # patch methods
    easy_install._log_requirement = _log_requirement
    Installer._get_dist = _get_dist
    Installer._constrain = _constrain

    # record file name, if needed
    if 'buildout_versions_file' in buildout['buildout']:
        file_name = buildout['buildout']['buildout_versions_file']
    
def finish(buildout):
    # now check that buildout-versions is constrained!
    version_section = buildout['buildout'].get('versions')
    if not (version_section and
            'buildout-versions' in buildout[version_section]):
        picked_versions['buildout-versions']=pkg_resources.require(
            'buildout-versions'
            )[0].version

    if picked_versions:
        output = ['[versions]']
        required_output = []
        for dist_, version in sorted(picked_versions.items()):
            if dist_ in required_by:
                required_output.append('')
                required_output.append('# Required by:')
                for req_ in sorted(required_by[dist_]):
                    required_output.append('# '+req_)
                target = required_output
            else:
                target = output
            target.append("%s = %s" % (dist_, version))

        output.extend(required_output)
        
        print "Versions had to be automatically picked."
        print "The following part definition lists the versions picked:"
        print '\n'.join(output)
        if file_name:
            if os.path.exists(file_name):
                output[:1] = [
                    '',
                    '# Added by Buildout Versions at %s' % datetime.now(),
                    ]
            output.append('')
            f = open(file_name,'a')
            f.write('\n'.join(output))
            f.close()
            print "This information has been written to %r" % file_name
