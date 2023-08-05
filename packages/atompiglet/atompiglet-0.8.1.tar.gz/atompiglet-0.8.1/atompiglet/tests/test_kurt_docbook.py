#!/usr/bin/env python
# encoding: utf-8
"""
test_kurt_docbook.py

Created by Keith Fahlgren on Fri Jan 30 19:22:35 PST 2009
Copyright (c) 2009 O'Reilly Media. All rights reserved.
"""

import os

from lxml import etree
from nose.tools import *

import atompiglet.kurt 
from atompiglet import NAMESPACES
from atompiglet.auth import BasicAuth 
from atompiglet.server import Server
from atompiglet.errors import ServerError

class TestKurtDocBook:
    def setup(self):
        self.testfiles_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))
        self.sql_pg_2e_xml = os.path.join(self.testfiles_dir, 'sql_pg_2e.xml')
        self.http_pref_pure_kurt_xml = os.path.join(self.testfiles_dir, 'http_pref.xml')

    def test_docbook_create(self):
        """DocBook objects for working with DocBook content from files should be createable."""
        db = atompiglet.kurt.DocBook(self.http_pref_pure_kurt_xml)
        assert(db)

    def test_docbook_create_already_parsed(self):
        """DocBook objects for working with DocBook content from Trees should be createable."""
        db_tree = etree.parse(self.sql_pg_2e_xml)
        db = atompiglet.kurt.DocBook(db_tree)
        assert(db)

    def test_docbook_filerefs(self):
        """DocBook objects should return a list of their current @filerefs."""
        db = atompiglet.kurt.DocBook(self.sql_pg_2e_xml)
        num_filerefs = len(db.filerefs)
        expected_filerefs = 6
        assert_equal(expected_filerefs, num_filerefs)

    def test_docbook_filerefs_regression(self):
        """DocBook objects should return a list of their current @filerefs even if the content is in the raw Digital Content Warehouse form."""
        db = atompiglet.kurt.DocBook(self.http_pref_pure_kurt_xml)
        num_filerefs = len(db.filerefs)
        expected_filerefs = 16
        assert_equal(expected_filerefs, num_filerefs)
