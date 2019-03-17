#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from enum import Enum, auto
from .helper import camel_to_snake


class NodeVisitor(ABC):
    def visit(self, nodes):
        if hasattr(nodes, "__iter__"):
            for node in nodes:
                return self.visit(node)
        else:
            method_name = "visit_" + camel_to_snake(type(nodes).__name__)
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(nodes)

    @classmethod
    def generic_visit(cls, node):
        raise Exception(f"No visitor found for {type(node).__name__}")


class AST(ABC):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne_(self, other):
        return not self == other


class Module(AST):
    def __init__(self, name, source_file, data_file):
        super().__init__()

        self.name = name
        self.source_file = source_file
        self.data_file = data_file

    def __repr__(self):
        return f"Module({self.name}, {self.source_file}, {self.data_file})"


class KrlFile(AST, ABC):
    def __init__(self, name, file_attributes, statements):
        super().__init__()

        self.name = name
        self.file_attributes = file_attributes
        self.statements = statements
        self.symbol_table = None

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.file_attributes}, {self.statements})")


class SourceFile(KrlFile):
    pass


class DataFile(KrlFile):
    pass


class SubmitFile(KrlFile):
    pass


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
        self.symbol_table = None

    def __repr__(self):
        return (f"FunctionDefinition("
                f"{self.name}, "
                f"{self.parameters}, "
                f"{self.body}, "
                f"{self.returns})")


class DataDefinition(AST):
    def __init__(self, name, body):
        super().__init__()

        self.name = name
        self.body = body or []
        self.symbol_table = None

    def __repr__(self):
        return f"DataDefinition({self.name}, {self.body})"


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


class FunctionCall(AST):
    def __init__(self, function, parameters):
        super().__init__()

        self.function = function
        self.parameters = parameters or []

    def __repr__(self):
        return (f"FunctionCall("
                f"{self.function}, "
                f"{self.parameters})")


class Type(AST):
    def __init__(self, name):
        super().__init__()

        self.name = name

    def __repr__(self):
        return f"Type({self.name})"


class Symbol(ABC):
    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type


class VariableSymbol(Symbol):
    def __repr__(self):
        return f"VariableSymbol({self.name}, {self.type})"


class FunctionSymbol(Symbol):
    def __init__(self, name, parameters, returns):
        super().__init__(name, self)

        self.parameters = parameters or []
        self.returns = returns


    @staticmethod
    def create_from_definition(definition):
        return FunctionSymbol(definition.name,
                              definition.parameters.copy(),
                              definition.returns)

    def __repr__(self):
        return f"FunctionSymbol({self.name}, {self.parameters}, {self.returns})"
