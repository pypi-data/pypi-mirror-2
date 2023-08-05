# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

from eztv import parser
from eztv.utils import readPageContent
from eztv.exceptions import PathNotFound

page = parser.Page(parser.getFrontPageXPath())
pageContent = readPageContent("http://www.eztv.it")

try:
    # parse eztvs mainpage, it returns a list of shows released.
    # each Release object have these attributes:
    #   - releaseName
    #   - downloads - A list of torrent/magnet links
    #   - date - A datetime.date object, with the time of when eztv released the show.
    page.feed(pageContent)
    page.process()
except (PathNotFound, ValueError) as error:
    print(error)
else:
    curdate = None
    for rel in page.matches:
        if curdate != rel.date:
            curdate = rel.date
            print("Date: %s" % curdate)
        print("\t%s" % rel.releaseName)
        for download in rel.downloads:
            print("\t\t- %s" % download)

