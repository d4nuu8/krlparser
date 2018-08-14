#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class _Tokens:
    def __init__(self):
        self.STRING = "STRING"
        self.NAME = "NAME"
        self.INTEGER = "INTEGER"
        self.REAL = "REAL"
        self.NEWLINE = "NEWLINE"
        self.END_OF_FILE = "END_OF_FILE"
        self.LEFT_BRACE = "LEFT_BRACE"
        self.RIGHT_BRACE = "RIGHT_BRACE"
        self.LEFT_SQUARE_BRACE = "LEFT_SQUARE_BRACE"
        self.RIGHT_SQUARE_BRACE = "RIGHT_SQUARE_BRACE"
        self.LEFT_CURLY_BRACE = "LEFT_CURLY_BRACE"
        self.RIGHT_CURLY_BRACE = "RIGHT_CURLY_BRACE"
        self.PLUS = "PLUS"
        self.MINUS = "MINUS"
        self.STAR = "STAR"
        self.SLASH = "SLASH"
        self.DOT = "DOT"
        self.COMMA = "COMMA"
        self.COLON = "COLON"
        self.HASH = "HASH"
        self.EQUAL = "EQUAL"
        self.EQUAL_EQUAL = "EQUAL_EQUAL"
        self.LESS = "LESS"
        self.GREATER = "GREATER"
        self.COMMENT = "COMMENT"
        self.FILE_ATTRIBUTE = "FILE_ATTRIBUTE"
        self.ERROR_TOKEN = "ERROR_TOKEN"
tokens = _Tokens()
