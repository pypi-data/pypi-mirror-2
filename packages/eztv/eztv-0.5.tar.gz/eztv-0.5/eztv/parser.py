# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

"""
    Main parser for eztv.
"""

import datetime
from lxml import html
from eztv import date

class TableError(Exception):
    """Exception raised when html table not found."""
    pass

class Release(object):
    """
    Keeper of a show release

    - releaseName as obvious as it sounds, is the name of the show given at eztv.it.
    - downloads is a list of torrent/magnet links.
    - date is a datetime.date object.

    The date attribute can only be trusted by what date it was released, it does not know
    at what point of time in that day the show was released as I found that
    irrelevant.
    """

    def __init__(self):
        self.releaseName = None
        self.downloads = []
        self.date = None

    def __str__(self):
        s = "%s\n%s\nDownloads:\n" % (self.releaseName, self.date)
        for link in self.downloads:
            s = s + "\t%s\n" % (link)
        return s

    def addDownload(self, link):
        """
        Append a download link.


        :parameters:
            link
                torrent/magnet link.

        """
        self.downloads.append(link)

class Parser(object):
    """
    Small parser for http://www.eztv.it.

    Class is due to be heavily reworked, but examples of how it currently
    works can be found in the examles/ directory.
    """

    FRONT_PAGE_XPATHS = [
        '//table[@class="forum_header_border" and @width="950"]',
        '//table[@class="forum_header_border" and @width="950"]/tbody'
    ]

    def __init__(self, url="http://www.eztv.it"):
        self.url = url
        self.doc = None
        self.currentDate = None

    def _findReleaseTable(self, elem):
        """Search for release table element."""
        for child in elem.iterchildren():
            if child.text_content().strip() == "Television Show Releases":
                return child
        return None

    def _createDateFromString(self, datestring):
        """
        Create a datetime.date object from a string gotten from eztv.it.
        """
        day, month, year = datestring.split(',')
        day = int(day.split(' ')[2])
        month = date.getMonth(month.strip().lower())
        year = int(year)
        return datetime.date(year, month, day)

    def _parseRelease(self, elem):
        """
        Parse one release from the page.

        :parameters:
            elem
                a <tr> element containing the release
        """
        rel = Release()

        if elem.get("class") == "forum_space_border":
            self.currentDate = self._createDateFromString(
                elem.text_content().strip())
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
        """
        Find what release table works.

        Then use that xpath, to locate the actual table element that we need
        to find each show release.
        """
        table = None
        for path in  self.FRONT_PAGE_XPATHS:
            releasePath = self.doc.xpath(path)
            if len(releasePath) > 0:
                table = self._findReleaseTable(releasePath[-1])
                if table is None:
                    continue
        return table

    def parse(self):
        """
        Simply load the document, may it be locally or remotely and parse it.

        This will be split up later, in the rework of the "parser" class. We
        should not both load, and parse the document in the same function, it's
        just not sane.
        """
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

