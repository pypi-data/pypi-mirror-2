# -*- coding: utf-8 -*-

"""
    bu.actions.py_action
    ~~~~~~~~~~~~~~~~~~~~

    Remote executable execnet module that executes an action with python

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)

    .. warning::

        This module is only intendend to be used by execnet's remote_exec call
        which is why the '__channelexec__' name check is made. See
        http://codespeak.net/execnet/example/test_info.html
"""


import sys, StringIO, traceback, os


def bootstrap_ve(ve, content):
    act = os.path.join(ve, 'bin', 'activate_this.py')
    script = 'execfile("%s", dict(__file__="%s"))' % (act, act)
    return '\n'.join([script, content])


def execute(name, content, namespace):
    """Execute a python action
    """
    if 've' in namespace:
        content = bootstrap_ve(namespace['ve'], content)
    s = StringIO.StringIO()
    oldout = sys.stdout
    sys.stdout = s
    try:
        code = compile(content + '\n', '<string>', 'exec')
        exec code in namespace.copy(), globals()
        returncode = 0
    except Exception, e:
        traceback.print_exc(file=s)
        returncode = 1
    s.seek(0)
    data = s.read()
    sys.stdout = oldout
    sys.stdout.write(data)
    return data, returncode


if __name__ == '__channelexec__':
    channel.send(execute(*channel.receive()))

