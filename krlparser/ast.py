#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC

class AST(ABC):
    def __init__(self, line_number, column):
        self.line_number = line_number
        self.column = column

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne_(self, other):
        return not self == other


class FunctionDefinition(AST):
    def __init__(self, name, arguments, body, returns, line_number):
        super().__init__(line_number, 0)

        self.name = name
        self.arguments = arguments
        self.body = body
        self.returns = returns

    def __repr__(self):
        return (f"FunctionDefinition("
                f"{self.name}, "
                f"{self.arguments}, "
                f"{self.body}, "
                f"{self.returns})")
