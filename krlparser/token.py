#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Token:
    def __init__(self, token_type, value, line_number, column):
        self.token_type = token_type
        self.value = value
        self.line_number = line_number
        self.column = column

    def __repr__(self):
        return "Token({token_type}, {value}, {line_number}, {column})".format(
            token_type=self.token_type,
            value=self.value if not isinstance(self.value, str) else "\"" + self.value + "\"",
            line_number=self.line_number, column=self.column
        )

    def __eq__(self, other):
        return (self.token_type == other.token_type and
                self.value == other.value and
                self.line_number == other.line_number and
                self.column == other.column
                )

    def __ne_(self, other):
        return not self == other
