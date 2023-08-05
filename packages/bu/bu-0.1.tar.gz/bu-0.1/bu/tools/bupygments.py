from pygments.lexer import RegexLexer, using, bygroups
from pygments.token import *

from pygments.lexers.text import BashLexer
from pygments.lexers.templates import DjangoLexer

class BuLexer(RegexLexer):
    name = 'Bu'
    aliases = ['bu']
    filenames = ['*.bu']

    tokens = {
        'root': [
            (r'[\t ]*\{%.*?%\}', using(DjangoLexer)),
            (r'[\t ]*\{\{.*?\}\}', using(DjangoLexer)),
            (r'^([\t ]*!)(.+\n)',
                bygroups(Operator, String)),
            (r'^([\t ]*@)(.+\n)',
                bygroups(Operator, Name.Function)),
            (r'(.*)(:\n)', bygroups(Keyword, Operator)),
            (r'.*\n', using(BashLexer)),
        ]
    }

__all__ = ['BuLexer']

