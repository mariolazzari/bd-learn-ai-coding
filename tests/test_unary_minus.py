import pytest

from sloperator.runner import run_source


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


@pytest.mark.parametrize("literal", ["✅", "❌"])
def test_unary_minus_rejects_boolean_literals(literal: str):
    assert fails(f"hallucinate(-{literal})✨") == (
        "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean"
    )
