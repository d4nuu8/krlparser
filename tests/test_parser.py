#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser import Lexer, Parser
from krlparser.parser import InputType
from krlparser.ast import FunctionDefinition, Parameter, Type, Scope, FunctionCall


class ParserTestCase(TestCase):
    def test_mod_def(self):
        test_input = (
            "GLOBAL DEF Foo(bar:IN, foobar:OUT)\n"
            "\n"
            "END"
            "\n"
            "\n"
            "DEF Bar()\n"
            "\n"
            "END"
        )

        awaited_result = [
            FunctionDefinition("Foo", [
                Parameter("bar", Parameter.TYPE.IN),
                Parameter("foobar", Parameter.TYPE.OUT)
                ], None, None),
            FunctionDefinition("Bar", None, None, None)
        ]

        self._generic_test(InputType.SRC, test_input, awaited_result)


    def test_fnc_def(self):
        test_input = (
            "GLOBAL DEFFCT INT Foo(bar:IN, foobar:OUT)\n"
            "\n"
            "ENDFCT"
            "\n"
            "\n"
            "DEFFCT REAL Bar()\n"
            "\n"
            "ENDFCT"
        )

        awaited_result = [
            FunctionDefinition("Foo", [
                Parameter("bar", Parameter.TYPE.IN),
                Parameter("foobar", Parameter.TYPE.OUT)
                ], None, Type("INT")),
            FunctionDefinition("Bar", None, None, Type("REAL"))
        ]

        self._generic_test(InputType.SRC, test_input, awaited_result)


    def test_dat_def(self):
        test_input = (
            "DEFDAT Foo PUBLIC\n"
            "\n"
            "ENDDAT"
        )

        awaited_result = [
            Scope("Foo")
        ]

        self._generic_test(InputType.DAT, test_input, awaited_result)


    def test_mod_call(self):
        test_input = (
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

        awaited_result = [
            FunctionDefinition("Foo", None, [
                FunctionCall("Bar", ["foo", "bar"]),
                FunctionCall("FooBar", None)
            ], None),
            FunctionDefinition("Bar", [
                Parameter("foo", Parameter.TYPE.IN),
                Parameter("bar", Parameter.TYPE.IN)
                ], None, None),
            FunctionDefinition("FooBar", None, None, None)
        ]

        self._generic_test(InputType.SRC, test_input, awaited_result)


    def _generic_test(self, input_type, test_input, awaited_result):
        lexer = Lexer(test_input)
        parser = Parser(lexer)
        parser.parse(input_type)
        result = parser.ast
        self.assertEqual(awaited_result, result)
