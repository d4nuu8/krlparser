#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SymbolTable:
    def __init__(self, name, parent_scope):
        self.name = name
        self.parent_scope = parent_scope
        self._symbols = {}


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __ne_(self, other):
        return not self == other


    def add(self, symbol):
        self._symbols[symbol.name] = symbol


    def lookup(self, name, current_scope_only=False):
        symbol = self._symbols.get(name)

        if symbol:
            return symbol

        if current_scope_only or not self.parent_scope:
            return None

        return self.parent_scope.lookup(name)


    def __repr__(self):
        return (f"SymbolTable("
                f"name={self.name}, "
                f"parent_scope={self.parent_scope}, "
                f"symbols={self._symbols})")
