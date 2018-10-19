#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .krlgrammar import TOKENS, KEYWORDS
from .ast import FunctionDefinition

class Parser:
    def __init__(self, lexer):
        self._ast = []
        self._tokens = lexer.generate_tokens()
        self._position = 0
        self._current_token = self._tokens[self._position]

    @property
    def ast(self):
        return self._ast

    def parse(self):
        self._mod_def()

    def _eat(self, token_type):
        if self._current_token.token_type == token_type:
            token = self._current_token
            self._advance()
            return token

        raise Exception("Invalid syntax!")

    def _advance(self):
        self._position += 1

        if self._position > len(self._tokens) - 1:
            self._current_token = None
        else:
            self._current_token = self._tokens[self._position]

    def _mod_def(self):
        global_definition = False
        if self._current_token.token_type == KEYWORDS.GLOBAL:
            self._eat(KEYWORDS.GLOBAL)
            global_definition = True

        if self._current_token.token_type == KEYWORDS.DEF:
            self._eat(KEYWORDS.DEF)

            name = self._eat(TOKENS.ID)
            self._eat(TOKENS.LEFT_BRACE)
            self._eat(TOKENS.RIGHT_BRACE)
            self._eat(TOKENS.NEWLINE)
            self._eat(KEYWORDS.END)

            self._ast.append(FunctionDefinition(name.value, None, None, None, name.line_number))
