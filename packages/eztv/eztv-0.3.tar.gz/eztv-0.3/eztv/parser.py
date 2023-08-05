# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

from lxml import html

class TableError(Exception):
    pass

class Release(object):

    def __init__(self):
        self.releaseName = None
        self.downloads = []
        self.date = None # released at date.

    def __str__(self):
        s = "%s\n%s\nDownloads:\n" % (self.releaseName, self.date)
        for link in self.downloads:
            s = s + "\t%s\n" % (link)
        return s

    def addDownload(self, link):
        self.downloads.append(link)

class Parser(object):

    FRONT_PAGE_XPATHS = [
        '//table[@class="forum_header_border" and @width="950"]',
        '//table[@class="forum_header_border" and @width="950"]/tbody'
    ]

    def __init__(self, url="http://www.eztv.it"):
        self.url = url
        self.doc = None
        self.currentDate = None

    def _findReleaseTable(self, elem):
        for child in elem.iterchildren():
            if child.text_content().strip() == "Television Show Releases":
                return child
        return None

    def _parseRelease(self, elem):
        rel = Release()

        if elem.get("class") == "forum_space_border":
            self.currentDate = elem.text_content().strip() # make this a real date object!
        else:
            rel.date = self.currentDate
            if elem[0].get("class") == "forum_thread_post":
                name = elem.find_class("epinfo")
                if len(name) >= 1:
                    rel.releaseName = name[0].text_content().strip()
            for link in elem.getchildren()[2].iterlinks():
                rel.addDownload(link[2].strip())
        return rel

    def _findFrontPageXpath(self):
        table = None
        for path in  self.FRONT_PAGE_XPATHS:
            releasePath = self.doc.xpath(path)
            if len(releasePath) > 0:
                table = self._findReleaseTable(releasePath[-1])
                if table is None:
                    continue
        return table

    def parse(self):
        self.doc = html.parse(self.url)
        releases = []
        table = self._findFrontPageXpath()

        if table is None:
            raise TableError("Couldn't find correct table for releases.")

        for sibling in table.itersiblings():
            r = self._parseRelease(sibling)
            if r.releaseName:
                releases.append(r)
        return releases

