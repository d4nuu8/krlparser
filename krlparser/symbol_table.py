#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SymbolTable:
    def __init__(self, name, parent_scope):
        self.name = name
        self.parent_scope = parent_scope
        self._symbols = {}


    def add(self, symbol):
        self._symbols[symbol.name] = symbol


    def lookup(self, name, current_scope_only=False):
        symbol = self._symbols.get(name)

        if symbol:
            return symbol

        if current_scope_only or not self.parent_scope:
            return None

        return self.parent_scope.lookup(name)
