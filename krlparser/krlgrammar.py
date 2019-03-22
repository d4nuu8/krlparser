#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class _Keywords:
    GLOBAL = "GLOBAL"
    PUBLIC = "PUBLIC"
    DEF = "DEF"
    DEFFCT = "DEFFCT"
    DEFDAT = "DEFDAT"
    IN = "IN"
    OUT = "OUT"
    END = "END"
    ENDFCT = "ENDFCT"
    ENDDAT = "ENDDAT"

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
