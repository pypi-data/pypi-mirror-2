# -*- coding: utf-8 -*-

"""
    bu.errors
    ~~~~~~~~~

    Bu exceptions

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

class BuError(Exception):
    """Base Bu Error Class"""


class SyntaxError(BuError):
    """Error parsing the file"""
    def __init__(self, message, script, line, char):
        message = '%s %s line:%s col:%s' % (message, script.path,
                                            line + 1, char + 1)
        BuError.__init__(self, message)

class UseError(SyntaxError):
    """Trying to use a missing !use"""


class BuildFileNotFound(BuError):
    """When the build script doesn't exist
    """

class TargetNotFound(RuntimeError):
    """When the target doesn't exist
    """

class UndefinedReference(BuError):
    """Attempt to call an undefined reference
    """

