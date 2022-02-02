import logging
import sqlparse
from pygments import highlight
from pygments.lexers.sql import MySqlLexer

from pygments.formatters import Terminal256Formatter
from pygments.style import Style
from pygments.token import Token


class SqlLogStyle(Style):
    styles = {
        Token.Keyword: 'ansiyellow',  # Keyword
        Token.Generic: 'ansibrightblue bg:ansibrightred',
        Token.Name: 'ansiwhite',

    }


class Template(logging.Formatter):
    """
    Format and syntax highlight SQL queries for the terminal
    """

    def format(self, record):
        try:
            sql = sqlparse.format(
                record.sql,
                keyword_case='upper',
                identifier_case='lower',
                truncate_strings=75,
                reindent=True).strip('\n')
            sql = '\n\t| '.join([l for l in sql.split('\n')])
            sql = highlight(sql, MySqlLexer(), Terminal256Formatter(style=SqlLogStyle))
            return '({:.3f}) | {}'.format(record.duration, sql)
        except:
            # fall back to the default formatting if anything happens
            return super().format(record)
