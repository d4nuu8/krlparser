#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ast import NodeVisitor, FunctionSymbol
from .symbol_table import SymbolTable


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable("GLOBAL", None)
        self._current_module_table = None
        self._current_function_table = None

    def visit_module(self, module):
        self._current_module_table = SymbolTable(module.name,
                                                 self.symbol_table)
        self.visit(module.source_file)
        self.visit(module.data_file)
        self._current_module_table = None

    def visit_source_file(self, file):
        self.visit_file(file)

    def visit_data_file(self, file):
        self.visit_file(file)

    def visit_submit_file(self, file):
        self.visit_file(file)

    def visit_file(self, file):
        if (not self._current_module_table or
                self._current_module_table.name != file.name):
            self._current_module_table = SymbolTable(file.name,
                                                     self.symbol_table)

        file.symbol_table = self._current_module_table

        for statement in file.statements:
            self.visit(statement)

    def visit_function_definition(self, definition):
        self._current_module_table.add(
            FunctionSymbol.create_from_definition(definition))

        smybol_table_name = \
            f"{self._current_module_table.name}.{definition.name}"

        definition.symbol_table = SymbolTable(smybol_table_name,
                                              self._current_module_table)

        for statement in definition.body:
            self.visit(statement)

    def visit_data_definition(self, definition):
        if (not self._current_module_table or
                self._current_module_table.name != definition.name):
            self._current_module_table = SymbolTable(definition.name,
                                                     self.symbol_table)

        definition.symbol_table = self._current_module_table

        for statement in definition.body:
            self.visit(statement)
