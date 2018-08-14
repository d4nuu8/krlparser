#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krllint import Lexer
from krllint.token import Token
from krllint.krlgrammar import tokens

class LexerTestCase(TestCase):
    def test_comment(self):
        lexer = Lexer(";Test")
        self.assertEqual(Token(tokens.COMMENT, "Test", 0, 0), lexer.get_next_token())

    def test_single_line_string(self):
        lexer = Lexer("\"Hello, World!\"")
        self.assertEqual(Token(tokens.STRING, "Hello, World!", 0, 0), lexer.get_next_token())

    def test_multine_line_string_terminated_by_eof(self):
        lexer = Lexer("\"Hello, World!")
        self.assertEqual(Token(tokens.STRING, "Hello, World!", 0, 0), lexer.get_next_token())
        self.assertEqual(tokens.ERROR_TOKEN, lexer.get_next_token().token_type)

    def test_multine_line_string_terminated_by_eol(self):
        lexer = Lexer("\"Hello, World!\n")
        self.assertEqual(Token(tokens.STRING, "Hello, World!", 0, 0), lexer.get_next_token())
        self.assertEqual(tokens.ERROR_TOKEN, lexer.get_next_token().token_type)

    def test_file_attribute(self):
        lexer = Lexer("&Test")
        self.assertEqual(Token(tokens.FILE_ATTRIBUTE, "Test", 0, 0), lexer.get_next_token())

    def test_name(self):
        lexer = Lexer("NamedTest")
        self.assertEqual(Token(tokens.NAME, "NamedTest", 0, 0), lexer.get_next_token())

    def test_name_with_whitespaces(self):
        lexer = Lexer("   NamedTest   ")
        self.assertEqual(Token(tokens.NAME, "NamedTest", 0, 3), lexer.get_next_token())

        lexer = Lexer("\tNamedTest\t")
        self.assertEqual(Token(tokens.NAME, "NamedTest", 0, 1), lexer.get_next_token())