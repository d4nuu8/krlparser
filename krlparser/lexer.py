#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import string

from .token import Token, TOKENS, KEYWORDS


class Lexer:
    FIRST_CHARACTERS_ID = list(string.ascii_letters) + ["$", "_"]

    CHARACHTERS_ID = FIRST_CHARACTERS_ID + list(string.digits)

    NUMBER_CHARACTERS = list(string.digits) + ["E", "e", ".", "+", "-"]

    @property
    def _token_mapping(self):
        def operator(token):
            return self._create_token_at_position(token, self._current_char)

        return {
            ";": self._comment,
            "&": self._file_attribute,
            "\"": self._string,
            "(": lambda: operator(TOKENS.LEFT_BRACE),
            ")": lambda: operator(TOKENS.RIGHT_BRACE),
            "[": lambda: operator(TOKENS.LEFT_SQUARE_BRACE),
            "]": lambda: operator(TOKENS.RIGHT_SQUARE_BRACE),
            "{": lambda: operator(TOKENS.LEFT_CURLY_BRACE),
            "}": lambda: operator(TOKENS.RIGHT_CURLY_BRACE),
            "+": lambda: operator(TOKENS.PLUS),
            "-": lambda: operator(TOKENS.MINUS),
            "*": lambda: operator(TOKENS.STAR),
            "/": lambda: operator(TOKENS.SLASH),
            ".": lambda: operator(TOKENS.DOT),
            ",": lambda: operator(TOKENS.COMMA),
            ":": lambda: operator(TOKENS.COLON),
            "#": lambda: operator(TOKENS.HASH),
            "=": self._equal,
            ">": self._greater,
            "<": self._less
        }

    def __init__(self, *, code):
        if code is None or not isinstance(code, str):
            raise ValueError("Invalid input!")

        self._input = code
        self._pos = 0
        self._line_number = 0
        self._column = 0
        self._current_token = None
        self._current_char = self._input[self._pos] if code else None
        self._error = []

    def generate_tokens(self):
        token_list = []

        while True:
            next_token = self._get_next_token()
            if next_token.token_type == TOKENS.END_OF_FILE:
                token_list.append(self._end_of_line())
                token_list.append(next_token)
                return token_list
            token_list.append(next_token)

    def _get_next_token(self):
        token = None

        # Error
        if self._error:
            token = self._error.pop(0)

        # End of file (EOF)
        elif self._current_char is None:
            token = self._end_of_file()

        # End of line (EOL)
        elif self._current_char == os.linesep:
            token = self._end_of_line()

        # Whitespace
        elif self._current_char.isspace():
            self._skip_whitespace()
            token = self._get_next_token()

        # Name
        elif self._current_char in self.FIRST_CHARACTERS_ID:
            token = self._name()

        # Numbers
        elif self._current_char.isdigit() or self._current_char == "'":
            token = self._number()

        else:
            try:
                token = self._token_mapping[self._current_char]()
            except KeyError:
                pass

        if token:
            return token

        # Error
        self._advance()
        return Token(token_type=TOKENS.ERROR_TOKEN,
                     value="Unknown character sequence!",
                     line_number=self._line_number,
                     column=self._column)

    def _advance(self):
        self._pos += 1
        self._column += 1

        if self._pos > len(self._input) - 1:
            self._current_char = None
        else:
            self._current_char = self._input[self._pos]

    def _peek(self):
        if self._pos > len(self._input) - 2:
            return None
        return self._input[self._pos + 1]

    def _end_of_file(self):
        return Token(token_type=TOKENS.END_OF_FILE,
                     value=None,
                     line_number=self._line_number,
                     column=self._column)

    def _end_of_line(self):
        token = Token(token_type=TOKENS.NEWLINE,
                      value=os.linesep,
                      line_number=self._line_number,
                      column=self._column)

        self._advance()
        self._column = 0
        self._line_number += 1
        return token

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _comment(self):
        start = self._column
        return Token(token_type=TOKENS.COMMENT,
                     value=self._read_line(),
                     line_number=self._line_number,
                     column=start)

    def _file_attribute(self):
        start = self._column
        return Token(token_type=TOKENS.FILE_ATTRIBUTE,
                     value=self._read_line(),
                     line_number=self._line_number,
                     column=start)

    def _read_line(self):
        self._advance()

        line = ""
        while (self._current_char is not None and
               self._current_char != os.linesep):
            line += self._current_char
            self._advance()

        return line

    def _read_until(self, terminater):
        value = ""
        while True:
            if self._current_char is None or self._current_char == os.linesep:
                token = Token(token_type=TOKENS.ERROR_TOKEN,
                              value="Unexpected newline!",
                              line_number=self._line_number,
                              column=self._column)
                self._error.append(token)
                return value

            if self._current_char in terminater:
                self._advance()
                return value

            value += self._current_char
            self._advance()

    def _string(self):
        start = self._column
        self._advance()

        return Token(token_type=TOKENS.STRING,
                     value=self._read_until(["\""]),
                     line_number=self._line_number,
                     column=start)

    def _name(self):
        start = self._column
        name = ""
        while (self._current_char is not None and
               self._current_char != os.linesep and
               self._current_char in self.CHARACHTERS_ID):
            name += self._current_char
            self._advance()

        if name.upper() in get_public_attributes(KEYWORDS):
            return Token(token_type=name.upper(),
                         value=name,
                         line_number=self._line_number,
                         column=start)

        return Token(token_type=TOKENS.NAME,
                     value=name,
                     line_number=self._line_number,
                     column=start)

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
                return Token(token_type=TOKENS.INTEGER,
                             value=int(value, base),
                             line_number=self._line_number,
                             column=start)
            except ValueError:
                return Token(token_type=TOKENS.ERROR_TOKEN,
                             value="Invalid syntax!",
                             line_number=self._line_number,
                             column=start)

        value = ""
        while self._current_char in self.NUMBER_CHARACTERS:
            value += self._current_char
            self._advance()

        if any((char in ["E", "e", "."]) for char in value):
            return Token(token_type=TOKENS.REAL,
                         value=float(value),
                         line_number=self._line_number,
                         column=start)

        return Token(token_type=TOKENS.INTEGER,
                     value=int(value),
                     line_number=self._line_number,
                     column=start)

    def _equal(self):
        if self._peek() == "=":
            token = self._create_token_at_position(TOKENS.EQUAL_EQUAL, "==")
            self._advance()
            return token
        return self._create_token_at_position(TOKENS.EQUAL, "=")

    def _greater(self):
        if self._peek() == "=":
            token = self._create_token_at_position(TOKENS.GREATER_EQUAL, ">=")
            self._advance()
            return token
        return self._create_token_at_position(TOKENS.GREATER, ">")

    def _less(self):
        if self._peek() == "=":
            token = self._create_token_at_position(TOKENS.LESS_EQUAL, "<=")
            self._advance()
            return token
        if self._peek() == ">":
            token = self._create_token_at_position(TOKENS.NOT_EQUAL, "<>")
            self._advance()
            return token
        return self._create_token_at_position(TOKENS.LESS, "<")

    def _create_token_at_position(self, token_type, value):
        token = Token(token_type=token_type,
                      value=value,
                      line_number=self._line_number,
                      column=self._column)
        self._advance()
        return token


def get_public_attributes(target):
    return (name for name in dir(target) if not name.startswith("_"))
