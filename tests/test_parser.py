#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser import Lexer, Parser
from krlparser.ast import FunctionDefinition, Parameter, Type

class ParserTestCase(TestCase):
    def test_mod_def(self):
        test_input = (
            "GLOBAL DEF Foo(bar:IN, foobar:OUT)\n"
            "END"
        )

        lexer = Lexer(test_input)
        parser = Parser(lexer)
        parser.parse()

        awaited_result = [
            FunctionDefinition("Foo", [
                Parameter("bar", Parameter.TYPE.IN),
                Parameter("foobar", Parameter.TYPE.OUT)
                ], None, None)
        ]
        result = parser.ast

        self.assertEqual(awaited_result, result)

    def test_fnc_def(self):
        test_input = (
            "GLOBAL DEFFCT INT Foo(bar:IN, foobar:OUT)\n"
            "ENDFCT"
        )

        lexer = Lexer(test_input)
        parser = Parser(lexer)
        parser.parse()

        awaited_result = [
            FunctionDefinition("Foo", [
                Parameter("bar", Parameter.TYPE.IN),
                Parameter("foobar", Parameter.TYPE.OUT)
                ], None, Type("INT"))
        ]
        result = parser.ast

        self.assertEqual(awaited_result, result)
