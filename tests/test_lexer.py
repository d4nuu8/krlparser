#!/usr/bin/env python3
# -*- coding(): utf-8 -*-

import os
import pytest

from krlparser.lexer import Lexer
from krlparser.token import Token, TOKENS


def test_invalid_input():
    with pytest.raises(ValueError):
        Lexer(code=None)

    with pytest.raises(ValueError):
        Lexer(code=0)


def test_unknown_input():
    lexer = Lexer(code="~foo")
    tokens = lexer.generate_tokens()
    assert TOKENS.ERROR_TOKEN == tokens[0].token_type
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=1)
            == tokens[1])


def test_peek_at_eol():
    lexer = Lexer(code="foo =")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.EQUAL,
                  value="=",
                  line_number=0,
                  column=4)
            == tokens[1])


def test_end_of_file():
    lexer = Lexer(code="")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NEWLINE,
                  value=os.linesep,
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.END_OF_FILE,
                  value=None,
                  line_number=0,
                  column=0)
            == tokens[1])


def test_comment():
    lexer = Lexer(code=";Test")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.COMMENT,
                  value="Test",
                  line_number=0,
                  column=0)
            == tokens[0])


def test_single_line_string():
    lexer = Lexer(code="\"Hello, World!\"")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.STRING,
                  value="Hello, World!",
                  line_number=0,
                  column=0)
            == tokens[0])


def test_multine_line_string_terminated_by_eof():
    lexer = Lexer(code="\"Hello, World!")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.STRING,
                  value="Hello, World!",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert TOKENS.ERROR_TOKEN == tokens[1].token_type


def test_multine_line_string_terminated_by_eol():
    lexer = Lexer(code="\"Hello, World!\n")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.STRING,
                  value="Hello, World!",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert TOKENS.ERROR_TOKEN == tokens[1].token_type


def test_file_attribute():
    lexer = Lexer(code="&Test")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.FILE_ATTRIBUTE,
                  value="Test",
                  line_number=0,
                  column=0)
            == tokens[0])


@pytest.mark.parametrize("keyword", ["global", "def", "end"])
def test_keyword(keyword):
    lexer = Lexer(code=keyword)
    tokens = lexer.generate_tokens()
    assert (Token(token_type=keyword.upper(),
                  value=keyword,
                  line_number=0,
                  column=0)
            == tokens[0])


def test_id():
    lexer = Lexer(code="IDdTest")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="IDdTest",
                  line_number=0,
                  column=0)
            == tokens[0])


def test_id_with_whitespaces():
    lexer = Lexer(code="   IDdTest   ")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="IDdTest",
                  line_number=0,
                  column=3)
            == tokens[0])

    lexer = Lexer(code="\tIDdTest\t")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="IDdTest",
                  line_number=0,
                  column=1)
            == tokens[0])


def test_hex_digit():
    lexer = Lexer(code="'H1F")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.INTEGER,
                  value=int("1f", 16),
                  line_number=0,
                  column=0)
            == tokens[0])


def test_invalid_hex_digit():
    lexer = Lexer(code="'H1FJ")
    tokens = lexer.generate_tokens()
    assert TOKENS.ERROR_TOKEN == tokens[0].token_type


def test_bin_digit():
    lexer = Lexer(code="'B1010'")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.INTEGER,
                  value=int("1010", 2),
                  line_number=0,
                  column=0)
            == tokens[0])


def test_integer():
    lexer = Lexer(code="12345")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.INTEGER,
                  value=12345,
                  line_number=0,
                  column=0)
            == tokens[0])


def test_real():
    lexer = Lexer(code="1.1")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.REAL,
                  value=1.1,
                  line_number=0,
                  column=0)
            == tokens[0])

    lexer = Lexer(code="1E3")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.REAL,
                  value=1E3,
                  line_number=0,
                  column=0)
            == tokens[0])

    lexer = Lexer(code="1.3E3")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.REAL,
                  value=1.3E3,
                  line_number=0,
                  column=0)
            == tokens[0])

    lexer = Lexer(code="1.3E-3")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.REAL,
                  value=1.3E-3,
                  line_number=0,
                  column=0)
            == tokens[0])


def test_structure_access():
    lexer = Lexer(code="foo.bar")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.DOT,
                  value=".",
                  line_number=0,
                  column=3)
            == tokens[1])
    assert (Token(token_type=TOKENS.NAME,
                  value="bar",
                  line_number=0,
                  column=4)
            == tokens[2])


def test_function_call():
    lexer = Lexer(code="Test(foo, bar)")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="Test",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.LEFT_BRACE,
                  value="(",
                  line_number=0,
                  column=4)
            == tokens[1])
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=5)
            == tokens[2])
    assert (Token(token_type=TOKENS.COMMA,
                  value=",",
                  line_number=0,
                  column=8)
            == tokens[3])
    assert (Token(token_type=TOKENS.NAME,
                  value="bar",
                  line_number=0,
                  column=10)
            == tokens[4])
    assert (Token(token_type=TOKENS.RIGHT_BRACE,
                  value=")",
                  line_number=0,
                  column=13)
            == tokens[5])


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
    lexer = Lexer(code=f"foo {string} bar")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=token,
                  value=string,
                  line_number=0,
                  column=4)
            == tokens[1])
    assert (Token(token_type=TOKENS.NAME,
                  value="bar",
                  line_number=0,
                  column=5 + len(string))
            == tokens[2])


def test_array_access():
    lexer = Lexer(code="foo[bar]")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.LEFT_SQUARE_BRACE,
                  value="[",
                  line_number=0,
                  column=3)
            == tokens[1])
    assert (Token(token_type=TOKENS.NAME,
                  value="bar",
                  line_number=0,
                  column=4)
            == tokens[2])
    assert (Token(token_type=TOKENS.RIGHT_SQUARE_BRACE,
                  value="]",
                  line_number=0,
                  column=7)
            == tokens[3])


def test_enum_access():
    lexer = Lexer(code="foo = #bar")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.EQUAL,
                  value="=",
                  line_number=0,
                  column=4)
            == tokens[1])
    assert (Token(token_type=TOKENS.HASH,
                  value="#",
                  line_number=0,
                  column=6)
            == tokens[2])
    assert (Token(token_type=TOKENS.NAME,
                  value="bar",
                  line_number=0,
                  column=7)
            == tokens[3])


def test_structure_declaration():
    lexer = Lexer(code="foo = { bar }")
    tokens = lexer.generate_tokens()
    assert (Token(token_type=TOKENS.NAME,
                  value="foo",
                  line_number=0,
                  column=0)
            == tokens[0])
    assert (Token(token_type=TOKENS.EQUAL,
                  value="=",
                  line_number=0,
                  column=4)
            == tokens[1])
    assert (Token(token_type=TOKENS.LEFT_CURLY_BRACE,
                  value="{",
                  line_number=0,
                  column=6)
            == tokens[2])
    assert (Token(token_type=TOKENS.NAME,
                  value="bar",
                  line_number=0,
                  column=8)
            == tokens[3])
    assert (Token(token_type=TOKENS.RIGHT_CURLY_BRACE,
                  value="}",
                  line_number=0,
                  column=12)
            == tokens[4])
