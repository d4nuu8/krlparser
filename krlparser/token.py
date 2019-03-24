#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Token:
    def __init__(self, *, token_type, value, line_number, column):
        self.token_type = token_type
        self.value = value
        self.line_number = line_number
        self.column = column

    def __repr__(self):
        value = (self.value
                 if not isinstance(self.value, str)
                 else "\"" + self.value + "\"")

        return (f"Token("
                f"{self.token_type},"
                f"{value},"
                f"{self.line_number},"
                f"{self.column})")

    def __eq__(self, other):
        return (self.token_type == other.token_type and
                self.value == other.value and
                self.line_number == other.line_number and
                self.column == other.column
                )

    def __ne_(self, other):
        return not self == other


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
    NAME = "NAME"
    INTEGER = "INTEGER"
    REAL = "REAL"
    STRING = "STRING"
    COMMENT = "COMMENT"
    FILE_ATTRIBUTE = "FILE_ATTRIBUTE"
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
    NOT_EQUAL = "<>"
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    ERROR_TOKEN = "ERROR_TOKEN"

    def __setattr__(self, *_):
        raise TypeError("Attribute is readonly!")


TOKENS = _Tokens()
