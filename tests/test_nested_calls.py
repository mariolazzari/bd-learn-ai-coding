from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_call_as_argument_to_another_call():
    source = """clanker double(n) {
    ship n * 2✨
}
clanker add(a, b) {
    ship a + b✨
}
hallucinate(add(double(3), double(4)))✨"""
    assert run(source) == "14\n"
