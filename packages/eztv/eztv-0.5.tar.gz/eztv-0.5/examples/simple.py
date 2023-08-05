from eztv import parser

page = parser.Parser(url="http://www.eztv.it")
try:
    # parse eztvs mainpage, it returns a list of shows released.
    # each Release object have these attributes:
    #   - releaseName
    #   - downloads - A list of torrent/magnet links
    #   - date - A datetime.date object, with the time of when eztv released the show.
    releases = page.parse()
except parser.TableError as error:
    print("Unable to parse the page: %s" % error)
else:
    curdate = None
    for rel in releases:
        if curdate != rel.date:
            curdate = rel.date
            print("Date: %s" % curdate)
        print("\t%s" % rel.releaseName)

