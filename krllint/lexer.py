#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import string

from .token import Token
from .krlgrammar import TOKENS

FIRST_CHARACTERS_NAME = list(string.ascii_letters) + ["$", "_"]
CHARACHTERS_NAME = FIRST_CHARACTERS_NAME + list(string.digits)
HEX_CHARACTERS = string.ascii_lowercase[:6] + string.ascii_uppercase[:6]

class Lexer:
    def __init__(self, input):
        if input is None or not isinstance(input, str):
            raise ValueError("Invalid input!")

        self._input = input
        self._pos = 0
        self._line_number = 0
        self._column = 0
        self._current_token = None
        self._current_char = self._input[self._pos] if input else None
        self._error = []

    def generate_tokens(self):
        token_list = []

        while True:
            next_token = self._get_next_token()
            token_list.append(next_token)

            if next_token.token_type == TOKENS.END_OF_FILE:
                return token_list

    def _get_next_token(self):
        # Error
        if self._error:
            return self._error.pop(0)

        # End of file (EOF)
        if self._current_char is None:
            return self._end_of_file()

        # End of line (EOL)
        if self._current_char == os.linesep:
            return self._end_of_line()

        # Whitespace
        if self._current_char.isspace():
            self._skip_whitespace()
            return self._get_next_token()

        # Comment
        if self._current_char == ";":
            return self._comment()

        # File attribute
        if self._current_char == "&":
            return self._file_attribute()

        # String
        if self._current_char == "\"":
            return self._string()

        # Name
        if self._current_char in FIRST_CHARACTERS_NAME:
            return self._name()

        # Numbers
        if self._current_char.isdigit() or self._current_char == "'":
            return self._number()

        # Plus (+)
        if self._current_char == "+":
            return self._create_token_at_position(TOKENS.PLUS, "+")

        # Minus (-)
        if self._current_char == "-":
            return self._create_token_at_position(TOKENS.MINUS, "-")

        # Star (*)
        if self._current_char == "*":
            return self._create_token_at_position(TOKENS.STAR, "*")

        # Slash (/)
        if self._current_char == "/":
            return self._create_token_at_position(TOKENS.SLASH, "/")

        # Dot (.)
        if self._current_char == ".":
            return self._create_token_at_position(TOKENS.DOT, ".")

        # Comma (,)
        if self._current_char == ",":
            return self._create_token_at_position(TOKENS.COMMA, ",")

        # Colon (:)
        if self._current_char == ":":
            return self._create_token_at_position(TOKENS.COLON, ":")

        # Hash (#)
        if self._current_char == "#":
            return self._create_token_at_position(TOKENS.HASH, "#")

        # Equal (=)
        if self._current_char == "=":
            return self._create_token_at_position(TOKENS.EQUAL, "=")

        # Less (<)
        if self._current_char == "<":
            return self._create_token_at_position(TOKENS.LESS, "<")

        # Greater (>)
        if self._current_char == ">":
            return self._create_token_at_position(TOKENS.GREATER, ">")

        # Left brace (()
        if self._current_char == "(":
            return self._create_token_at_position(TOKENS.LEFT_BRACE, "(")

        # Right brace ())
        if self._current_char == ")":
            return self._create_token_at_position(TOKENS.RIGHT_BRACE, ")")

        # Left square brace ([)
        if self._current_char == "[":
            return self._create_token_at_position(TOKENS.LEFT_SQUARE_BRACE, "[")

        # Right square brace (])
        if self._current_char == "]":
            return self._create_token_at_position(TOKENS.RIGHT_SQUARE_BRACE, "]")

        # Left curly brace ({)
        if self._current_char == "{":
            return self._create_token_at_position(TOKENS.LEFT_CURLY_BRACE, "{")

        # Right curly brace (})
        if self._current_char == "}":
            return self._create_token_at_position(TOKENS.RIGHT_CURLY_BRACE, "}")

        self._advance()
        return Token(TOKENS.ERROR_TOKEN, "Unknown character sequence!",
                     self._line_number, self._column)

    def _advance(self):
        self._pos += 1
        self._column += 1

        if self._pos > len(self._input) - 1:
            self._current_char = None
        else:
            self._current_char = self._input[self._pos]

    def _end_of_file(self):
        return Token(TOKENS.END_OF_FILE, None, self._line_number, self._column)

    def _end_of_line(self):
        token = Token(TOKENS.NEWLINE, os.linesep, self._line_number, self._column)

        self._advance()
        self._column = 0
        self._line_number += 1
        return token

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _comment(self):
        start = self._column
        return Token(TOKENS.COMMENT, self._read_line(), self._line_number, start)

    def _file_attribute(self):
        start = self._column
        return Token(TOKENS.FILE_ATTRIBUTE, self._read_line(), self._line_number, start)

    def _read_line(self):
        self._advance()

        line = ""
        while self._current_char is not None and self._current_char != os.linesep:
            line += self._current_char
            self._advance()

        return line

    def _read_until(self, terminater):
        value = ""
        while True:
            if self._current_char is None or self._current_char == os.linesep:
                self._error.append(Token(TOKENS.ERROR_TOKEN, "Unexpected newline!",
                                         self._line_number, self._column))
                return value

            if self._current_char in terminater:
                self._advance()
                return value

            value += self._current_char
            self._advance()

    def _string(self):
        start = self._column
        self._advance()

        return Token(TOKENS.STRING, self._read_until(["\""]),
                     self._line_number, start)

    def _name(self):
        start = self._column
        name = ""
        while (self._current_char is not None and
               self._current_char != os.linesep and
               self._current_char in CHARACHTERS_NAME):
            name += self._current_char
            self._advance()

        return Token(TOKENS.NAME, name, self._line_number, start)

    def _number(self):
        start = self._column

        if self._current_char == "'":
            self._advance()

            base = 10
            if self._current_char in ["H", "h"]:
                base = 16

            if self._current_char in ["B", "b"]:
                base = 2

            self._advance()
            value = self._read_until("'")

            try:
                return Token(TOKENS.INTEGER, int(value, base),
                             self._line_number, start)
            except ValueError:
                return Token(TOKENS.ERROR_TOKEN, "Invalid syntax!",
                             self._line_number, start)

        value = ""
        while (self._current_char is not None and
               self._current_char != os.linesep and
               not self._current_char.isspace()):
            value += self._current_char
            self._advance()

        if any((char in ["E", "e", "."]) for char in value):
            return Token(TOKENS.REAL, float(value), self._line_number, start)

        return Token(TOKENS.INTEGER, int(value), self._line_number, start)

    def _create_token_at_position(self, token_type, value):
        token = Token(token_type, value, self._line_number, self._column)
        self._advance()
        return token
