#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
src_file: (mod_def | fnc_def)+

mod_def: NEWLINE* (GLOBAL)? DEF ID LPAREN parameters RPAREN NEWLINE*
         END NEWLINE*

fnc_def: NEWLINE* (GLOBAL)? DEFFCT ID ID LPAREN parameters RPAREN NEWLINE*
         END NEWLINE*

parameters: (parameter (COMMA parameter)*)*

parameter: ID COLON (IN | OUT)
"""


class _Keywords:
    GLOBAL = "GLOBAL"
    DEF = "DEF"
    DEFFCT = "DEFFCT"
    IN = "IN"
    OUT = "OUT"
    END = "END"
    ENDFCT = "ENDFCT"

    def __setattr__(self, *_):
        raise TypeError("Attribute is readonly!")

KEYWORDS = _Keywords()


class _Tokens:
    ID = "ID"
    STRING = "STRING"
    INTEGER = "INTEGER"
    REAL = "REAL"
    NEWLINE = "NEWLINE"
    END_OF_FILE = "END_OF_FILE"
    LEFT_BRACE = "("
    RIGHT_BRACE = ")"
    LEFT_SQUARE_BRACE = "["
    RIGHT_SQUARE_BRACE = "]"
    LEFT_CURLY_BRACE = "{"
    RIGHT_CURLY_BRACE = "}"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    DOT = "."
    COMMA = ","
    COLON = ":"
    HASH = "#"
    EQUAL = "="
    EQUAL_EQUAL = "=="
    LESS = "<"
    GREATER = ">"
    COMMENT = ";"
    FILE_ATTRIBUTE = "&"
    ERROR_TOKEN = "ERROR_TOKEN"

    def __setattr__(self, *_):
        raise TypeError("Attribute is readonly!")

TOKENS = _Tokens()
