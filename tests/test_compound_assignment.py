"""Runtime behavior of the compound assignment operator +=."""

import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    return result.stdout


def test_plus_equal_adds_to_current_value():
    source = """slop n = 2✨
n += 3 * 4✨
hallucinate(n)✨"""
    assert run(source) == "14\n"


def test_plus_equal_evaluates_right_hand_side_before_adding():
    source = """slop n = 1✨
n += n + 1✨
hallucinate(n)✨"""
    assert run(source) == "3\n"


def test_plus_equal_concatenates_strings():
    source = """slop greeting = “hello”✨
greeting += “, slop”✨
hallucinate(greeting)✨"""
    assert run(source) == "hello, slop\n"


def test_plus_equal_updates_the_nearest_binding():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score += 10✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨"""
    assert run(source) == "12\n1\n"


def test_plus_equal_can_be_repeated():
    source = """slop total = 0✨
total += 1✨
total += 2✨
total += 3✨
hallucinate(total)✨"""
    assert run(source) == "6\n"


@pytest.mark.parametrize(
    ("source", "message"),
    [
        (
            "missing += 1✨",
            "undefined variable 'missing'",
        ),
        (
            "loadbearing LIMIT = 1✨\nLIMIT += 1✨",
            "cannot assign to loadbearing 'LIMIT'",
        ),
        (
            "slop n = 1✨\nn += “slop”✨",
            "operands of '+=' must both be numbers or both be strings, got number and string",
        ),
        (
            "slop s = “slop”✨\ns += 1✨",
            "operands of '+=' must both be numbers or both be strings, got string and number",
        ),
    ],
)
def test_plus_equal_runtime_errors(source: str, message: str):
    result = run_source(source)
    assert result.stdout == ""
    assert result.exit_code == 1
    assert message in result.stderr
