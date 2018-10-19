#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser import Lexer, Parser
from krlparser.ast import FunctionDefinition

class ParserTestCase(TestCase):
    def test_fnc_def(self):
        test_input = (
            "GLOBAL DEF Foo()\n"
            "END"
        )

        lexer = Lexer(test_input)
        parser = Parser(lexer)
        parser.parse()

        awaited_result = [
            FunctionDefinition("Foo", None, None, None, 0)
        ]
        result = parser.ast

        self.assertEqual(awaited_result, result)
