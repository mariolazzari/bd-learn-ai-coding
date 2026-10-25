import pytest

from sloperator.errors import LexicalError
from sloperator.lexer.scanner import tokenize


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ("a # b", 1, "unexpected character '#'"),
        ("a\n\n  $", 3, "unexpected character '$'"),
    ],
)
def test_unexpected_character_fallback(source: str, line: int, message: str):
    with pytest.raises(LexicalError) as info:
        tokenize(source)
    assert info.value.line == line
    assert info.value.message == message
    assert str(info.value) == f"SlopLang lexical error at line {line}: {message}"
