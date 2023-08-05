# -*- coding: utf-8 -*-

"""
    bu.parsing
    ~~~~~~~~~~

    Parsing the bu build format.

    :copyright: 2010 Ali Afshar <aafshar@gmail.com> (see AUTHORS)
    :license: LGPL 2 or later (see LICENSE)
"""

import os, re, pkgutil


from bu.model import Script
from bu.errors import SyntaxError, UseError


def external_token(scanner, token):
    return 'EXTERNAL', token


def name_token(scanner, token):
    start, end = scanner.match.span()
    return 'NAME', token, start, end


def quoted_name_token(scanner, token):
    start, end = scanner.match.span()
    return 'NAME', token[1:-1], start, end


def assign_token(scanner, token):
    start, end = scanner.match.span()
    return 'ASSIGN', token, start, end


def line_tokens(token_name):
    def callback(scanner, token, token_name=token_name):
        tokens = line_scanner.scan(token)[0]
        return (token_name, tokens)
    return callback


# The entire syntax is contained here
# Something is either a NAME, ASSIGN, COMMENT
#
line_scanner = re.Scanner([
    (r"[^\s=!:@\"']+", name_token),
    (r"'[^\n']*'", quoted_name_token),
    (r'"[^\n\"]*"', quoted_name_token),
    (r'=', assign_token),
    (r'\#.*$', None),
    (r'!|@|:', None),
    (r'\s+', None),
    (r'.*', None),
])

scanner = re.Scanner([
    (r'#.+', None),
    (r'^\s*@.+$', line_tokens('REFERENCE')),
    (r'^\s*!.+$', line_tokens('ACTION')),
    (r'[^\s].+:$', line_tokens('TARGET')),
    (r'\s+.+', external_token),
])


def lex(lines):
    for i, line in enumerate(lines):
        token, remainder = scanner.scan(line)
        if token:
            yield token[0], i


def is_token(token, token_name):
    return token[0] == token_name


#def token_name(token):
#    return token[0]


def token_value(token):
    return token[1]


class ParserContext(object):

    def __init__(self):
        self.script = Script()
        self.target = None
        self.action = None

    def create_target(self, name, options):
        self.target = self.script.create_target(name, options)
        self.action = None


class Parser(object):

    def __init__(self, lexer=lex):
        self.lexer = lexer

    def parse(self, lines, as_path=None):
        ctx = ParserContext()
        ctx.script.path = as_path
        for token, lineno in self.lexer(lines):
            token_name, value = token
            handler = getattr(self, '_parse_%s' % token_name)
            handler(ctx, value, lineno)
        return ctx.script

    def parse_path(self, path):
        if not os.path.exists(path):
            return None
        else:
            f = open(path)
            return self.parse(f, as_path=path)

    def parse_string(self, s, as_path='<string>'):
        return self.parse(s.splitlines(), as_path=as_path)

    def parse_pkgutil(self, path):
        try:
            data = pkgutil.get_data('bu.lib', path)
            return self.parse_string(data, as_path='bu/lib/%s' % path)
        except IOError:
            return None

    def _parse_TARGET(self, ctx, tokens, line):
        name, options = self._parse_control(ctx, tokens, line)
        ctx.create_target(name, options)

    def _parse_ACTION(self, ctx, tokens, line):
        name, options = self._parse_control(ctx, tokens, line)
        handler = getattr(self, '_parse_act_%s' % name, None)
        if handler is not None:
            handler(ctx, options, line)
        else:
            ctx.action = ctx.target.create_action(name, options)

    def _parse_REFERENCE(self, ctx, tokens, line):
        name, options = self._parse_control(ctx, tokens, line)
        ref = ctx.target.create_reference(name, options, ctx.script)
        ctx.action = None

    def _parse_EXTERNAL(self, ctx, tokens, line):
        if ctx.target is None:
            raise SyntaxError('Command outside target.', ctx.script, line, 0)
        if ctx.action is None:
            ctx.action = ctx.target.create_action('sh', {})
        if ctx.action.command_indent is None:
            ctx.action.command_indent = self._parse_indent(tokens)
        indent_length = len(ctx.action.command_indent)
        indent = tokens[:indent_length]
        value = tokens[indent_length:]
        if indent != ctx.action.command_indent:
            raise SyntaxError('Mixed indentation inside action.', ctx.script,
                              line, len(indent))
        ctx.action.children.append(value)

    def _parse_control(self, ctx, tokens, lineno):
        """Return a name, options tuple for the tokenised line
        """
        if not tokens or not is_token(tokens[0], 'NAME'):
            raise SyntaxError('Missing target name.',
                              ctx.script, lineno, 0)
        name = token_value(tokens.pop(0))
        options = {}
        pos_count = 0
        while tokens:
            if not is_token(tokens[0], 'NAME'):
                raise SyntaxError('Missing option name',
                                  ctx.script, lineno, tokens[0][2])
            key = token_value(tokens.pop(0))
            if not tokens or is_token(tokens[0], 'NAME'):
                options[pos_count] = key
                pos_count += 1
                continue
            elif is_token(tokens[0], 'ASSIGN'):
                assign = tokens.pop(0)
                if not tokens or not is_token(tokens[0], 'NAME'):
                    raise SyntaxError('Unmatched key value pair %r %r.' %
                        (key, token_value(assign)), ctx.script,
                        lineno, assign[3])
                value = token_value(tokens.pop(0))
                options[key] = value
        return name, options

    def _parse_act_opt(self, ctx, options, line):
        ctx.script.options.update(options)

    def _parse_act_use(self, ctx, options, line):
        path = options[0]
        script = self.parse_path(path)
        if script is None:
            script = self.parse_pkgutil(path)
        if script is None:
            raise UseError('Could not resolve to use %r.' % path,
                            ctx.script, line, 0)
        ctx.script.merge(script)

    def _parse_indent(self, tokens):
        chars = []
        for c in tokens:
            if c in ' \t':
                chars.append(c)
            else:
                break
        return ''.join(chars)


