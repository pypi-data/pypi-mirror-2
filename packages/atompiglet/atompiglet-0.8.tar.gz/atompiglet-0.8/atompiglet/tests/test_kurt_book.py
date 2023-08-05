#!/usr/bin/env python
# encoding: utf-8
"""
test_kurt_book.py

Created by Keith Fahlgren on Fri Jan 30 19:22:35 PST 2009
Copyright (c) 2009 O'Reilly Media. All rights reserved.
"""

import glob
import os
import re
import shutil
import tempfile

from lxml import etree
from nose.tools import *

import atompiglet.kurt 
import atompiglet.rdf as rdf
from atompiglet import NAMESPACES
from atompiglet.auth import BasicAuth 
from atompiglet.server import Server
from atompiglet.errors import ServerError

class TestKurtBook:
    def setup(self):
        self.kurt_auth = BasicAuth('orm','123456789')
        self.prod_server = Server(Server.KURT, auth=self.kurt_auth)
        self.prod_orm_wksp = self.prod_server.workspaces["O'Reilly Media"]
        self.prod_books_coll = self.prod_orm_wksp.collections["Books"]
        sql_pg_2e_urn = "urn:x-domain:oreilly.com:product:9780596526887.IP"
        self.sql_pg_2e_book_entry = rdf.entry_from_unique_urn(self.prod_server, self.prod_books_coll, sql_pg_2e_urn)
        self.sql_pg_2e_kurt_book = atompiglet.kurt.Book(self.sql_pg_2e_book_entry, self.prod_server)

        http_pref_urn = "urn:x-domain:oreilly.com:product:9781565928626.IP"
        self.http_pref_book_entry = rdf.entry_from_unique_urn(self.prod_server, self.prod_books_coll, http_pref_urn)
        self.http_pref_kurt_book = atompiglet.kurt.Book(self.http_pref_book_entry, self.prod_server)

        self.to_delete = []
        self.to_clean = []
        self.tempdir = tempfile.mkdtemp('kurt_books_dumpy')

    def test_book_create(self):
        """Book objects for working with Kurt's collections of DocBook content should be createable."""
        kurt_book = atompiglet.kurt.Book(self.sql_pg_2e_book_entry, self.prod_server)
        assert(kurt_book)

    def test_book_remove_kurt_ids(self):
        """Book objects should allow the kurt:ids to be removed from the content."""
        self.sql_pg_2e_kurt_book.remove_kurt_ids()
        kurt_ids_remaining = self.sql_pg_2e_kurt_book.docbook.etree.xpath('//@kurt:id', namespaces=NAMESPACES)
        assert_equal(0, len(kurt_ids_remaining))

    def test_book_dumpfile_bookfile_size(self):
        """Book objects should be able to be dumped to a directory as a set of files (XML + images)."""
        bookfile, _ = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir)
        self.to_clean.append(bookfile)
        min_size = 1000
        dumpfile_size = os.path.getsize(bookfile)
        assert(dumpfile_size > min_size)

    def test_book_dumpfile_image_dir(self):
        """An image file should exist in the requested subdirectory."""
        subdir = 'figs'
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir, figs_subdir=subdir)
        expected = len(self.sql_pg_2e_kurt_book.docbook.filerefs) 
        figs_dir = os.path.join(dumpeddir, subdir)
        num_files = len(glob.glob(figs_dir + '/*.*'))
        assert_equal(expected, num_files)

    def test_book_dumpfile_image_count(self):
        """An image file should exist for each @fileref from the Book after dumping to a directory."""
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir)
        min_files = len(self.sql_pg_2e_kurt_book.docbook.filerefs) + 1 # for the bookfile, duh
        num_files = len(glob.glob(dumpeddir + '/*.*'))
        assert(num_files >= min_files)

    def test_book_dumpfile_image_exclude_print(self):
        """Book objects should be able to be dumped to a directory with filters on which of the images will be downloaded (web)."""
        webbish = atompiglet.kurt.Book.WEB_IMAGE_CONTENT_TYPES
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir, allowed_image_content_types=webbish)
        pdf_files = glob.glob(dumpeddir + '/*.pdf')
        assert(not(pdf_files))

    def test_book_dumpfile_image_exclude_web(self):
        """Book objects should be able to be dumped to a directory with filters on which of the images will be downloaded (print)."""
        printish = atompiglet.kurt.Book.PRINT_IMAGE_CONTENT_TYPES
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir, allowed_image_content_types=printish)
        jpg_files = len(glob.glob(dumpeddir + '/*.jpg'))
        assert(not(jpg_files))

    def test_book_dumpfile_image_exclude_print_regression(self):
        """All web images in kurt should be downloaded."""
        expected = 6 # Five web images (PNG, JPG, GIF) in kurt, plus 1 bookfile 
        webbish = atompiglet.kurt.Book.WEB_IMAGE_CONTENT_TYPES
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir, allowed_image_content_types=webbish)
        image_files = len(glob.glob(dumpeddir + '/*'))
        assert_equal(expected, image_files)

    def test_book_dumpfile_image_exclude_web_regression(self):
        """All print images in kurt should be downloaded"""
        expected = 5 # Four print images (PDF, GIF) in kurt, plus 1 bookfile 
        printish = atompiglet.kurt.Book.PRINT_IMAGE_CONTENT_TYPES
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir, allowed_image_content_types=printish)
        image_files = len(glob.glob(dumpeddir + '/*'))
        assert_equal(expected, image_files)

    def test_book_dumpfile_filerefs_exist(self):
        """An image file should exist at the filename specified by the @fileref inside the Book after dumping to a directory."""
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir)
        min_size = 1
        for filename in self.sql_pg_2e_kurt_book.docbook.filerefs:
            full_filename = os.path.join(dumpeddir, filename)
            dumpfile_size = os.path.getsize(full_filename)
            assert(dumpfile_size > min_size)

    def test_book_dumpfile_filerefs_exist_with_filter_regression(self):
        """An image file should exist at the filename specified by the @fileref inside the Book after dumping to a directory for anything not filtered."""
        webbish = atompiglet.kurt.Book.WEB_IMAGE_CONTENT_TYPES
        bookfile, dumpeddir = self.http_pref_kurt_book.dump_book(dumpdir=self.tempdir)
        min_size = 1
        for filename in self.http_pref_kurt_book.docbook.filerefs:
            _, ext = os.path.splitext(filename)
            if ext != '.pdf':
                full_filename = os.path.join(dumpeddir, filename)
                dumpfile_size = os.path.getsize(full_filename)
                assert(dumpfile_size > min_size)

    def test_book_dumpfile_filerefs_exist_basename_regression(self):
        """Book objects should use relative @filerefs after dumping to a directory."""
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir)
        for filename in self.sql_pg_2e_kurt_book.docbook.filerefs:
            basename = os.path.basename(filename)
            assert_equal(filename, basename)

    def test_book_dumpfile_prettyness(self):
        """Book objects should only dump files with nice names."""
        bookfile, dumpeddir = self.sql_pg_2e_kurt_book.dump_book(dumpdir=self.tempdir)
        non_words = re.compile('\W')
        for filename in glob.glob(dumpeddir + '/*.*'):
            root, _ = os.path.splitext(filename)
            basename = os.path.basename(root)
            assert(not(non_words.match(basename)))


    def teardown(self):
        no_clean = False
        if no_clean:
            for file in self.to_clean:
                print "Not deleting file %s" % file
            for d in self.to_delete:
                print "Not deleting entry at %s" % d.location
        else:
            for d in self.to_delete:
                try:
                    d.delete()
                except Exception, e:    
                    print "Warning: %s could not be deleted (%s)!" % (d.location, e)

            for file in self.to_clean:
                try:
                    os.remove(file)
                except Exception, e:
                    print "Couldn't remove %s during cleanup (%s)" % (file, e)

            shutil.rmtree(self.tempdir)

