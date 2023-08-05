# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

_monthTranslateTable = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

def getMonth(month):
    if month not in _monthTranslateTable:
        raise ValueError("not a valid month!")
    return _monthTranslateTable[month]

