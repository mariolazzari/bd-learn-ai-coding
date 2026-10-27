from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_loop_with_false_condition_never_runs_its_body():
    source = """ralph ❌ {
    hallucinate(“never”)✨
}"""
    assert run(source) == ""


def test_loop_with_false_condition_does_not_evaluate_its_body():
    # A body that would raise proves the body is skipped, not merely silent.
    source = """ralph ❌ {
    hallucinate(undefined_name)✨
}"""
    assert run(source) == ""
