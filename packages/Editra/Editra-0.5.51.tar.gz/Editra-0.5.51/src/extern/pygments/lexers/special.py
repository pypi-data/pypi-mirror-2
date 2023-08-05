# -*- coding: utf-8 -*-
"""
    pygments.lexers.special
    ~~~~~~~~~~~~~~~~~~~~~~~

    Special lexers.

    :copyright: 2006-2007 by Georg Brandl.
    :license: BSD, see LICENSE for more details.
"""

import re
import cStringIO

from pygments.lexer import Lexer
from pygments.token import Token, Error, Text
from pygments.util import get_choice_opt


__all__ = ['TextLexer', 'RawTokenLexer']


class TextLexer(Lexer):
    """
    "Null" lexer, doesn't highlight anything.
    """
    name = 'Text only'
    aliases = ['text']
    filenames = ['*.txt']
    mimetypes = ['text/plain']

    def get_tokens_unprocessed(self, text):
        yield 0, Text, text


_ttype_cache = {}

line_re = re.compile('.*?\n')

class RawTokenLexer(Lexer):
    """
    Recreate a token stream formatted with the `RawTokenFormatter`.  This
    lexer raises exceptions during parsing if the token stream in the
    file is malformed.

    Additional options accepted:

    `compress`
        If set to ``"gz"`` or ``"bz2"``, decompress the token stream with
        the given compression algorithm before lexing (default: ``""``).
    """
    name = 'Raw token data'
    aliases = ['raw']
    filenames = []
    mimetypes = ['application/x-pygments-tokens']

    def __init__(self, **options):
        self.compress = get_choice_opt(options, 'compress',
                                       ['', 'none', 'gz', 'bz2'], '')
        Lexer.__init__(self, **options)

    def get_tokens(self, text):
        if self.compress == 'gz':
            import gzip
            gzipfile = gzip.GzipFile('', 'rb', 9, cStringIO.StringIO(text))
            text = gzipfile.read()
        elif self.compress == 'bz2':
            import bz2
            text = bz2.decompress(text)

        # do not call Lexer.get_tokens() because we do not want Unicode
        # decoding to occur, and stripping is not optional.
        text = text.strip('\n') + '\n'
        for i, t, v in self.get_tokens_unprocessed(text):
            yield t, v

    def get_tokens_unprocessed(self, text):
        length = 0
        for match in line_re.finditer(text):
            try:
                ttypestr, val = match.group().split('\t', 1)
            except ValueError:
                val = match.group().decode(self.encoding)
                ttype = Error
            else:
                ttype = _ttype_cache.get(ttypestr)
                if not ttype:
                    ttype = Token
                    ttypes = ttypestr.split('.')[1:]
                    for ttype_ in ttypes:
                        if not ttype_ or not ttype_[0].isupper():
                            raise ValueError('malformed token name')
                        ttype = getattr(ttype, ttype_)
                    _ttype_cache[ttypestr] = ttype
                val = val[2:-2].decode('unicode-escape')
            yield length, ttype, val
            length += len(val)
