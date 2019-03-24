#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ParsingError(Exception):
    def __init__(self, *, line_number, column, message):
        super().__init__(message)

        self.line_number = line_number
        self.column = column
        self.message = message
