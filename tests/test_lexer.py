#!/usr/bin/env python3
# -*- coding(): utf-8 -*-

import pytest

from krlparser.lexer import Lexer
from krlparser.token import Token, TOKENS


def test_invalid_input():
    with pytest.raises(ValueError):
        Lexer(None)

    with pytest.raises(ValueError):
        Lexer(0)


def test_unknown_input():
    lexer = Lexer("~foo")
    tokens = lexer.generate_tokens()
    assert TOKENS.ERROR_TOKEN == tokens[0].token_type
    assert Token(TOKENS.NAME, "foo", 0, 1) == tokens[1]


def test_comment():
    lexer = Lexer(";Test")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.COMMENT, "Test", 0, 0) == tokens[0]


def test_single_line_string():
    lexer = Lexer("\"Hello, World!\"")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.STRING, "Hello, World!", 0, 0) == tokens[0]


def test_multine_line_string_terminated_by_eof():
    lexer = Lexer("\"Hello, World!")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.STRING, "Hello, World!", 0, 0) == tokens[0]
    assert TOKENS.ERROR_TOKEN == tokens[1].token_type


def test_multine_line_string_terminated_by_eol():
    lexer = Lexer("\"Hello, World!\n")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.STRING, "Hello, World!", 0, 0) == tokens[0]
    assert TOKENS.ERROR_TOKEN == tokens[1].token_type


def test_file_attribute():
    lexer = Lexer("&Test")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.FILE_ATTRIBUTE, "Test", 0, 0) == tokens[0]


@pytest.mark.parametrize("keyword", ["global", "def", "end"])
def test_keyword(keyword):
    lexer = Lexer(keyword)
    tokens = lexer.generate_tokens()
    assert Token(keyword.upper(), keyword, 0, 0) == tokens[0]


def test_id():
    lexer = Lexer("IDdTest")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "IDdTest", 0, 0) == tokens[0]


def test_id_with_whitespaces():
    lexer = Lexer("   IDdTest   ")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "IDdTest", 0, 3) == tokens[0]

    lexer = Lexer("\tIDdTest\t")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "IDdTest", 0, 1) == tokens[0]


def test_hex_digit():
    lexer = Lexer("'H1F")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.INTEGER, int("1f", 16), 0, 0) == tokens[0]


def test_invalid_hex_digit():
    lexer = Lexer("'H1FJ")
    tokens = lexer.generate_tokens()
    assert TOKENS.ERROR_TOKEN == tokens[0].token_type


def test_bin_digit():
    lexer = Lexer("'B1010'")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.INTEGER, int("1010", 2), 0, 0) == tokens[0]
    assert Token(TOKENS.END_OF_FILE, None, 0, 7) == tokens[1]


def test_integer():
    lexer = Lexer("12345")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.INTEGER, 12345, 0, 0) == tokens[0]
    assert Token(TOKENS.END_OF_FILE, None, 0, 5) == tokens[1]


def test_real():
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


def test_structure_access():
    lexer = Lexer("foo.bar")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "foo", 0, 0) == tokens[0]
    assert Token(TOKENS.DOT, ".", 0, 3) == tokens[1]
    assert Token(TOKENS.NAME, "bar", 0, 4) == tokens[2]


def test_function_call():
    lexer = Lexer("Test(foo, bar)")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "Test", 0, 0) == tokens[0]
    assert Token(TOKENS.LEFT_BRACE, "(", 0, 4) == tokens[1]
    assert Token(TOKENS.NAME, "foo", 0, 5) == tokens[2]
    assert Token(TOKENS.COMMA, ",", 0, 8) == tokens[3]
    assert Token(TOKENS.NAME, "bar", 0, 10) == tokens[4]
    assert Token(TOKENS.RIGHT_BRACE, ")", 0, 13) == tokens[5]


@pytest.mark.parametrize("token,string", [
    (TOKENS.PLUS, "+"),
    (TOKENS.MINUS, "-"),
    (TOKENS.STAR, "*"),
    (TOKENS.SLASH, "/"),
    (TOKENS.COLON, ":"),
    (TOKENS.EQUAL, "="),
    (TOKENS.EQUAL_EQUAL, "=="),
    (TOKENS.NOT_EQUAL, "<>"),
    (TOKENS.GREATER, ">"),
    (TOKENS.LESS, "<"),
    (TOKENS.GREATER_EQUAL, ">="),
    (TOKENS.LESS_EQUAL, "<=")
])
def test_binary_operators(token, string):
    lexer = Lexer(f"foo {string} bar")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "foo", 0, 0) == tokens[0]
    assert Token(token, string, 0, 4) == tokens[1]
    assert Token(TOKENS.NAME, "bar", 0, 5 + len(string)) == tokens[2]


def test_array_access():
    lexer = Lexer("foo[bar]")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "foo", 0, 0) == tokens[0]
    assert Token(TOKENS.LEFT_SQUARE_BRACE, "[", 0, 3) == tokens[1]
    assert Token(TOKENS.NAME, "bar", 0, 4) == tokens[2]
    assert Token(TOKENS.RIGHT_SQUARE_BRACE, "]", 0, 7) == tokens[3]


def test_enum_access():
    lexer = Lexer("foo = #bar")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "foo", 0, 0) == tokens[0]
    assert Token(TOKENS.EQUAL, "=", 0, 4) == tokens[1]
    assert Token(TOKENS.HASH, "#", 0, 6) == tokens[2]
    assert Token(TOKENS.NAME, "bar", 0, 7) == tokens[3]


def test_structure_declaration():
    lexer = Lexer("foo = { bar }")
    tokens = lexer.generate_tokens()
    assert Token(TOKENS.NAME, "foo", 0, 0) == tokens[0]
    assert Token(TOKENS.EQUAL, "=", 0, 4) == tokens[1]
    assert Token(TOKENS.LEFT_CURLY_BRACE, "{", 0, 6) == tokens[2]
    assert Token(TOKENS.NAME, "bar", 0, 8) == tokens[3]
    assert Token(TOKENS.RIGHT_CURLY_BRACE, "}", 0, 12) == tokens[4]
