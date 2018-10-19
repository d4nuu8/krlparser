#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser import Lexer, Parser
from krlparser.ast import FunctionDefinition, Parameter, Type

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

        self._generic_test(test_input, awaited_result)

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

        self._generic_test(test_input, awaited_result)

    def _generic_test(self, test_input, awaited_result):
        lexer = Lexer(test_input)
        parser = Parser(lexer)
        parser.parse()
        result = parser.ast
        self.assertEqual(awaited_result, result)
