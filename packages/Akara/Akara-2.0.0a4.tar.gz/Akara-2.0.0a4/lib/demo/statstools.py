# -*- encoding: utf-8 -*-
'''
See also: http://broadcast.oreilly.com/2009/04/data-chef-spss-tripe-consomme.html

----

Python interfaces to R
Create new topic
 
there seems to be many... e.g. RSPython, rpy, and even a redesigned version rpy2 (see http://rpy.sourceforge.net) -- what works well for you, and why?
rsvp 2 days ago
 
My *nix alternative would be to use <<HereDocument scripting with Python and R within a bash script to also get access to the shell as a bonus feature.
rsvp 2 days ago
 
Relatively new interface called "PypeR" -- see http://www.jstatsoft.org/v35/c02/paper for PDF or for the source code http://rinpy.sourceforge.net/
rsvp about 16 hours ago
 
Ryan Rosario gives a walkthrough of his data mining code using RPy2 as interface to R, http://www.bytemining.com/2010/10/accessing-r-from-python-using-rpy2/ -- the video gets going after the first ten minutes (35 minutes total running time). The caveats he points out are worth noting.

(from https://convore.com/rstats/python-interfaces-to-r/ )

'''

from __future__ import with_statement
import sys, time
import urllib, urlparse
import tempfile
import os
import re
import csv
import cgi
from cStringIO import StringIO
from gettext import gettext as _
from itertools import *
from functools import *
from subprocess import *

import amara
from amara.xslt import transform
from amara.xpath.util import simplify
from amara.bindery import html
from amara.lib.util import *
# Requires Python 2.6 or http://code.google.com/p/json/
from amara.thirdparty import json

import akara
from akara.services import simple_service

VAR_PAT = re.compile('VARIABLE\s+LABELS\s+(((\w+)\s+"([^"]+)"\s*)+)\.')
VAR_DEF_PAT = re.compile('(\w+)\s+"([^"]+)"')

VALUE_PAT = re.compile('VALUE\s+LABELS\s+((/(\w+)\s+(\'(\w+)\'\s+"([^"]+)"\s*)+)+)\.')
VALUE_DEF_SET_PAT = re.compile('/(\w+)\s+((\'(\w+)\'\s+"([^"]+)"\s*)+)')
VALUE_DEF_PAT = re.compile('\'(\w+)\'\s+"([^"]+)"')

VALUE_SET_TYPE = 'value_set'
VARIABLE_LABELS_TYPE = 'variable_labels'
VALUE_LABELS_TYPE = 'value_labels'

#R_SCRIPT = '''library(foreign)
#mydata <- read.spss(file='%s')
#write.csv2(mydata)
#'''

R_SCRIPT = '''library(Hmisc)
mydata <- spss.get(file='%s')
write.csv2(mydata)
'''

R_FILE_CMD = akara.module_config(__name__).get('r_command', 'r')

POR_REQUIRED = _("The 'POR' POST parameter is mandatory.")

SERVICE_ID = 'http://purl.org/akara/services/demo/spss.json'
@simple_service('POST', SERVICE_ID, 'spss.json', 'application/json')
def spss2json(body, ctype, **params):
    '''
    Uses GNU R to convert SPSS to JSON
    Optionally tries to guess long labels from an original .SPS file
    
    Requires POST body of multipart/form-data
    
    Sample request:
    curl -F "POR=@foo.por" http://localhost:8880/spss.json
    curl -F "POR=@foo.por" -F "SPSS=@foo.sps" http://localhost:8880/spss.json
    '''
    #curl --request POST -F "POR=@lat506.por" -F "SPSS=@LAT506.SPS" http://labs.zepheira.com:8880/spss.json
    
    #Useful:
    # * [[http://wiki.math.yorku.ca/index.php/R:_Data_conversion_from_SPSS|R: Data conversion from SPSS]]

    body = StringIO(body)
    form = cgi.FieldStorage(fp=body, environ=WSGI_ENVIRON)
    #for k in form:
    #    print >> sys.stderr, (k, form[k][:100])
    por = form.getvalue('POR')
    assert_not_equal(por, None, msg=POR_REQUIRED)
    spss = form.getvalue('SPSS')
    
    (items, varlabels, valuelabels) = parse_spss(por, spss)

    for count, item in enumerate(items):
        #print >> sys.stderr, row
        item['id'] = item['label'] = '_' + str(count)
        item['type'] = VALUE_SET_TYPE

    return json.dumps({'items': items, VARIABLE_LABELS_TYPE: varlabels, VALUE_LABELS_TYPE: valuelabels}, indent=4)


def parse_spss(spss_por, spss_syntax=None):
    '''
    Uses GNU R to convert SPSS to a simple Python data structure
    Optionally tries to guess long labels from an original .SPS file
    '''
    varlabels = {}
    valuelabels = {}
    if spss_syntax:
        matchinfo = VAR_PAT.search(spss_syntax)
        if matchinfo:
            #print >> sys.stderr, matchinfo.groups
            defns = matchinfo.group(1)
            for defn in VAR_DEF_PAT.finditer(defns):
                varlabels[defn.group(1)] = defn.group(2)

        matchinfo = VALUE_PAT.search(spss_syntax)
        defsets = matchinfo.group(1)
        for defset in VALUE_DEF_SET_PAT.finditer(defsets):
            valuelabelset = {}
            for defn in VALUE_DEF_PAT.finditer(defset.group(2)):
                valuelabelset[defn.group(1)] = defn.group(2)
            valuelabels[defset.group(1)] = valuelabelset

    #print >> sys.stderr, varlabels
    #print >> sys.stderr, valuelabels

    #print >> sys.stderr, por[:100]
    #print >> sys.stderr, spss[:100]
    temp = tempfile.mkstemp(suffix=".por")
    os.write(temp[0], spss_por)

    cmdline = R_FILE_CMD
    process = Popen(cmdline, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    
    csvdata, perr = process.communicate(input=R_SCRIPT%temp[1])
    os.close(temp[0])
    os.remove(temp[1])
    if not csvdata:
        print >> sys.stderr, R_SCRIPT%temp[1]
        print >> sys.stderr, perr
        #FIXME: L10N
        raise ValueError('Empty output from the command line.  Probably a failure.  Command line: "%s"'%cmdline)

    def value(k, v):
        if k in valuelabels and v in valuelabels[k]:
            return valuelabels[k][v]
        else:
            return v

    r_reader = csv.DictReader(csvdata.splitlines(), delimiter=';')
    rows = [
        dict(((k, value(k, v.strip())) for (k, v) in row.iteritems()))
        for row in r_reader
    ]

    return (rows, varlabels, valuelabels)

