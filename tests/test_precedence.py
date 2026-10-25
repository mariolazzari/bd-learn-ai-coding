from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Grouping
from sloperator.runner import run_source


def evaluate_expression(expression: str) -> str:
    result = run_source(f"hallucinate({expression})✨")
    assert result.stderr == "", result.stderr
    return result.stdout


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_tighter_than_addition():
    expr = only_expression("2 + 3 * 4✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.PLUS
    assert isinstance(expr.right, Binary) and expr.right.operator.type is TokenType.STAR


def test_addition_is_below_multiplication_on_either_side():
    assert evaluate_expression("2 + 3 * 4") == "14\n"
    assert evaluate_expression("2 * 3 + 4") == "10\n"


def test_grouping_overrides_multiplication_precedence():
    expr = only_expression("(2 + 3) * 4✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.STAR
    assert isinstance(expr.left, Grouping)
    assert evaluate_expression("(2 + 3) * 4") == "20\n"
