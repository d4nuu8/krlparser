#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .lexer import Lexer
from .token import TOKENS, KEYWORDS
from .ast import (Module, SourceFile, DataFile, FileAttribute,
                  FunctionDefinition, DataDefinition,
                  Parameter, Type, FunctionCall)
from .exceptions import ParsingError


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
        source_file = self._source_file(module_name)

        self._initialize(data_tokens)
        data_file = self._data_file(module_name)

        self.ast.append(Module(name=module_name,
                               source_file=source_file,
                               data_file=data_file))

    def add_source_file(self, name, source_file):
        source_tokens = Lexer(source_file).generate_tokens()
        self._initialize(source_tokens)
        source_file = self._source_file(name)
        self.ast.append(source_file)

    def add_data_file(self, name, data_file):
        data_tokens = Lexer(data_file).generate_tokens()
        self._initialize(data_tokens)
        data_file = self._data_file(name)
        self.ast.append(data_file)

    def _initialize(self, tokens):
        self._tokens = tokens
        self._temp_ast = []
        self._position = 0
        self._current_token = self._tokens[self._position]

    def _error(self, message):
        token = self._current_token
        raise ParsingError(line_number=token.line_number,
                           column=token.column,
                           message=message)

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

    def _peek(self):
        if self._position > len(self._tokens) - 2:
            return None
        return self._tokens[self._position + 1]

    def _is_current_token(self, token_type):
        return self._current_token.token_type == token_type

    def _is_next_token(self, token_type):
        return self._peek().token_type == token_type

    def _advance(self):
        self._position += 1

        if self._position > len(self._tokens) - 1:
            self._current_token = None
        else:
            self._current_token = self._tokens[self._position]

    # =========================================================================
    #                            Grammar definitions
    # =========================================================================

    def _source_file(self, name):
        """
        source_file = (header
                       1*(module_definition / function_definition))
        """
        attributes = self._header()

        statements = []
        while any(self._is_current_token(token) for token in
                  (KEYWORDS.GLOBAL, KEYWORDS.DEF, KEYWORDS.DEFFCT)):
            definitions = (self._module_definition(), self._function_definition())
            for definition in filter(None, definitions):
                statements.append(definition)

        if not statements:
            raise self._error("No module or function definition found")

        self._eat(TOKENS.END_OF_FILE)

        return SourceFile(name=name,
                          file_attributes=attributes,
                          statements=statements)

    def _data_file(self, name):
        """
        data_file = (header
                     1data_definition)
        """
        attributes = self._header()

        statements = []
        while self._is_current_token(KEYWORDS.DEFDAT):
            statements.append(self._data_definition())

        if not statements:
            raise self._error("No data definition found")
        if len(statements) > 1:
            raise self._error("More than one data definition found")

        self._eat(TOKENS.END_OF_FILE)

        return DataFile(name=name,
                        file_attributes=attributes,
                        statements=statements)

    def _header(self):
        """
        header = *(file_attribute 1*newline)
        """
        attributes = []
        while self._current_token.token_type == TOKENS.FILE_ATTRIBUTE:
            attributes.append(
                FileAttribute(value=self._eat(TOKENS.FILE_ATTRIBUTE).value))
            self._eat(TOKENS.NEWLINE)
        return attributes

    def _module_definition(self):
        """
        module_definition = (["GLOBAL"] "DEF" name "(" parameter_definitions ")" comment_or_newline
                             statements
                             "END" comment_or_newline)
        """
        global_definition = self._try_eat(KEYWORDS.GLOBAL)

        if not self._is_current_token(KEYWORDS.DEF):
            return None

        self._eat(KEYWORDS.DEF)
        name = self._eat(TOKENS.NAME)
        self._eat(TOKENS.LEFT_BRACE)
        parameters = self._parameter_definitions()
        self._eat(TOKENS.RIGHT_BRACE)
        self._comment_or_newline()

        body = self._statements()

        self._eat(KEYWORDS.END)
        self._comment_or_newline()

        return FunctionDefinition(name=name.value,
                                  parameters=parameters,
                                  body=body)

    def _function_definition(self):
        """
        function_definition = (["GLOBAL"] "DEFFCT" type name "(" parameter_definitions ")" comment_or_newline
                               statements
                               "END" comment_or_newline)
        """
        global_definition = self._try_eat(KEYWORDS.GLOBAL)

        if not self._is_current_token(KEYWORDS.DEFFCT):
            return None

        self._eat(KEYWORDS.DEFFCT)
        return_type = self._eat(TOKENS.NAME)
        name = self._eat(TOKENS.NAME)
        self._eat(TOKENS.LEFT_BRACE)
        parameters = self._parameter_definitions()
        self._eat(TOKENS.RIGHT_BRACE)
        self._comment_or_newline()

        body = self._statements()

        self._eat(KEYWORDS.ENDFCT)
        self._comment_or_newline()

        return FunctionDefinition(name=name.value,
                                  parameters=parameters,
                                  body=body,
                                  returns=Type(name=return_type.value))

    def _data_definition(self):
        """
        data_definition = ("DEFDAT" name ["PUBLIC"] comment_or_newline
                           "ENDDAT" comment_or_newline)
        """
        self._eat(KEYWORDS.DEFDAT)
        name = self._eat(TOKENS.NAME)
        public_definition = self._try_eat(KEYWORDS.PUBLIC)
        self._comment_or_newline()

        self._eat(KEYWORDS.ENDDAT)
        self._comment_or_newline()

        return DataDefinition(name=name.value)

    def _parameter_definitions(self):
        """
        parameter_definitions = [(parameter_definition [("," parameter_definition)])]
        """
        parameters = []
        if not self._is_current_token(TOKENS.NAME):
            return parameters

        parameters.append(self._parameter_definition())

        while self._try_eat(TOKENS.COMMA):
            parameters.append(self._parameter_definition())

        return parameters

    def _parameter_definition(self):
        """
        parameter_definition = name ":" ("IN" / "OUT")
        """
        name = self._eat(TOKENS.NAME)
        self._eat(TOKENS.COLON)

        parameter_type = None
        if self._try_eat(KEYWORDS.IN):
            parameter_type = Parameter.TYPE.IN
        elif self._try_eat(KEYWORDS.OUT):
            parameter_type = Parameter.TYPE.OUT

        if not parameter_type:
            self._error(f"Expected \"{KEYWORDS.IN}\" or \"{KEYWORDS.OUT}\"")

        return Parameter(name=name.value, parameter_type=parameter_type)

    def _statements(self):
        """
        statements = *(module_call / comment_or_newline)
        """
        statements = []
        while True:
            if (self._is_current_token(TOKENS.NAME) and
               self._is_next_token(TOKENS.LEFT_BRACE)):
                statements.append(self._module_call())
            elif any(self._is_current_token(token) for token in
                     (TOKENS.COMMENT, TOKENS.NEWLINE)):
                self._comment_or_newline()
            else:
                break

        return statements

    def _module_call(self):
        """
        module_call = name "(" parameters ")"
        """
        function = self._eat(TOKENS.NAME)
        self._eat(TOKENS.LEFT_BRACE)
        parameters = self._parameters()
        self._eat(TOKENS.RIGHT_BRACE)
        return FunctionCall(name=function.value, parameters=parameters)

    def _parameters(self):
        """
        parameters = [(name *("," name))]
        """
        parameters = []
        if not self._is_current_token(TOKENS.NAME):
            return parameters

        parameters.append(self._eat(TOKENS.NAME).value)

        while self._try_eat(TOKENS.COMMA):
            parameters.append(self._eat(TOKENS.NAME).value)

        return parameters

    def _comment_or_newline(self):
        """
        comment_or_newline = 1*([comment] newline)
        """
        self._try_eat(TOKENS.COMMENT)
        self._eat(TOKENS.NEWLINE)

        while any(self._is_current_token(token) for token in
                  (TOKENS.COMMENT, TOKENS.NEWLINE)):
            self._try_eat(TOKENS.COMMENT)
            self._eat(TOKENS.NEWLINE)
