#-*- coding:utf-8 -*-

"""
Provides functions to handle source code highlighting.
"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name, PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from pydozeoff.conf import settings


def get_style_defs(name="default"):
    """Returns the CSS code used to highlight source code. If the given style
    name isn't found, the default style will be used.
    """
    try:
        return HtmlFormatter(style=name).get_style_defs()
    except:
        return HtmlFormatter().get_style_defs()


def code(language, source_code):
    """Formats the given source code snippet as HTML.
    """
    formatter = HtmlFormatter(**settings["SYNTAX_HIGHLIGHT_OPTIONS"])
    return highlight(source_code, _get_lexer(language, source_code), formatter)


def _get_lexer(language, source_code):
    """Returns the appropriate lexer to parse the given source code snippet.
    """
    try:
        lexer = get_lexer_by_name(language)
    except:
        try:
            lexer = guess_lexer(source_code)
        except:
            lexer = PythonLexer()
    return lexer
