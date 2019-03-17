#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser import Parser
from krlparser.ast import (Module, SourceFile, DataFile,
                           FunctionDefinition, DataDefinition, Parameter,
                           FunctionCall)


class ParserTestCase(TestCase):
    def test_module_parsing(self):
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

        awaited_ast = [
            Module(module_name,
                   SourceFile(module_name, None, [
                       FunctionDefinition("Foo", [
                           Parameter("bar", Parameter.TYPE.IN),
                           Parameter("foobar", Parameter.TYPE.OUT)
                           ], None, None),
                       FunctionDefinition("Bar", None, None, None)]),
                   DataFile(module_name, None, [DataDefinition("Foo", [])]))]

        parser = Parser()
        parser.add_module(module_name, source_file, data_file)

        self.maxDiff = None
        self.assertEqual(awaited_ast, parser.ast)


    def test_source_parsing(self):
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

        awaited_ast = [
            SourceFile("Foo", None, [
                FunctionDefinition("Foo", [
                    Parameter("bar", Parameter.TYPE.IN),
                    Parameter("foobar", Parameter.TYPE.OUT)
                ], None, None),
                FunctionDefinition("Bar", None, None, None)
            ])]

        parser = Parser()
        parser.add_source_file("Foo", source_file)

        self.maxDiff = None
        self.assertEqual(awaited_ast, parser.ast)


    def test_data_parsing(self):
        data_file = (
            "DEFDAT Foo\n"
            "\n"
            "ENDDAT"
        )

        awaited_ast = [DataFile("Foo", None, [DataDefinition("Foo", [])])]

        parser = Parser()
        parser.add_data_file("Foo", data_file)

        self.maxDiff = None
        self.assertEqual(awaited_ast, parser.ast)


    def test_sub_parsing(self):
        pass


    def test_mod_call(self):
        source_file = (
            "DEF Foo()\n"
            "Bar(foo, bar)\n"
            "FooBar()\n"
            "END"
            "\n"
            "DEF Bar(foo:IN, bar:IN)\n"
            "END"
            "\n"
            "DEF FooBar()\n"
            "END"
        )

        awaited_ast = [
            SourceFile("Foo", None, [
                FunctionDefinition("Foo", None, [
                    FunctionCall("Bar", ["foo", "bar"]),
                    FunctionCall("FooBar", None)
                ], None),
                FunctionDefinition("Bar", [
                    Parameter("foo", Parameter.TYPE.IN),
                    Parameter("bar", Parameter.TYPE.IN)
                    ], None, None),
                FunctionDefinition("FooBar", None, None, None)])]


        parser = Parser()
        parser.add_source_file("Foo", source_file)

        self.maxDiff = None
        self.assertEqual(awaited_ast, parser.ast)
