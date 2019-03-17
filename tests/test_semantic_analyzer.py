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

        function_definition1 = FunctionDefinition(name="Foo", parameters=[
            Parameter(name="bar", parameter_type=Parameter.TYPE.IN),
            Parameter(name="foobar", parameter_type=Parameter.TYPE.OUT)
            ])

        function_definition2 = FunctionDefinition(name="Bar")

        global_symbol_table = SymbolTable("GLOBAL", None)
        module_symbol_table = SymbolTable("Foo", global_symbol_table)
        function1_symbol_table = SymbolTable("Foo.Foo", module_symbol_table)
        function2_symbol_table = SymbolTable("Foo.Bar", module_symbol_table)

        awaited_ast = [
            Module(name=module_name,
                   source_file=SourceFile(name=module_name, statements=[
                       FunctionDefinition(name="Foo", parameters=[
                           Parameter(name="bar", parameter_type=Parameter.TYPE.IN),
                           Parameter(name="foobar", parameter_type=Parameter.TYPE.OUT)
                           ]),
                       FunctionDefinition(name="Bar")]),
                   data_file=DataFile(name=module_name, statements=[DataDefinition(name="Foo")]))]

        module_symbol_table.add(FunctionSymbol.create_from_definition(function_definition1))
        module_symbol_table.add(FunctionSymbol.create_from_definition(function_definition2))

        parser = Parser()
        parser.add_module(module_name, source_file, data_file)

        self.maxDiff = None
        analyzer = SemanticAnalyzer()
        analyzer.visit(parser.ast)


