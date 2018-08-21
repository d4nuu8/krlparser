#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from krllint import Lexer
from krllint.token import Token
from krllint.krlgrammar import TOKENS

class LexerTestCase(TestCase):
    def test_comment(self):
        lexer = Lexer(";Test")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.COMMENT, "Test", 0, 0), tokens[0])

    def test_single_line_string(self):
        lexer = Lexer("\"Hello, World!\"")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.STRING, "Hello, World!", 0, 0), tokens[0])

    def test_multine_line_string_terminated_by_eof(self):
        lexer = Lexer("\"Hello, World!")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.STRING, "Hello, World!", 0, 0), tokens[0])
        self.assertEqual(TOKENS.ERROR_TOKEN, tokens[1].token_type)

    def test_multine_line_string_terminated_by_eol(self):
        lexer = Lexer("\"Hello, World!\n")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.STRING, "Hello, World!", 0, 0), tokens[0])
        self.assertEqual(TOKENS.ERROR_TOKEN, tokens[1].token_type)

    def test_file_attribute(self):
        lexer = Lexer("&Test")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.FILE_ATTRIBUTE, "Test", 0, 0), tokens[0])

    def test_name(self):
        lexer = Lexer("NamedTest")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.NAME, "NamedTest", 0, 0), tokens[0])

    def test_name_with_whitespaces(self):
        lexer = Lexer("   NamedTest   ")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.NAME, "NamedTest", 0, 3), tokens[0])

        lexer = Lexer("\tNamedTest\t")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.NAME, "NamedTest", 0, 1), tokens[0])

    def test_hex_digit(self):
        lexer = Lexer("'H1F")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.INTEGER, int("1f", 16), 0, 0), tokens[0])

    def test_invalid_hex_digit(self):
        lexer = Lexer("'H1FJ")
        tokens = lexer.generate_tokens()
        self.assertEqual(TOKENS.ERROR_TOKEN, tokens[0].token_type)

    def test_bin_digit(self):
        lexer = Lexer("'B1010'")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.INTEGER, int("1010", 2), 0, 0), tokens[0])
        self.assertEqual(Token(TOKENS.END_OF_FILE, None, 0, 7), tokens[1])

    def test_integer(self):
        lexer = Lexer("12345")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.INTEGER, 12345, 0, 0), tokens[0])
        self.assertEqual(Token(TOKENS.END_OF_FILE, None, 0, 5), tokens[1])

    def test_real(self):
        lexer = Lexer("1.1")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.REAL, 1.1, 0, 0), tokens[0])

        lexer = Lexer("1E3")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.REAL, 1E3, 0, 0), tokens[0])

        lexer = Lexer("1.3E3")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.REAL, 1.3E3, 0, 0), tokens[0])

        lexer = Lexer("1.3E-3")
        tokens = lexer.generate_tokens()
        self.assertEqual(Token(TOKENS.REAL, 1.3E-3, 0, 0), tokens[0])
