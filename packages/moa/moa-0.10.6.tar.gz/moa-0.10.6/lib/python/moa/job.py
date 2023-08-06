# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.job
-------

"""

import os
import glob
import tempfile

import Yaco

import moa.utils
import moa.logger as l
import moa.template
import moa.jobConf

from moa.sysConf import sysConf


def newJob(wd, template, title, parameters=[], provider=None):
    """
    Create a new job in the wd and return the proper job object
    currently only makefile jobs are supported - later we'll scan the
    template, and instantiate the proper job type

    >>> wd = tempfile.mkdtemp()
    >>> job = newJob(wd, template='blast', title='test')
    >>> assert(isinstance(job, Job))
    >>> assert(job.template.name == 'blast')
    >>> assert(job.conf.title == 'test')
    
    :param wd: Directory to create this job in, note that this
       directory must already exists
    :param template: Template name for this job
    :type template: String
    :type force: Boolean
    :param parameters: A list of parameters to set for this job
    :type parameters: list of (key, value) tuples
    :rtype: instance of :class:`moa.job.Job`
    
    """

    job = Job(wd)
    job.setTemplate(template, provider=provider)
    job.conf.title = title
    for pk, pv in parameters:
        job.conf[pk] = pv
    job.conf.save()
    return job

def newTestJob(template, title="Test job", provider=None):
    """    
    for testing purposes - creates a temporary directory and uses that to
    instantiate a job. This function returns the job object created

    >>> job = newTestJob(template = 'adhoc', title='test title')
    >>> assert(isinstance(job, Job))
    >>> assert(os.path.exists(job.wd))
    >>> assert(job.conf.title == 'test title')
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa')))
    >>> assert(os.path.exists(os.path.join(job.wd, '.moa', 'template')))
    >>> assert(job.template.name == 'adhoc')
    
    :returns: the created job
    :rtype: instance of :class:`moa.job.Job`
    """
    wd = tempfile.mkdtemp()
    job = Job(wd)
    job.setTemplate(template, provider=provider)
    job.conf.title = title
    job.conf.save()
    return job

class Job(object):
    """
    Class defining a single job

    >>> wd = tempfile.mkdtemp()
    >>> job = Job(wd)
    >>> assert(isinstance(job, Job))
    >>> assert(job.template.name == 'nojob')
    
    :param wd: The directory containing the job
    :param template: The template a job should have. If undefined,
        read the template from `./.moa/template`
    :param options: Additional options to feed to this job
    """
      
    def __init__(self, wd):

        if wd[-1] == '/':
            wd = wd[:-1]
        self.wd = wd
        
        self.confDir = os.path.join(self.wd, '.moa')
        self.templateFile = os.path.join(self.confDir, 'template')
        self.backend = None
        self.args = []
        self.env = {}
        #used by the backends to store specific data
        self.data = Yaco.Yaco()

        # a list of globs that defines what is crucial to a Moa job
        # and what is not.
        self.data.moaFiles = [
            '.moa/template',
            '.moa/template.d/*',
            '.moa/config',
            'moa.*'
            ]
        
        self.loadTemplate()

        # then load the job configuration
        self.conf = moa.jobConf.JobConf(self)

    def getFiles(self):
        """
        Return all moa files - i.e. all files crucial to this job.

        """
        rv = set()
        for gl in self.data.moaFiles:
            rv.update(set(glob.glob(os.path.join(self.wd, gl))))

        remove = [x for x in rv if x[-1] == '~']
        rv.difference_update(remove)
        return list(rv)
    
    def hasCommand(self, command):
        """        
        Check if this job defines a certain command

        .. Warning::
            THIS METHOD DOES NOT WORK PROPERLY YET

        >>> job = newTestJob('unittest')
        >>> assert(job.hasCommand('run'))
        >>> assert(job.hasCommand('run2'))
        >>> assert(not job.hasCommand('dummy'))

        """
        if command in self.template.commands.keys():
            return True
        if self.template.backend == 'ruff':
            return self.backend.hasCommand(command)
        else:
            return True

    def checkCommands(self, command):
        """
        Check command, and rearrange if there are delegates.
        
        >>> job = newTestJob('unittest')
        >>> assert(job.template.commands.run.delegate == ['prepare', 'run2'])
        >>> assert(job.checkCommands('run2') == ['run2'])
        >>> assert(job.checkCommands('run') == ['prepare', 'run2'])
        >>> assert(job.checkCommands('prepare') == ['prepare'])
        
        :param commands: The list of commands to check
        :type commands: list of strings
        :returns: The checked list of commands
        :rtype: list of strings
        """        
        rv = []
        if self.template.commands.get(command, {}).has_key('delegate'):
            rv.extend(self.template.commands[command].delegate)
        else:
            rv.append(command)

        return rv

    def checkConfDir(self):
        """
        Check if the configuration directory exists. If not create it.
        
        >>> job = newTestJob('unittest')
        >>> confdir = os.path.join(job.wd, '.moa')
        >>> assert(os.path.exists(confdir))
        >>> import shutil
        >>> shutil.rmtree(confdir)
        >>> assert(os.path.exists(confdir) == False)
        >>> job.checkConfDir()
        >>> assert(os.path.exists(confdir))
        """
        
        if not os.path.exists(self.confDir):
            os.mkdir(self.confDir)

            
    def execute(self, command, verbose=False, silent=False):
        """
        Execute `command` in the context of this job. Execution is
        alwasy deferred to the backend

        #Note: Uncertain how to test verbose & silent

        
        :param command: the command to execute
        :type command: string
        :param verbose: output lots of data
        :type verbose: Boolean        
        :param silent: output nothing
        :type silent: Boolean        

        """

        rc = 0
        
        if not self.backend:
            l.critical("No backend loaded - cannot execute %s" % command)

        ## Ask the job if it's is ok with
        ## the command provided (might want to change order, or insert
        ## stuff
        execList = self.checkCommands(command)
        sysConf.executeCommand = execList

        l.debug("Run moa commands: %s" % ",".join(execList))
        l.debug("with args %s" % sysConf.newargs)

        ### Start job initialization
        self.prepare()

        ### Run plugin initialization step 3 - just before execution
        sysConf.plugins.run('prepare_3')
        sysConf.plugins.run("pre_command")

        #run a prep step if the original command is not in the
        #execlist
        if command not in execList:
            sysConf.plugins.run("pre%s" % command.capitalize())

        #run through all commands...
        for execNow in execList:
            l.info("Executing %s" % execNow)
            sysConf.plugins.run("pre%s" % execNow.capitalize())

            rc = self.backend.execute(
                execNow, verbose = verbose, silent=silent)
            sysConf.rc = rc

            if rc != 0:
                sysConf.plugins.run('postError')
                break
            
            sysConf.plugins.run("post%s" % execNow.capitalize(), reverse=True)

        #likewise if the command is not in the execlist - run a
        #post process 
        if command not in execList:
            sysConf.plugins.run("post%s" % command.capitalize(), reverse=True)

        sysConf.plugins.run("post_command", reverse=True)
        sysConf.plugins.run("finish", reverse=True)

        return rc

    

                    
    def prepare(self):
        """
        Give this job a chance to prepare for execution - deferred to
        the backend.

        >>> job = newTestJob('unittest')
        >>> job.prepare()
        
        """
        if self.backend and getattr(self.backend, 'prepare', None):
            self.backend.prepare()
        
    def defineOptions(self, parser):
        """
        Set command line options - deferred to the backends
        
        >>> job = newTestJob('unittest')
        >>> import optparse
        >>> parser = optparse.OptionParser()
        >>> job.defineOptions(parser)

        """
        if self.backend and getattr(self.backend, 'defineOptions'):
            self.backend.defineOptions(parser)
                
    def refreshTemplate(self):
        """
        Reload the template into the local .moa/template.d directory

        >>> job = newTestJob('unittest')
        >>> templateFile = os.path.join(job.confDir, 'template.d', 'unittest.jinja2')
        >>> assert(os.path.exists(templateFile))
        >>> os.unlink(templateFile)
        >>> assert(not os.path.exists(templateFile))
        >>> job.refreshTemplate()
        >>> assert(os.path.exists(templateFile))
        
        """
        moa.template.refresh(self.wd)
        
    def setTemplate(self, name, provider = None):
        """
        Set a new template for this job

        >>> job = newTestJob('unittest')
        >>> job.setTemplate('adhoc')
        >>> afile = os.path.join(job.confDir, 'template.d', 'adhoc.mk')
        >>> assert(os.path.exists(afile))
        """
        self.checkConfDir()
        l.debug("Setting job template to %s" % name)
        #get the template
        moa.template.installTemplate(self.wd, name, provider = provider)
        self.loadTemplate()
        
    def loadTemplate(self):
        """
        
        Load the template for this job, based on what configuration 
        can be found
        """
        self.template = moa.template.Template(self.templateFile)
        self.loadBackend()
                
    def loadBackend(self):
        """
        load the backend
        """
        backendName = self.template.backend
        l.debug("attempt to load backend %s" % backendName)
        try:
            moduleName = 'moa.backend.%s' % backendName
            module =  __import__( moduleName, globals(),
                                   locals(), [moduleName], -1)            
            l.debug("Successfully Loaded module %s" % moduleName)
        except ImportError, e:
            if str(e) == "No module named %s" % moduleName:
                l.critical("Backend %s does not exists" % backendName)
            l.critical("Error loading backend %s" % backendName)
            raise
            
        self.backend = getattr(module, backendName.capitalize())(self)
        self.initialize()

        
    def isMoa(self):
        """
        Check if this is a Moa directory - Currently, this needs to be overridden
        #weird; uncertain if this ever gets called
        
        """
        if not os.path.exists(os.path.join(self.wd, '.moa')):
            return False
        if self.template.name == 'noJob':
            return False
        return True
                              

    def initialize(self):
        """
        Initialize a new job in the current wd
        """
        if getattr(self.backend, 'initialize', None):
            l.debug("calling backend to initialize template %s" %
                    self.template.name)
            self.backend.initialize()
        


####
# nose tests

