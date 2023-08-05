# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
#
# Copyright (C) 2010 Evax Software <contact@evax.fr>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at
# http://www.evax.fr/open-source-software/evax.bitten.tools#license

import os
import unittest
import shutil
import tempfile
from bitten.recipe import Context

from evax.bitten.tools.check import check
from evax.bitten.tools.lcov import lcov

class EvaxBittenToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.basedir = os.path.realpath(tempfile.mkdtemp())
        self.ctxt = Context(self.basedir)

    def tearDown(self):
        shutil.rmtree(self.basedir)

class CheckTestCase(EvaxBittenToolsTestCase):
    def test_missing_param_reports(self):
        self.assertRaises(AssertionError, check, self.ctxt)

class LCovTestCase(EvaxBittenToolsTestCase):
    def test_missing_param_directory(self):
        self.assertRaises(AssertionError, lcov, self.ctxt)

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CheckTestCase, 'test'))
    suite.addTest(unittest.makeSuite(LCovTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='get_suite')

