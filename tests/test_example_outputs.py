"""Exact stdout for examples that demonstrate a language feature."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
EXPECTED_OUTPUT = {
    "equality": "✅\n❌\n❌\n",
    "short-circuit": "❌\n✅\n",
}


@pytest.mark.parametrize(("stem", "expected"), EXPECTED_OUTPUT.items(), ids=EXPECTED_OUTPUT.keys())
def test_example_output(stem: str, expected: str):
    path = EXAMPLES / f"{stem}.slop"
    result = run_source(path.read_text(encoding="utf-8"))
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected
