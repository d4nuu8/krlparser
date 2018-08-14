#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import string

from .token import Token
from .krlgrammar import tokens

FIRST_CHARACTERS_NAME = list(string.ascii_letters) + ["$", "_"]
CHARACHTERS_NAME      = FIRST_CHARACTERS_NAME + list(string.digits)

class Lexer:
    def __init__(self, input):
        self._input = input
        self._pos = 0
        self._line_number = 0
        self._column = 0
        self._current_token = None
        self._current_char = self._input[self._pos]
        self._error = None
  
    def get_next_token(self):
        # Error
        if self._error is not None: return self._error

        # End of file (EOF)
        if self._current_char is None: return self._end_of_file()

        # End of line (EOL)
        if self._current_char == os.linesep: return self._end_of_line()

        # Whitespace
        if self._current_char.isspace(): self._skip_whitespace()

        # Comment
        if self._current_char == ";": return self._comment()

        # File attribute
        if self._current_char == "&": return self._file_attribute()

        # String
        if self._current_char == "\"": return self._string()

        # Name
        if self._current_char in FIRST_CHARACTERS_NAME: return self._name()

        # Plus (+)
        if self._current_char == "+": return self._create_token_at_position(tokens.PLUS, "+")            

        # Minus (-)
        if self._current_char == "-": return self._create_token_at_position(tokens.MINUS, "-")            

        # Star (*)
        if self._current_char == "*": return self._create_token_at_position(tokens.STAR, "*")            

        # Slash (/)
        if self._current_char == "/": return self._create_token_at_position(tokens.SLASH, "/")            

        # Dot (.)
        if self._current_char == ".": return self._create_token_at_position(tokens.DOT, ".")            

        # Comma (,)
        if self._current_char == ",": return self._create_token_at_position(tokens.COMMA, ",")            

        # Colon (:)
        if self._current_char == ":": return self._create_token_at_position(tokens.COLON, ".")            

        # Hash (#)
        if self._current_char == "#": return self._create_token_at_position(tokens.HASH, "#")            

        # Equal (=)
        if self._current_char == "=": return self._create_token_at_position(tokens.EQUAL, "=")            

        # Less (<)
        if self._current_char == "<": return self._create_token_at_position(tokens.LESS, "<")            

        # Greater (>)
        if self._current_char == ">": return self._create_token_at_position(tokens.GREATER, ">")            

        # Left brace (()
        if self._current_char == "(": return self._create_token_at_position(tokens.LEFT_BRACE, "(")            

        # Right brace ())
        if self._current_char == ")": return self._create_token_at_position(tokens.RIGHT_BRACE, ")")            
        
        # Left square brace ([)
        if self._current_char == "[": return self._create_token_at_position(tokens.LEFT_SQUARE_BRACE, "[")            

        # Right square brace (])
        if self._current_char == "]": return self._create_token_at_position(tokens.RIGHT_SQUARE_BRACE, "]")            

        # Left curly brace ({)
        if self._current_char == "{": return self._create_token_at_position(tokens.LEFT_CURLY_BRACE, "{")            

        # Right curly brace (})
        if self._current_char == "}": return self._create_token_at_position(tokens.RIGHT_CURLY_BRACE, "}")            

        return Token(tokens.ERROR_TOKEN, "Unknown character sequence!", self._line_number, self._column)

    def _advance(self):
        self._pos += 1
        self._column += 1

        if self._pos > len(self._input) - 1:
            self._current_char = None
        else:
            self._current_char = self._input[self._pos]

    def _end_of_file(self):
        self._column = 0
        self._line_number += 1
        return Token(tokens.END_OF_FILE, None, self._line_number, self._column)

    def _end_of_line(self):      
        token = Token(tokens.NEWLINE, os.linesep, self._line_number, self._column)

        self._advance()
        self._column = 0
        self._line_number += 1
        return token

    def _skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _comment(self):
        start = self._column
        return Token(tokens.COMMENT, self._read_line(), self._line_number, start)

    def _file_attribute(self):
        start = self._column
        return Token(tokens.FILE_ATTRIBUTE, self._read_line(), self._line_number, start)

    def _read_line(self):
        self._advance()

        line = ""
        while self._current_char is not None and self._current_char != os.linesep:
            line += self._current_char
            self._advance()

        return line

    def _string(self):
        start = self._column
        self._advance()

        string = ""
        while True:
            if self._current_char is None or self._current_char == os.linesep:
                self._error = Token(tokens.ERROR_TOKEN, "Multiline string literals are not supported!", self._line_number, self._column)
                return Token(tokens.STRING, string, self._line_number, start)

            if self._current_char == "\"":
                self._advance()
                return Token(tokens.STRING, string, self._line_number, start)

            string += self._current_char
            self._advance()

    def _name(self):
        start = self._column
        name = ""
        while self._current_char is not None and self._current_char != os.linesep and self._current_char in CHARACHTERS_NAME:
            name += self._current_char
            self._advance()

        return Token(tokens.NAME, name, self._line_number, start)
    
    def _create_token_at_position(self, token_type, value):
        self._advance()
        return Token(token_type, value, self._line_number, self._column)