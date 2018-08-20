#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krllint import Lexer
from krllint.token import Token
from krllint.krlgrammar import TOKENS

class LexerTestCase(TestCase):
    def test_comment(self):
        lexer = Lexer(";Test")
        self.assertEqual(Token(TOKENS.COMMENT, "Test", 0, 0), lexer.get_next_token())

    def test_single_line_string(self):
        lexer = Lexer("\"Hello, World!\"")
        self.assertEqual(Token(TOKENS.STRING, "Hello, World!", 0, 0), lexer.get_next_token())

    def test_multine_line_string_terminated_by_eof(self):
        lexer = Lexer("\"Hello, World!")
        self.assertEqual(Token(TOKENS.STRING, "Hello, World!", 0, 0), lexer.get_next_token())
        self.assertEqual(TOKENS.ERROR_TOKEN, lexer.get_next_token().token_type)

    def test_multine_line_string_terminated_by_eol(self):
        lexer = Lexer("\"Hello, World!\n")
        self.assertEqual(Token(TOKENS.STRING, "Hello, World!", 0, 0), lexer.get_next_token())
        self.assertEqual(TOKENS.ERROR_TOKEN, lexer.get_next_token().token_type)

    def test_file_attribute(self):
        lexer = Lexer("&Test")
        self.assertEqual(Token(TOKENS.FILE_ATTRIBUTE, "Test", 0, 0), lexer.get_next_token())

    def test_name(self):
        lexer = Lexer("NamedTest")
        self.assertEqual(Token(TOKENS.NAME, "NamedTest", 0, 0), lexer.get_next_token())

    def test_name_with_whitespaces(self):
        lexer = Lexer("   NamedTest   ")
        self.assertEqual(Token(TOKENS.NAME, "NamedTest", 0, 3), lexer.get_next_token())

        lexer = Lexer("\tNamedTest\t")
        self.assertEqual(Token(TOKENS.NAME, "NamedTest", 0, 1), lexer.get_next_token())

    def test_hex_digit(self):
        lexer = Lexer("'H1F")
        self.assertEqual(Token(TOKENS.INTEGER, int("1f", 16), 0, 0), lexer.get_next_token())

    def test_invalid_hex_digit(self):
        lexer = Lexer("'H1FJ")
        self.assertEqual(TOKENS.ERROR_TOKEN, lexer.get_next_token().token_type)

    def test_bin_digit(self):
        lexer = Lexer("'B1010")
        self.assertEqual(Token(TOKENS.INTEGER, int("1010", 2), 0, 0), lexer.get_next_token())

    def test_integer(self):
        lexer = Lexer("12345")
        self.assertEqual(Token(TOKENS.INTEGER, 12345, 0, 0), lexer.get_next_token())

    def test_real(self):
        lexer = Lexer("1.1")
        self.assertEqual(Token(TOKENS.REAL, 1.1, 0, 0), lexer.get_next_token())

        lexer = Lexer("1E3")
        self.assertEqual(Token(TOKENS.REAL, 1E3, 0, 0), lexer.get_next_token())

        lexer = Lexer("1.3E3")
        self.assertEqual(Token(TOKENS.REAL, 1.3E3, 0, 0), lexer.get_next_token())

        lexer = Lexer("1.3E-3")
        self.assertEqual(Token(TOKENS.REAL, 1.3E-3, 0, 0), lexer.get_next_token())
