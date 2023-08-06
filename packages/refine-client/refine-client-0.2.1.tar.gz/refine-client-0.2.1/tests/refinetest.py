#!/usr/bin/env python
"""
refinetest.py

RefineTestCase is a base class that loads Refine projects specified by
the class's 'project_file' attribute and provides a 'project' object.

These tests require a connection to a Refine server either at
http://127.0.0.1:3333/ or by specifying environment variables REFINE_HOST
and REFINE_PORT.
"""

# Copyright (c) 2011 Paul Makepeace, Real Programmers. All rights reserved.

import os
import unittest

from google.refine import refine

PATH_TO_TEST_DATA = os.path.join('tests', 'data')


class RefineTestCase(unittest.TestCase):
    project_file = None
    project_file_options = {}
    project = None
    # Section "2. Exploration using Facets": {1}, {2}

    def project_path(self):
        return os.path.join(PATH_TO_TEST_DATA, self.project_file)

    def setUp(self):
        self.server = refine.RefineServer()
        self.refine = refine.Refine(self.server)
        if self.project_file:
            self.project = self.refine.new_project(
                self.project_path(), **self.project_file_options)

    def tearDown(self):
        if self.project:
            self.project.delete()
            self.project = None

    def assertInResponse(self, expect):
        try:
            desc = self.project.history_entry.description
            self.assertTrue(expect in desc)
        except AssertionError:
            raise AssertionError('Expecting "%s" in "%s"' % (expect, desc))
