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
    def __init__(self, *, name, source_file, data_file):
        super().__init__()

        self.name = name
        self.source_file = source_file
        self.data_file = data_file

    def __repr__(self):
        return (f"Module(name={self.name}, "
                f"source_file{self.source_file}, "
                f"data_file={self.data_file})")


class KrlFile(AST, ABC):
    def __init__(self, *, name, file_attributes=[], statements=[],
                 symbol_table=None):
        super().__init__()

        self.name = name
        self.file_attributes = file_attributes
        self.statements = statements
        self.symbol_table = symbol_table

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"file_attributes={self.file_attributes}, "
                f"statements={self.statements})")


class SourceFile(KrlFile):
    pass


class DataFile(KrlFile):
    pass


class SubmitFile(KrlFile):
    pass


class FileAttribute(AST):
    def __init__(self, *, value):
        super().__init__()

        self.value = value

    def __repr__(self):
        return f"FileAttribute({self.value})"


class FunctionDefinition(AST):
    def __init__(self, *, name, parameters=[], body=[], returns=None,
                 is_global=False, symbol_table=None):
        super().__init__()

        self.name = name
        self.parameters = parameters
        self.body = body
        self.returns = returns
        self.is_global = is_global
        self.symbol_table = symbol_table

    def __repr__(self):
        return (f"FunctionDefinition("
                f"name={self.name}, "
                f"parameters={self.parameters}, "
                f"body={self.body}, "
                f"returns={self.returns}, "
                f"is_global={self.is_global}, "
                f"symbol_table={self.symbol_table})")


class DataDefinition(AST):
    def __init__(self, *, name, body=[], symbol_table=None):
        super().__init__()

        self.name = name
        self.body = body
        self.symbol_table = symbol_table

    def __repr__(self):
        return (f"DataDefinition("
                f"name={self.name}, "
                f"body={self.body}, "
                f"symbol_table={self.symbol_table})")


class Parameter(AST):
    def __init__(self, *, name, parameter_type):
        super().__init__()

        self.name = name
        self.parameter_type = parameter_type

    def __repr__(self):
        return (f"Parameter("
                f"name={self.name}, "
                f"parameter_type={self.parameter_type})")

    class TYPE(Enum):
        IN = auto()
        OUT = auto()


class FunctionCall(AST):
    def __init__(self, *, name, parameters=[]):
        super().__init__()

        self.name = name
        self.parameters = parameters

    def __repr__(self):
        return (f"FunctionCall("
                f"name={self.name}, "
                f"parameters={self.parameters})")


class Type(AST):
    def __init__(self, *, name):
        super().__init__()

        self.name = name

    def __repr__(self):
        return f"Type(name={self.name})"


class Symbol(AST, ABC):
    def __init__(self, *, name, symbol_type):
        self.name = name
        self.type = symbol_type

    def __repr__(self):
        return f"VariableSymbol(name={self.name}, type={self.type})"


class VariableSymbol(Symbol):
    pass


class FunctionSymbol(Symbol):
    def __init__(self, *, name, parameters=[], returns=None):
        super().__init__(name=name, symbol_type=returns)

        self.parameters = parameters

    @staticmethod
    def create_from_definition(definition):
        return FunctionSymbol(name=definition.name,
                              parameters=definition.parameters.copy(),
                              returns=definition.returns)

    def __repr__(self):
        return (f"FunctionSymbol("
                f"name={self.name}, "
                f"parameters={self.parameters}, "
                f"returns={self.type})")
