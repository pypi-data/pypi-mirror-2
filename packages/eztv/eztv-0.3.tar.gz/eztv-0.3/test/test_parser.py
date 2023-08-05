# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

import unittest
from eztv.parser import Parser, Release

class TestEztvParser(unittest.TestCase):

    def setUp(self):
        self.page = Parser("test/eztv.html")

    def test_page_should_not_be_none(self):
        self.assertNotEqual(self.page, None)

    def test_page_should_have_url(self):
        self.assertNotEqual(self.page.url, None, "url should not be None")

    def test_parse(self):
        shows = self.page.parse()
        self.assert_(len(shows) > 0, "should have more then 0 shows")
        for show in shows:
            self.assert_(show != None)

    def test_show_should_be_valid(self):
        show = self.page.parse()[0]
        self.assertEqual(len(show.downloads), 4, "should have 4 downloads")
        self.assert_(show.releaseName.startswith("BBC Jimmys"))

