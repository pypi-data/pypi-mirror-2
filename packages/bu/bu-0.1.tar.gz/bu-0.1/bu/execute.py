# -*- coding: utf-8 -*-

"""
    bu.execute
    ~~~~~~~~~~

    Executing bu files.

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

import execnet

from bu.preproc import preproc_action
from bu.errors import TargetNotFound


explicit_executors = {}


def execute_execnet(action, content, namespace):
    """Execute an action with execnet

    :param action:
        The action to execute
    :param content:
        The preprocessed action content
    :param namespace:
        The namespace to execute in
    """
    obj = '%s_action' % action.name
    module = 'bu.actions.%s' % obj
    exec_mod = __import__(module, None, None, [obj])
    if 'ssh' in namespace:
        gw = execnet.makegateway('ssh=%s' % namespace['ssh'])
    else:
        gw = execnet.makegateway()
    channel = gw.remote_exec(exec_mod)
    channel.send((
        action.name,
        content,
        namespace,
    ))
    out, code = channel.receive()
    channel.waitclose()
    return out.strip(), code


class ExecutionNode(object):
    """A node in the execution graph

    :param action: The action that the node is created from
    """
    def __init__(self, action):
        self.action = action
        self.namespace, self.content = preproc_action(action)

    def __call__(self):
        executor = explicit_executors.get(self.action.name, execute_execnet)
        return executor(self.action, self.content, self.namespace)


class ExecutionQueue(object):

    def __init__(self, script, target_name):
        self.queue = []
        self.script = script
        target = script.targets.get(target_name)
        if target is None:
            raise TargetNotFound('Missing target: %r' % target_name)
        self.add_target(target)

    def add_target(self, target):
        for action in target.actions:
            self.add_action(action)


    def add_action(self, action):
        self.queue.append(ExecutionNode(action))

    def __iter__(self):
        return iter(self.queue)



