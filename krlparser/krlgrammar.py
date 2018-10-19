#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
mod_def: (GLOBAL)? DEF ID LPAREN parameters RPAREN NEWLINE END
parameters: (parameter (COMMA parameter)*)*
parameter: ID COLON (IN | OUT)
"""


class _Keywords:
    GLOBAL = "GLOBAL"
    DEF = "DEF"
    IN = "IN"
    OUT = "OUT"
    END = "END"

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
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    LEFT_SQUARE_BRACE = "LEFT_SQUARE_BRACE"
    RIGHT_SQUARE_BRACE = "RIGHT_SQUARE_BRACE"
    LEFT_CURLY_BRACE = "LEFT_CURLY_BRACE"
    RIGHT_CURLY_BRACE = "RIGHT_CURLY_BRACE"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    DOT = "DOT"
    COMMA = "COMMA"
    COLON = "COLON"
    HASH = "HASH"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    COMMENT = "COMMENT"
    FILE_ATTRIBUTE = "FILE_ATTRIBUTE"
    ERROR_TOKEN = "ERROR_TOKEN"

    def __setattr__(self, *_):
        raise TypeError("Attribute is readonly!")

TOKENS = _Tokens()
