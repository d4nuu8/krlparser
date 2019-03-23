#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=too-many-public-methods, no-self-use

import pytest

from krlparser.lexer import Lexer
from krlparser.token import Token, TOKENS


class LexerTests:
    def test_invalid_input(self):
        with pytest.raises(ValueError):
            Lexer(None)

        with pytest.raises(ValueError):
            Lexer(0)

    def test_unknown_input(self):
        lexer = Lexer("~foo")
        tokens = lexer.generate_tokens()
        assert TOKENS.ERROR_TOKEN == tokens[0].token_type
        assert Token(TOKENS.ID, "foo", 0, 1) == tokens[1]

    def test_comment(self):
        lexer = Lexer(";Test")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.COMMENT, "Test", 0, 0) == tokens[0]

    def test_single_line_string(self):
        lexer = Lexer("\"Hello, World!\"")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.STRING, "Hello, World!", 0, 0) == tokens[0]

    def test_multine_line_string_terminated_by_eof(self):
        lexer = Lexer("\"Hello, World!")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.STRING, "Hello, World!", 0, 0) == tokens[0]
        assert TOKENS.ERROR_TOKEN == tokens[1].token_type

    def test_multine_line_string_terminated_by_eol(self):
        lexer = Lexer("\"Hello, World!\n")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.STRING, "Hello, World!", 0, 0) == tokens[0]
        assert TOKENS.ERROR_TOKEN == tokens[1].token_type

    def test_file_attribute(self):
        lexer = Lexer("&Test")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.FILE_ATTRIBUTE, "Test", 0, 0) == tokens[0]

    @pytest.mark.parametrize("keyword", ["global", "def", "end"])
    def test_keyword(self, keyword):
        lexer = Lexer(keyword)
        tokens = lexer.generate_tokens()
        assert Token(keyword.upper(), keyword, 0, 0) == tokens[0]

    def test_id(self):
        lexer = Lexer("IDdTest")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "IDdTest", 0, 0) == tokens[0]

    def test_id_with_whitespaces(self):
        lexer = Lexer("   IDdTest   ")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "IDdTest", 0, 3) == tokens[0]

        lexer = Lexer("\tIDdTest\t")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "IDdTest", 0, 1) == tokens[0]

    def test_hex_digit(self):
        lexer = Lexer("'H1F")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, int("1f", 16), 0, 0) == tokens[0]

    def test_invalid_hex_digit(self):
        lexer = Lexer("'H1FJ")
        tokens = lexer.generate_tokens()
        assert TOKENS.ERROR_TOKEN == tokens[0].token_type

    def test_bin_digit(self):
        lexer = Lexer("'B1010'")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, int("1010", 2), 0, 0) == tokens[0]
        assert Token(TOKENS.END_OF_FILE, None, 0, 7) == tokens[1]

    def test_integer(self):
        lexer = Lexer("12345")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, 12345, 0, 0) == tokens[0]
        assert Token(TOKENS.END_OF_FILE, None, 0, 5) == tokens[1]

    def test_real(self):
        lexer = Lexer("1.1")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.REAL, 1.1, 0, 0) == tokens[0]

        lexer = Lexer("1E3")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.REAL, 1E3, 0, 0) == tokens[0]

        lexer = Lexer("1.3E3")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.REAL, 1.3E3, 0, 0) == tokens[0]

        lexer = Lexer("1.3E-3")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.REAL, 1.3E-3, 0, 0) == tokens[0]

    def test_addition(self):
        lexer = Lexer("10 + 1")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, 10, 0, 0) == tokens[0]
        assert Token(TOKENS.PLUS, "+", 0, 3) == tokens[1]
        assert Token(TOKENS.INTEGER, 1, 0, 5) == tokens[2]

    def test_substraction(self):
        lexer = Lexer("10 - 1")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, 10, 0, 0) == tokens[0]
        assert Token(TOKENS.MINUS, "-", 0, 3) == tokens[1]
        assert Token(TOKENS.INTEGER, 1, 0, 5) == tokens[2]

    def test_divison(self):
        lexer = Lexer("10 / 1")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, 10, 0, 0) == tokens[0]
        assert Token(TOKENS.SLASH, "/", 0, 3) == tokens[1]
        assert Token(TOKENS.INTEGER, 1, 0, 5) == tokens[2]

    def test_multiplication(self):
        lexer = Lexer("10 * 1")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.INTEGER, 10, 0, 0) == tokens[0]
        assert Token(TOKENS.STAR, "*", 0, 3) == tokens[1]
        assert Token(TOKENS.INTEGER, 1, 0, 5) == tokens[2]

    def test_structure_access(self):
        lexer = Lexer("foo.bar")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.DOT, ".", 0, 3) == tokens[1]
        assert Token(TOKENS.ID, "bar", 0, 4) == tokens[2]

    def test_function_call(self):
        lexer = Lexer("Test(foo, bar)")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "Test", 0, 0) == tokens[0]
        assert Token(TOKENS.LEFT_BRACE, "(", 0, 4) == tokens[1]
        assert Token(TOKENS.ID, "foo", 0, 5) == tokens[2]
        assert Token(TOKENS.COMMA, ",", 0, 8) == tokens[3]
        assert Token(TOKENS.ID, "bar", 0, 10) == tokens[4]
        assert Token(TOKENS.RIGHT_BRACE, ")", 0, 13) == tokens[5]

    def test_greater_than(self):
        lexer = Lexer("foo > bar")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.GREATER, ">", 0, 4) == tokens[1]
        assert Token(TOKENS.ID, "bar", 0, 6) == tokens[2]

    def test_less_than(self):
        lexer = Lexer("foo < bar")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.LESS, "<", 0, 4) == tokens[1]
        assert Token(TOKENS.ID, "bar", 0, 6) == tokens[2]

    def test_assign(self):
        lexer = Lexer("foo = bar")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.EQUAL, "=", 0, 4) == tokens[1]
        assert Token(TOKENS.ID, "bar", 0, 6) == tokens[2]

    def test_geometric_shift(self):
        lexer = Lexer("foo : bar")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.COLON, ":", 0, 4) == tokens[1]
        assert Token(TOKENS.ID, "bar", 0, 6) == tokens[2]

    def test_array_access(self):
        lexer = Lexer("foo[bar]")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.LEFT_SQUARE_BRACE, "[", 0, 3) == tokens[1]
        assert Token(TOKENS.ID, "bar", 0, 4) == tokens[2]
        assert Token(TOKENS.RIGHT_SQUARE_BRACE, "]", 0, 7) == tokens[3]

    def test_enum_access(self):
        lexer = Lexer("foo = #bar")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.EQUAL, "=", 0, 4) == tokens[1]
        assert Token(TOKENS.HASH, "#", 0, 6) == tokens[2]
        assert Token(TOKENS.ID, "bar", 0, 7) == tokens[3]

    def test_structure_declaration(self):
        lexer = Lexer("foo = { bar }")
        tokens = lexer.generate_tokens()
        assert Token(TOKENS.ID, "foo", 0, 0) == tokens[0]
        assert Token(TOKENS.EQUAL, "=", 0, 4) == tokens[1]
        assert Token(TOKENS.LEFT_CURLY_BRACE, "{", 0, 6) == tokens[2]
        assert Token(TOKENS.ID, "bar", 0, 8) == tokens[3]
        assert Token(TOKENS.RIGHT_CURLY_BRACE, "}", 0, 12) == tokens[4]
