#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser.semantic_analyzer import SemanticAnalyzer
from krlparser.symbol_table import SymbolTable
from krlparser.parser import Parser
from krlparser.ast import *


class SymbolTableTestCase(TestCase):
    def test_simple_module_definition(self):
        module_name = "Foo"

        source_file = (
            "GLOBAL DEF Foo(bar:IN, foobar:OUT)\n"
            "\n"
            "END"
            "\n"
            "\n"
            "DEF Bar()\n"
            "\n"
            "END"
        )

        data_file = (
            "DEFDAT Foo\n"
            "\n"
            "ENDDAT"
        )

        function_definition1 = FunctionDefinition("Foo", [
            Parameter("bar", Parameter.TYPE.IN),
            Parameter("foobar", Parameter.TYPE.OUT)
            ], None, None)

        function_definition2 = FunctionDefinition("Bar", None, None, None)

        global_symbol_table = SymbolTable("GLOBAL", None)
        module_symbol_table = SymbolTable("Foo", global_symbol_table)
        function1_symbol_table = SymbolTable("Foo.Foo", module_symbol_table)
        function2_symbol_table = SymbolTable("Foo.Bar", module_symbol_table)

        awaited_ast = [
            Module(module_name,
                   SourceFile(module_name, None, [
                       FunctionDefinition("Foo", [
                           Parameter("bar", Parameter.TYPE.IN),
                           Parameter("foobar", Parameter.TYPE.OUT)
                           ], None, None),
                       FunctionDefinition("Bar", None, None, None)]),
                   DataFile(module_name, None, [DataDefinition("Foo", [])]))]

        module_symbol_table.add(
            FunctionSymbol.create_from_definition(function_definition1))
        module_symbol_table.add(
            FunctionSymbol.create_from_definition(function_definition2))

        parser = Parser()
        parser.add_module(module_name, source_file, data_file)

        self.maxDiff = None
        analyzer = SemanticAnalyzer()
        analyzer.visit(parser.ast)


