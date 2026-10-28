"""Regression tests for assignment through nested bare blocks."""

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == ""
    assert result.exit_code == 0
    return result.stdout


def test_assignment_in_nested_block_updates_nearest_binding():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨"""
    assert run(source) == "3\n1\n"


def test_nested_block_reads_enclosing_block_binding():
    source = """{
    slop outer = 10✨
    {
        hallucinate(outer)✨
    }
}"""
    assert run(source) == "10\n"


def test_nested_block_assignment_without_shadowing_updates_outer_block():
    source = """{
    slop value = 1✨
    {
        value = 2✨
    }
    hallucinate(value)✨
}"""
    assert run(source) == "2\n"


def test_block_local_binding_does_not_leak_to_global_scope():
    source = """{
    slop hidden = 1✨
}
hallucinate(hidden)✨"""
    result = run_source(source)
    assert result.stdout == ""
    assert result.stderr == "SlopLang runtime error at line 4: undefined variable 'hidden'\n"
