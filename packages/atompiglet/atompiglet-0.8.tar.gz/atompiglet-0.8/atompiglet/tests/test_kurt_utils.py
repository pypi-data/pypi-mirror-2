#!/usr/bin/env python
# encoding: utf-8
"""
test_kurt_utils.py

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
from atompiglet.errors import NotFoundError, ServerError

class TestKurtUtils:
    def setup(self):
        self.testfiles_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))
        self.test_pdf = os.path.join(self.testfiles_dir, 'a_test.pdf')
        self.pdf_mimetype = 'application/pdf' 

        self.to_delete = []

        username = 'orm'
        password = '123456789'
        self.server = Server(Server.TEST_KURT, auth=BasicAuth(username, password))
        self.orm_wksp = self.server.workspaces["O'Reilly Media"]
        self.webpdfs_coll = self.orm_wksp.collections["Web PDFs"]
        self.new_entry = self.webpdfs_coll.add_from_file(self.test_pdf, self.pdf_mimetype)
        self.to_delete.append(self.new_entry)

    def test_kurt_utils_entry_from_atom_id_fail(self):
        """The Kurt utilities should be able return an matching entry from the server given an Atom ID."""
        existing_atom_id = self.new_entry.atom_id
        matching_entry = atompiglet.kurt.Utils.entry_from_atom_id(self.server, existing_atom_id)
        matching_entry_atom_id = matching_entry.atom_id
        assert_equal(existing_atom_id, matching_entry_atom_id)

    def test_kurt_utils_entry_from_atom_id(self):
        """The Kurt utilities should not be able return an matching entry from the server given a bogus Atom ID."""
        bogus_atom_id = 'bogus'
        assert_raises(NotFoundError, atompiglet.kurt.Utils.entry_from_atom_id, self.server, bogus_atom_id)

    def teardown(self):
        for d in self.to_delete:
            try:
                d.delete()
            except:    
                print "%s could not be deleted!" % (d)


