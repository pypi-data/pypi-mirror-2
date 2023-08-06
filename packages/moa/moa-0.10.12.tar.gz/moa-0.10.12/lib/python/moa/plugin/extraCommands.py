# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
**extraCommands** - Pre & Post commands
---------------------------------------

Allow execution of a bash oneline before & after job completion
"""

import os
import moa.logger as l
import jinja2

def prepare_3(data):
    job = data['job']

    job.template.parameters.precommand = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'A single command to be executed before the main run' + \
                 'starts',
        'type' : 'string'
        }
    job.template.parameters.postcommand = {
        'category' : 'advanced',
        'optional' : True,
        'help' : 'A single command to be executed after the main run ' + \
                 'starts',
        'type' : 'string'
        }


def executeExtraCommand(command, job):
    jobData = job.conf
    for k in job.conf.keys():
        v = job.conf[k]
        if isinstance(v, list):
            os.putenv(k, " ".join(v))
        elif isinstance(v, dict):
            continue
        else:
            os.putenv(k, str(v))            
    template = jinja2.Template(command)
    os.system(template.render(jobData))

def preRun(data):
    """
    If defined, execute the precommand
    """
    job = data['job']
    precommand = str(job.conf['precommand'])
    if precommand:
        l.debug("Executing precommand %s" % precommand)
        executeExtraCommand(precommand, job)

def postRun(data):
    """
    If defined, execute the postCommand
    """
    job = data['job']
    postcommand = str(job.conf['postcommand'])
    if postcommand:
        l.debug("Executing postcommand %s" % postcommand)
        executeExtraCommand(postcommand, job)
