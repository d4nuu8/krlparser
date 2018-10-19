#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .krlgrammar import TOKENS, KEYWORDS
from .ast import FunctionDefinition, Parameter, Type


class ParsingError(Exception):
    def __init__(self, line_number, column, message):
        super().__init__(message)

        self.line_number = line_number
        self.column = column
        self.message = message


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
        self._fnc_def()

        if not self._ast:
            raise self._error("No module or function definition found")

    def _error(self, message):
        token = self._current_token
        raise ParsingError(token.line_number, token.column, message)

    def _eat(self, token_type):
        token = self._current_token
        if token.token_type == token_type:
            self._advance()
            return token

        self._error(f"Expected \"{token_type}\", found \"{token.token_type}\"")

    def _try_eat(self, token_type):
        try:
            self._eat(token_type)
            return True
        except ParsingError:
            return False

    def _is_current_token(self, token_type):
        return self._current_token.token_type == token_type

    def _advance(self):
        self._position += 1

        if self._position > len(self._tokens) - 1:
            self._current_token = None
        else:
            self._current_token = self._tokens[self._position]

    def _mod_def(self):
        global_definition = self._try_eat(KEYWORDS.GLOBAL)

        if self._current_token.token_type == KEYWORDS.DEF:
            self._eat(KEYWORDS.DEF)

            name = self._eat(TOKENS.ID)
            self._eat(TOKENS.LEFT_BRACE)
            parameters = self._parameters()
            self._eat(TOKENS.RIGHT_BRACE)
            self._eat(TOKENS.NEWLINE)
            self._eat(KEYWORDS.END)

            self._ast.append(
                FunctionDefinition(name.value, parameters, None, None))

    def _fnc_def(self):
        global_definition = self._try_eat(KEYWORDS.GLOBAL)

        if self._current_token.token_type == KEYWORDS.DEFFCT:
            self._eat(KEYWORDS.DEFFCT)

            return_type = self._eat(TOKENS.ID)
            name = self._eat(TOKENS.ID)
            self._eat(TOKENS.LEFT_BRACE)
            parameters = self._parameters()
            self._eat(TOKENS.RIGHT_BRACE)
            self._eat(TOKENS.NEWLINE)
            self._eat(KEYWORDS.ENDFCT)

            self._ast.append(
                FunctionDefinition(name.value, parameters,
                                   None, Type(return_type.value)))

    def _parameters(self):
        if not self._is_current_token(TOKENS.ID):
            return None

        parameters = []
        parameters.append(self._parameter())

        while self._try_eat(TOKENS.COMMA):
            parameters.append(self._parameter())

        return parameters


    def _parameter(self):
        name = self._eat(TOKENS.ID)
        self._eat(TOKENS.COLON)

        parameter_type = None
        if self._try_eat(KEYWORDS.IN):
            parameter_type = Parameter.TYPE.IN
        elif self._try_eat(KEYWORDS.OUT):
            parameter_type = Parameter.TYPE.OUT


        if not parameter_type:
            self._error(f"Expected \"{KEYWORDS.IN}\" or \"{KEYWORDS.OUT}\"")

        return Parameter(name.value, parameter_type)
