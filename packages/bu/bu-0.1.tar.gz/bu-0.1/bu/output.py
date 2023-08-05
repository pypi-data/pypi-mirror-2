# -*- coding: utf-8 -*-

"""
    bu.output
    ~~~~~~~~~

    Shell Output and general abuse of the logging module.

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

import logging

from bu.preproc import preproc_action


logging.basicConfig(level=logging.DEBUG,
    format='%(name)s: %(message)s')


def info(prefix, content):
    log = logging.getLogger(prefix)
    log.info(content)


def error(e):
    log = logging.getLogger(e.__class__.__name__)
    log.error(str(e))


def log_lines(lines, level=info):
    for i, line in enumerate(lines):
        level(str(i + 1).rjust(8), line)


def _flatten_options(options):
    return '{%s}' % ' '.join('%s=%s' % i for i in options.items())


def log_action(action):
    info(action.name, _flatten_options(action.options))
    namespace, content = preproc_action(action)
    log_lines(content.splitlines())


def log_reply(data, code):
    info('>>', '%s' % code)
    lines = data.strip().splitlines()
    log_lines(lines)

