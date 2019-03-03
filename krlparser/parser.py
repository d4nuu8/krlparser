#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, auto
from .krlgrammar import TOKENS, KEYWORDS
from .ast import FunctionDefinition, Parameter, Type, Scope, FunctionCall


class ParsingError(Exception):
    def __init__(self, line_number, column, message):
        super().__init__(message)

        self.line_number = line_number
        self.column = column
        self.message = message


class InputType(Enum):
    SRC = auto()
    SUB = auto()
    DAT = auto()


class Parser:
    def __init__(self, lexer):
        self._ast = []
        self._tokens = lexer.generate_tokens()
        self._position = 0
        self._current_token = self._tokens[self._position]

    @property
    def ast(self):
        return self._ast

    def parse(self, input_type):
        if input_type in (InputType.SRC, InputType.SUB):
            self._src_file()
        elif input_type == InputType.DAT:
            self._dat_file()

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

    def _skip_newlines(self):
        while self._try_eat(TOKENS.NEWLINE):
            pass

    def _src_file(self):
        self._mod_def()
        self._fnc_def()

        if not self._ast:
            raise self._error("No module or function definition found")

        while any(self._is_current_token(token) for token in
                  (KEYWORDS.GLOBAL, KEYWORDS.DEF, KEYWORDS.DEFFCT)):
            self._mod_def()
            self._fnc_def()

    def _dat_file(self):
        self._dat_def()

    def _file_attrs(self):
        while self._current_token.token_type == TOKENS.FILE_ATTRIBUTE:
            self._file_attr()

    def _file_attr(self):
        # TODO: Add attributes somewhere
        attribute = self._eat(TOKENS.FILE_ATTRIBUTE)

    def _mod_def(self):
        self._skip_newlines()

        global_definition = self._try_eat(KEYWORDS.GLOBAL)

        if self._current_token.token_type == KEYWORDS.DEF:
            self._eat(KEYWORDS.DEF)

            name = self._eat(TOKENS.ID)
            self._eat(TOKENS.LEFT_BRACE)
            parameters = self._params_def()
            self._eat(TOKENS.RIGHT_BRACE)
            self._eat(TOKENS.NEWLINE)

            self._skip_newlines()

            body = self._body()

            self._eat(KEYWORDS.END)

            self._ast.append(
                FunctionDefinition(name.value, parameters, body, None))

            self._skip_newlines()

    def _fnc_def(self):
        self._skip_newlines()

        global_definition = self._try_eat(KEYWORDS.GLOBAL)

        if self._current_token.token_type == KEYWORDS.DEFFCT:
            self._eat(KEYWORDS.DEFFCT)

            return_type = self._eat(TOKENS.ID)
            name = self._eat(TOKENS.ID)
            self._eat(TOKENS.LEFT_BRACE)
            parameters = self._params_def()
            self._eat(TOKENS.RIGHT_BRACE)
            self._eat(TOKENS.NEWLINE)

            self._skip_newlines()

            body = self._body()

            self._eat(KEYWORDS.ENDFCT)

            self._ast.append(
                FunctionDefinition(name.value, parameters,
                                   body, Type(return_type.value)))

            self._skip_newlines()

    def _dat_def(self):
        self._skip_newlines()

        self._eat(KEYWORDS.DEFDAT)
        name = self._eat(TOKENS.ID)
        public_definition = self._try_eat(KEYWORDS.PUBLIC)
        self._eat(TOKENS.NEWLINE)

        self._skip_newlines()

        self._eat(KEYWORDS.ENDDAT)

        self._ast.append(Scope(name.value))

        self._skip_newlines()

    def _params_def(self):
        if not self._is_current_token(TOKENS.ID):
            return None

        parameters = []
        parameters.append(self._param_def())

        while self._try_eat(TOKENS.COMMA):
            parameters.append(self._param_def())

        return parameters


    def _param_def(self):
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


    def _body(self):
        body = []
        while True:
            self._skip_newlines()

            if self._is_current_token(TOKENS.ID):
                body.append(self._mod_call())
            else:
                break

        return body


    def _mod_call(self):
        function = self._eat(TOKENS.ID)
        self._eat(TOKENS.LEFT_BRACE)
        parameters = self._params()
        self._eat(TOKENS.RIGHT_BRACE)
        self._eat(TOKENS.NEWLINE)

        return FunctionCall(function.value, parameters)


    def _params(self):
        if not self._is_current_token(TOKENS.ID):
            return None

        parameters = []
        parameters.append(self._param())

        while self._try_eat(TOKENS.COMMA):
            parameters.append(self._param())

        return parameters


    def _param(self):
        return self._eat(TOKENS.ID).value
