"""Parser coverage for the compound assignment operator +=."""

import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary


def test_plus_equal_lexes_as_one_token():
    tokens = tokenize("n += 3")
    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.EOF,
    ]
    assert tokens[1].lexeme == "+="


def test_plus_equal_does_not_break_plain_plus():
    tokens = tokenize("a + b")
    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]


def test_plus_equal_parses_as_assign_statement():
    program = parse(tokenize("n += 3 * 4✨"))
    assert len(program) == 1
    statement = program[0]
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "n"
    assert statement.operator.type is TokenType.PLUS_EQUAL


def test_plus_equal_keeps_operator_precedence_on_the_right():
    program = parse(tokenize("n += 3 * 4✨"))
    statement = program[0]
    assert isinstance(statement, Assign)
    value = statement.value
    assert isinstance(value, Binary)
    assert value.operator.type is TokenType.STAR


def test_plus_equal_requires_a_terminator():
    with pytest.raises(SlopSyntaxError) as info:
        parse(tokenize("n += 3"))
    assert info.value.message == "expected ✨ after assignment, but reached end of file"


def test_plus_equal_requires_an_expression():
    with pytest.raises(SlopSyntaxError) as info:
        parse(tokenize("n += ✨"))
    assert info.value.message == "expected an expression, found '✨'"


def test_plus_equal_is_not_an_expression():
    with pytest.raises(SlopSyntaxError) as info:
        parse(tokenize("hallucinate(n += 1)✨"))
    assert info.value.message == "expected ')' after arguments, found '+='"
