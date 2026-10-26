from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt
from sloperator.runner import run_source


def evaluate_expression(expression: str) -> str:
    result = run_source(f"hallucinate({expression})✨")
    assert result.stderr == "", result.stderr
    return result.stdout


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_comparison_binds_tighter_than_equality():
    expr = only_expression("1 < 2 == ✅✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, Binary) and expr.left.operator.type is TokenType.LESS


def test_comparison_true_equals_true():
    assert evaluate_expression("1 < 2 == ✅") == "✅\n"


def test_equality_right_operand_is_a_full_comparison():
    assert evaluate_expression("✅ == 1 < 2") == "✅\n"


def test_arithmetic_binds_tighter_than_comparison():
    assert evaluate_expression("1 + 1 < 3 == ✅") == "✅\n"
