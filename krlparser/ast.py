#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from enum import Enum, auto


class AST(ABC):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne_(self, other):
        return not self == other


class FileAttribute(AST):
    def __init__(self, value):
        super().__init__()

        self.value = value

    def __repr__(self):
        return f"FileAttribute({self.value})"


class FunctionDefinition(AST):
    def __init__(self, name, parameters, body, returns):
        super().__init__()

        self.name = name
        self.parameters = parameters or []
        self.body = body or []
        self.returns = returns

    def __repr__(self):
        return (f"FunctionDefinition("
                f"{self.name}, "
                f"{self.parameters}, "
                f"{self.body}, "
                f"{self.returns})")


class Parameter(AST):
    def __init__(self, name, parameter_type):
        super().__init__()

        self.name = name
        self.parameter_type = parameter_type

    def __repr__(self):
        return (f"Parameter("
                f"{self.name}, "
                f"{self.parameter_type})")

    class TYPE(Enum):
        IN = auto()
        OUT = auto()


class Type(AST):
    def __init__(self, name):
        super().__init__()

        self.name = name

    def __repr__(self):
        return f"Type({self.name})"


class Scope(AST):
    def __init__(self, name):
        super().__init__()

        self.name = name
