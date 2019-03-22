#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .lexer import Lexer
from .token import TOKENS, KEYWORDS
from .ast import (Module, SourceFile, DataFile,
                  FunctionDefinition, DataDefinition,
                  Parameter, Type, FunctionCall)


class ParsingError(Exception):
    def __init__(self, line_number, column, message):
        super().__init__(message)

        self.line_number = line_number
        self.column = column
        self.message = message


class Parser:
    def __init__(self):
        self._ast = []
        self._temp_ast = []
        self._tokens = []
        self._position = 0
        self._current_token = None


    @property
    def ast(self):
        return self._ast


    def add_module(self, module_name, source_file, data_file):
        source_tokens = Lexer(source_file).generate_tokens()
        data_tokens = Lexer(data_file).generate_tokens()

        self._initialize(source_tokens)
        source_file = self._src_file(module_name)

        self._initialize(data_tokens)
        data_file = self._dat_file(module_name)

        self.ast.append(Module(name=module_name,
                               source_file=source_file,
                               data_file=data_file))


    def add_source_file(self, name, source_file):
        source_tokens = Lexer(source_file).generate_tokens()
        self._initialize(source_tokens)
        source_file = self._src_file(name)
        self.ast.append(source_file)


    def add_data_file(self, name, data_file):
        data_tokens = Lexer(data_file).generate_tokens()
        self._initialize(data_tokens)
        data_file = self._dat_file(name)
        self.ast.append(data_file)


    def _initialize(self, tokens):
        self._tokens = tokens
        self._temp_ast = []
        self._position = 0
        self._current_token = self._tokens[self._position]


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


    def _src_file(self, name):
        attributes = self._file_attrs()
        statements = []
        statements.append(self._mod_def() or self._fnc_def())

        if not statements:
            raise self._error("No module or function definition found")

        while any(self._is_current_token(token) for token in
                  (KEYWORDS.GLOBAL, KEYWORDS.DEF, KEYWORDS.DEFFCT)):
            definitions = (self._mod_def(), self._fnc_def())
            for definition in filter(None, definitions):
                statements.append(definition)

        return SourceFile(name=name,
                          file_attributes=attributes,
                          statements=statements)


    def _dat_file(self, name):
        attributes = self._file_attrs()
        data_definition = self._dat_def()

        if not data_definition:
            raise self._error("No data definition found")

        self._eat(TOKENS.END_OF_FILE)

        return DataFile(name=name,
                        file_attributes=attributes,
                        statements=[data_definition])


    def _file_attrs(self):
        attributes = []
        while self._current_token.token_type == TOKENS.FILE_ATTRIBUTE:
            attributes.append(self._file_attr())

        return attributes or None


    def _file_attr(self):
        return self._eat(TOKENS.FILE_ATTRIBUTE)


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

            self._skip_newlines()
            return FunctionDefinition(name=name.value,
                                      parameters=parameters,
                                      body=body)

        return None


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

            self._skip_newlines()
            return FunctionDefinition(name=name.value,
                                      parameters=parameters,
                                      body=body,
                                      returns=Type(name=return_type.value))

        return None


    def _dat_def(self):
        self._skip_newlines()

        self._eat(KEYWORDS.DEFDAT)
        name = self._eat(TOKENS.ID)
        public_definition = self._try_eat(KEYWORDS.PUBLIC)
        self._eat(TOKENS.NEWLINE)

        self._skip_newlines()

        self._eat(KEYWORDS.ENDDAT)

        self._skip_newlines()
        return DataDefinition(name=name.value)


    def _params_def(self):
        parameters = []
        if not self._is_current_token(TOKENS.ID):
            return parameters

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

        return Parameter(name=name.value, parameter_type=parameter_type)


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

        return FunctionCall(name=function.value, parameters=parameters)


    def _params(self):
        parameters = []
        if not self._is_current_token(TOKENS.ID):
            return parameters

        parameters.append(self._param())

        while self._try_eat(TOKENS.COMMA):
            parameters.append(self._param())

        return parameters


    def _param(self):
        return self._eat(TOKENS.ID).value
