# -*- coding: utf-8 -*-

"""
    bu.actions.sh_action
    ~~~~~~~~~~~~~~~~~~~~

    Remote executable execnet module that executes an action with the shell

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)

    .. warning::

        This module is only intendend to be used by execnet's remote_exec call
        which is why the '__channelexec__' name check is made. See
        http://codespeak.net/execnet/example/test_info.html
"""

import os
from subprocess import Popen, PIPE, STDOUT


def bootstrap_ve(ve, content):
    act = os.path.join(ve, 'bin', 'activate')
    return '\n'.join(['source %s' % act, content])


def execute(name, content, namespace):
    """Execute the action as a shell command
    """
    if 've' in namespace:
        content = bootstrap_ve(namespace['ve'], content)
    p = Popen(
        ['bash', '-c', content],
        stdout=PIPE, stderr=STDOUT, stdin=PIPE,
        env=namespace.copy(),
    )
    out, err = p.communicate()
    return out, p.returncode


if __name__ == '__channelexec__':
    channel.send(execute(*channel.receive()))

