# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

"""
Some assorted utility functions.
"""

import datetime
import urllib
import random

from eztv import date

class DandyURLOpener(urllib.FancyURLopener, object):
    """
    Random user-agent.
    """
    # UserAgents taken from http://www.eff.org/deeplinks/2010/01/tracking-by-user-agent.
    browsers = (
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009091010 Iceweasel/3.0.6 (Debian-3.0.6-3)",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7C144 Safari/528.16",
        "BlackBerry9530/4.7.0.148 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/105",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; T-Mobile G1 Build/DRC83) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
    )

    def __init__(self):
        self.version = random.choice(self.browsers)
        super(DandyURLOpener, self).__init__()

def readPageContent(url):
    """
    Read the contents from an URL.

    :parameters:
        url
            URL to the page.
    """
    opener = DandyURLOpener()
    page = opener.open(url)
    return page.read()


def convertToDate(datestring):
    """
    Create a datetime.date object from a string gotten from eztv.it

    Should it fail to parse the date, fallback to use todays date.
    """
    day, month, year = datestring.split(',')
    d = None
    try:
        day = int(day.split(' ')[2])
        year = int(year)
    except ValueError as error:
        d = datetime.datetime.now()
    else:
        month = date.getMonth(month.strip().lower())
        d = datetime.date(year, month, day)
    return d

