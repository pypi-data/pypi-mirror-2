# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

"""
Main parser for eztv.
"""

from lxml import html
from eztv import utils
from eztv.exceptions import PathNotFound

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

class BaseParser(object):
    """
    Base parser class, implements the bare essentials needed.
    """

    def __init__(self):
        self.document = None

    def feed(self, data):
        """
        Feed data to the parser.

        :parameters:
            data
                A string with data to feed to the parser.
        """
        if len(data) < 0:
            raise ValueError("length of `data' has to be > 0")
        self.document = html.document_fromstring(data)

    def process(self):
        """
        Process the page. Should be implemented by a subclass!
        """
        raise NotImplementedError

def getFrontPageXPath():
    """XPaths for the frontpage of eztv."""
    return ('//table[@class="forum_header_border" and @width="950"]',
            '//table[@class="forum_header_border" and @width="950"]/tbody')

def getShowPageXPath():
    """
    XPaths for the showpage of eztv. ex: http://eztv.it/shows/282/two-and-a-half-men/
    """
    return ('//table[@class="forum_header_noborder"]',
            '//table[@class="forum_header_noborder"]/tbody')

class Page(BaseParser):
    """
    Main parser for http://www.eztv.it.

    We feed data to it, then process it. Then all matches found by the parser
    will be readily available in the matches attribute.
    """
    def __init__(self, xpaths):
        super(Page, self).__init__()
        self.xpaths = xpaths
        self.matches = []
        self.currentDate = None

    def _validateXPathWorks(self):
        """Validate to make sure the xpath works on the page."""
        entities = None
        for path in self.xpaths:
            foundPath = self.document.xpath(path)
            if len(foundPath) > 0:
                entities = foundPath
        if not entities:
            raise PathNotFound("Unable to find any hits for the xpath(s).")
        return entities

    def _processShows(self, entity):
        """Process all show releases on the page."""
        for child in entity.iterchildren():
            if "Show Releases" in child.text_content().strip():
                for sibling in child.itersiblings():
                    self._processOneShow(sibling)

    def _processDownloadLinks(self, entity):
        """Process all download links for a show release."""
        links = []
        for child in entity.iterchildren():
            if child.get("class") == "forum_thread_post" and child.get("align") == "center":
                for link in child.iterlinks():
                    links.append(link)
        return links

    def _processOneShow(self, entity):
        """Processes one show release, and adds itself to matches."""
        rel = Release()
        if entity.get("class") == "forum_space_border":
            self.currentDate = utils.convertToDate(entity.text_content().strip())
        else:
            rel.date = self.currentDate
            name = entity.find_class("epinfo")
            if len(name) >= 1:
                rel.releaseName = name[0].text_content().strip()
                for link in self._processDownloadLinks(entity):
                    rel.addDownload(link[2].strip())
                self.matches.append(rel)

    def process(self):
        """
        Start processing a page.
        """
        entity = self._validateXPathWorks()
        # ugly hack, but we most likely will have found several hits.
        # so lets use last one only!
        if isinstance(entity, list):
            entity = entity[-1]
        self._processShows(entity)

