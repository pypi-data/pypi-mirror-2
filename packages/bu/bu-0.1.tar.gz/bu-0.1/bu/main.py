# -*- coding: utf-8 -*-

"""
    bu.main
    ~~~~~~~

    The main bu execution script

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

import argparse


from bu.parsing import Parser
from bu.execute import ExecutionQueue
from bu.output import info, log_action, log_reply, error
from bu.errors import BuError


def load_script(path):
    """Parse and load a script

    :param path: The file path to load
    """
    return Parser().parse_path(path)


def execute_target(script, target):
    """Execute a target in a script

    :param script: The script instance to execute
    :param target: The target to execute
    """
    print_version()
    info('bu', '[%s] @%s build starts' % (script.path, target))
    for exec_node in ExecutionQueue(script, target):
        log_action(exec_node.action)
        out, code = exec_node()
        log_reply(out, code)
    info('bu', '@%s build ends' % target)


def print_targets(script):
    """Print the targets in a script

    :param script: The script to list targets
    """
    print_version()
    info('bu', '[%s] listing targets' % script.path)
    info('local', '')
    for target in sorted(script.targets):
        if not '.' in target and not target.startswith('_'):
            info('  ', target)
    info('import', '')
    for target in sorted(script.targets):
        if '.' in target and not target.startswith('_'):
            info('  ', target)


def print_version():
    """Print the version string
    """
    info('bu', '0.1')


def _run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', '-f',
        default='build.bu',
        help='The file to build'
    )
    parser.add_argument(
        'target', nargs='?',
        help='The target to build'
    )
    parser.add_argument(
        'options', nargs='*',
        metavar='key=value',
        help='The target to build'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List the targets without executing'
    )
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Print the version string and exit'
    )
    args = parser.parse_args()
    if args.version:
        print_version()
    else:
        script = load_script(args.file)
        if args.list:
            print_targets(script)
        elif args.target:
            execute_target(script, args.target)
        else:
            parser.print_help()


def main():
    """Execute bu
    """
    try:
        return _run()
    except BuError, e:
        error(e)


if __name__ == '__main__':
    main()
