# -*- coding: utf-8 -*-

"""
    bu.model
    ~~~~~~~~

    Document object model.

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

from bu.errors import UndefinedReference


def namespace(*options):
    opts = {}
    for o in reversed(options):
        opts.update(o)
    return opts


class NamedNode(object):
    """A node with a name, children, and options
    """

    def __init__(self, name, parents, options):
        self.name = name
        self.parents = parents
        self.children = []
        self.options = options
        self.overrides = {}

    def clone(self):
        clone = self.__class__(self.name, self.parents, self.options)
        clone.children = list(self.children)
        return clone

    def child(self, child_type, name, options, *args, **kw):
        child = child_type(name, [self], options, *args, **kw)
        self.children.append(child)
        return child

    @property
    def ancestors(self):
        for parent in self.parents:
            yield parent
            for ancestor in parent.ancestors:
                yield ancestor

    @property
    def local_namespace(self):
        return namespace(self.overrides, self.options)

    @property
    def namespace(self):
        return namespace(*[self.local_namespace] +
            [a.local_namespace for a in self.ancestors])

    def __repr__(self):
        return '<%s %s (%s) %s>' % (self.__class__.__name__, self.name,
                                 len(self.children), self.options)


class Action(NamedNode):
    """An action"""

    command_indent = None

    @property
    def raw_content(self):
        return '\n'.join(self.children + [''])

    @property
    def actions(self):
        yield self


class Reference(NamedNode):
    """A reference"""

    def __init__(self, name, parents, options, script):
        NamedNode.__init__(self, name, parents, options)
        self.script = script
        self._target = None

    @property
    def actions(self):
        if self._target is None:
            self._generate()
        return self._actions

    def _generate(self):
        target = self.script.targets.get(self.name)
        if target is None:
            raise UndefinedReference('Missing target %r' % self.name)
        if target not in self.ancestors:
            self._target = target.clone_with(self.options)
            self._target.parents.insert(0, self)
            self.children.append(self._target)
            self._actions = self._target.actions
        else:
            self._actions = []



class Target(NamedNode):
    """A target"""

    def create_action(self, name, options):
        return self.child(Action, name, options)

    def create_reference(self, name, options, script):
        return self.child(Reference, name, options, script)

    def clone_with(self, overrides):
        clone = self.clone()
        clone.overrides.update(self.options)
        return clone

    @property
    def actions(self):
        for child in self.children:
            for action in child.actions:
                yield action



class Script(NamedNode):

    def __init__(self):
        NamedNode.__init__(self, None, [], {})
        self.targets = {}

    def add_target(self, target):
        self.children.append(target)
        self.targets[target.name] = target

    def create_target(self, name, options):
        child = self.child(Target, name, options)
        self.targets[name] = child
        return child

    def merge(self, other):
        self.options.update(other.options)
        for target in other.children:
            target.parents.insert(0, self)
            self.add_target(target)





