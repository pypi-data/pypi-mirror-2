#!/usr/bin/env python2.6

import os
import sys
import site
import subprocess

from jinja2 import Environment, FileSystemLoader

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

if not os.environ.has_key('MOABASE'):
    raise Exception("MOABASE is undefined")


MOABASE = os.environ['MOABASE']
site.addsitedir(os.path.join(os.environ['MOABASE'], 'lib', 'python'))

import moa.job

#initialize the jinja environment
jenv = Environment(
    loader=FileSystemLoader(
        os.path.join(MOABASE, 'www', 'jinja2')))

def getWebRoot():
    webRoot = os.environ.get('MOAWEBROOT')
    if webRoot[-1] == '/':
        webRoot = webRoot[:-1]
    return webRoot

def getDataRoot():
    dataRoot = os.environ.get('MOADATAROOT')
    if dataRoot[-1] == '/':
        dataRoot = dataRoot[:-1]
    return dataRoot

def getLocalDir():
    requestUri = os.environ.get('REQUEST_URI')
    dataRoot = getDataRoot()
    webRoot = getWebRoot()

    if requestUri.find(webRoot) != 0:
        return False
    moadir = dataRoot + requestUri[len(webRoot):]
    if '?' in moadir:
        moadir = moadir[:moadir.index('?')]
    return moadir

def getDescription(cwd):
    dfile = os.path.join(cwd, 'moa.description')
    if not os.path.exists(dfile):
        return ""
    else:
        description = open(dfile).read()
        #convert from jinja-markdown to html!
        p = subprocess.Popen("pandoc -f markdown -t html".split(),
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(description)
        html,err = p.communicate()
        return html
        
def getBreadCrumbs():
    ## Prepare breadcrumbs
    dataRoot = getDataRoot()
    if moacwd.find(dataRoot) != 0:
        blocks = [{'name' : moacwd,
                   'class' : 'moaBreadCrumb',
                   'link' : requestUri,
                   'notlast' : True}]
    else:
        webRoot = getWebRoot()
        pathUntilNow = webRoot
        steps = moacwd[len(dataRoot)+1:].split('/')

        blocks = [{'name' : webRoot,
                   'class' : 'moaBreadCrumb',
                   'link' : webRoot,
                   'notLast' : True }]

        if len(steps) > 1:        
            for r in steps[:-1]:
                pathUntilNow += '/' + r
                blocks.append({'name' : r,
                               'class' : 'moaBreadCrumb',
                               'link' : pathUntilNow,
                               'notLast' : True })

        blocks[-1]['class'] += ' moaBreadCrumbActive'
        blocks[-1]['notLast'] = False
    return blocks

d = {'MOABASE' : MOABASE}
moacwd = getLocalDir()
d['requestUri'] = os.environ.get('REQUEST_URI')
d['moacwd'] = moacwd
d['status'] = 'notmoa'
d['dataRoot'] = getDataRoot()
d['webRoot'] = getWebRoot()
d['blocks']  = getBreadCrumbs()
d['jobDescription'] = getDescription(moacwd)
#Fire off a generic page without any information if this is not a Moa dir
sys.stderr.write("getting a job for %s" % moacwd)
job = moa.job.Job(moacwd)
sys.stderr.write("found a job? %s %s" % (job, job.template.name))
if job.template.name == 'nojob':
    pageTemplate = jenv.get_template('notMoa.html')
    print pageTemplate.render(**d)
    sys.exit()

#ok, this must be a moa directory: gather information
d['job'] = job
d['status'] = 'moa'
pageTemplate = jenv.get_template('Moa.html')
print pageTemplate.render(**d)
