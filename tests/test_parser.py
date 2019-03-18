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
            Module(name=module_name,
                   source_file=SourceFile(name=module_name, statements=[
                       FunctionDefinition(name="Foo", parameters=[
                           Parameter(name="bar",
                                     parameter_type=Parameter.TYPE.IN),
                           Parameter(name="foobar",
                                     parameter_type=Parameter.TYPE.OUT)
                           ]),
                       FunctionDefinition(name="Bar")]),
                   data_file=DataFile(name=module_name,
                                      statements=[DataDefinition(name="Foo")]))]

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
            SourceFile(name="Foo", statements=[
                FunctionDefinition(name="Foo", parameters=[
                    Parameter(name="bar", parameter_type=Parameter.TYPE.IN),
                    Parameter(name="foobar", parameter_type=Parameter.TYPE.OUT)
                ]),
                FunctionDefinition(name="Bar")
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

        awaited_ast = [DataFile(name="Foo",
                                statements=[DataDefinition(name="Foo")])]

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
            SourceFile(name="Foo", statements=[
                FunctionDefinition(name="Foo", body=[
                    FunctionCall(name="Bar", parameters=["foo", "bar"]),
                    FunctionCall(name="FooBar")
                ]),
                FunctionDefinition(name="Bar", parameters=[
                    Parameter(name="foo", parameter_type=Parameter.TYPE.IN),
                    Parameter(name="bar", parameter_type=Parameter.TYPE.IN)
                    ]),
                FunctionDefinition(name="FooBar")])]


        parser = Parser()
        parser.add_source_file("Foo", source_file)

        self.maxDiff = None
        self.assertEqual(awaited_ast, parser.ast)
