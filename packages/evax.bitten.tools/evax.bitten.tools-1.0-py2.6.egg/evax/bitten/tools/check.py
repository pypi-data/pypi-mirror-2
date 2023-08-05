# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
#
# Copyright (C) 2010 Evax Software <contact@evax.fr>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at
# http://www.evax.fr/open-source-software/evax.bitten.tools#license

__docformat__ = 'restructuredtext en'

from bitten.build import FileSet
from bitten.util import xmlio
import os
from xml.dom import minidom
from xml.parsers.expat import ExpatError

def get_xml_value(elem, sub_elem):
    """ xml helper function """
    return elem.getElementsByTagName(sub_elem)[0].firstChild.data

def check(ctxt, reports=None):
    """ Analyse the xml output from check and integrate it in the report.

    :param ctxt: the build context
    :type ctxt: `Context`
    :param reports: a glob pattern matching the check xml repports
    """
    assert reports, 'Missing required attribute "reports"'

    results = xmlio.Fragment()

    for filename in FileSet(ctxt.basedir, reports, None):
        try:
            xmldoc = minidom.parse(os.path.join(ctxt.basedir, filename))
        except ExpatError:
            continue
        for suite in xmldoc.getElementsByTagName('suite'):
            # not used by bitten yet
            #suite_name = get_xml_value(suite, 'title')
            for test in suite.getElementsByTagName('test'):
                desc = get_xml_value(test, 'description')
                tid = get_xml_value(test, 'id')
                result = test.attributes['result'].value
                results.append(xmlio.Element('test', fixture=desc,
                                             name=tid, status=result))
    ctxt.report('test', results)
