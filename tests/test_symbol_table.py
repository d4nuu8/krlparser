#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krlparser.symbol_table import SymbolTable
from krlparser.ast import VariableSymbol


class SymbolTableTestCase(TestCase):
    def test_create_table_and_get_symbol(self):
        symbol_table = SymbolTable("GLOBAL", None)
        symbol = VariableSymbol(name="foo", symbol_type="INT")
        symbol_table.add(symbol)

        result = symbol_table.lookup("foo")
        self.assertEqual(symbol, result)

    def test_get_unknown_symbol(self):
        symbol_table = SymbolTable("GLOBAL", None)
        self.assertEqual(symbol_table.lookup("foo"), None)

    def test_get_symbol_from_parent(self):
        parent_scope = SymbolTable("GLOBAL", None)
        sub_scope = SymbolTable("GLOBAL", parent_scope)
        symbol = VariableSymbol(name="foo", symbol_type="INT")
        parent_scope.add(symbol)

        result = sub_scope.lookup("foo")
        self.assertEqual(symbol, result)
