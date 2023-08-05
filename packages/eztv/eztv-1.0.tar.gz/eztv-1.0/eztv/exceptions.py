# Copyright (c) 2010 Alexander Borgerth
# See LICENSE for details.

"""
Exceptions in use by the eztv package.
"""

class EztvException(Exception):
    """Base exception"""
    pass

class PathNotFound(EztvException):
    """XPath not found exception"""
    pass

