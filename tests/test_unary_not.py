import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import ExprStmt, Unary
from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_not_flips_booleans_and_double_not_flips_back():
    assert run("hallucinate(!✅, !❌, !!✅)✨") == "❌ ✅ ✅\n"


def test_not_works_on_boolean_variables_and_conditions():
    source = """slop ready = ❌✨
vibe !ready {
    hallucinate(!ready)✨
}"""
    assert run(source) == "✅\n"


def test_not_binds_tighter_than_equality():
    assert run("hallucinate(!✅ == ❌)✨") == "✅\n"


def test_not_is_a_unary_expression():
    (statement,) = parse(tokenize("!✅✨"))
    assert isinstance(statement, ExprStmt)
    assert isinstance(statement.expression, Unary)
    assert statement.expression.operator.type is TokenType.BANG


def test_double_not_is_nested_unary_expressions():
    (statement,) = parse(tokenize("!!✅✨"))
    assert isinstance(statement, ExprStmt)
    outer = statement.expression
    assert isinstance(outer, Unary) and outer.operator.type is TokenType.BANG
    assert isinstance(outer.operand, Unary) and outer.operand.operator.type is TokenType.BANG


@pytest.mark.parametrize(
    ("literal", "type_name"),
    [
        ("1", "number"),
        ("“text”", "string"),
    ],
)
def test_not_rejects_non_booleans(literal: str, type_name: str):
    assert fails(f"hallucinate(!{literal})✨") == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got {type_name}"
    )
