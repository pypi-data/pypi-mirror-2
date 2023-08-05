# -*- coding: utf-8 -*-

"""
    bu.preprocessing
    ~~~~~~~~~~~~~~~~

    Preprocessing commands

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

import os

from jinja2 import Template

from bu.model import namespace


GLOBALS = {
    'cwd': os.getcwd,
    'user-agent': 'bu',
}


def global_namespace(ns):
    """Create a namespace including the global values.

    The global namespace includes various useful entities such as the current
    working directory, etc.

    :param ns: The namespace to update as a global namespace.
    """
    gns = {}
    for k, v in GLOBALS.items():
        if callable(v):
            gns[k] = v()
        else:
            gns[k] = v
    return namespace(ns, gns)


def preproc_action(action):
    namespace = preproc_options(global_namespace(action.namespace))
    return namespace, Template(action.raw_content).render(namespace)


def preproc_options(options):
    opts = {}
    for k, v in options.items():
        opts[k] = Template(v).render(global_namespace(options))
    return opts


