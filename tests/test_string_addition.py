from sloperator.runner import run_source


def evaluate_expression(expression: str) -> str:
    result = run_source(f"hallucinate({expression})✨")
    assert result.stderr == "", result.stderr
    return result.stdout


def test_empty_string_on_the_left_is_the_identity():
    assert evaluate_expression("“” + “slop”") == "slop\n"


def test_empty_string_on_the_right_is_the_identity():
    assert evaluate_expression("“slop” + “”") == "slop\n"


def test_adding_two_empty_strings_yields_an_empty_string():
    assert evaluate_expression("“” + “”") == "\n"


def test_concatenation_preserves_non_ascii_characters():
    assert evaluate_expression("“café” + “✨”") == "café✨\n"


def test_concatenation_with_emoji_on_either_side():
    assert evaluate_expression("“✨” + “café”") == "✨café\n"


def test_concatenation_is_not_commutative_for_ordering():
    assert evaluate_expression("“a” + “b”") == "ab\n"
    assert evaluate_expression("“b” + “a”") == "ba\n"


def test_concatenation_chains_left_to_right():
    assert evaluate_expression("“” + “slo” + “p” + “”") == "slop\n"


def test_concatenation_of_variables_holding_strings():
    source = """slop greeting = “café”✨
slop sparkle = “✨”✨
hallucinate(greeting + sparkle)✨
hallucinate(greeting + “”)✨
hallucinate(“” + sparkle)✨"""
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.stdout == "café✨\ncafé\n✨\n"


def test_concatenation_does_not_mutate_operands():
    source = """slop base = “slop”✨
slop joined = base + “✨”✨
hallucinate(base)✨
hallucinate(joined)✨"""
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.stdout == "slop\nslop✨\n"


def test_string_plus_number_is_a_runtime_error():
    result = run_source("hallucinate(“slop” + 1)✨")
    assert result.exit_code == 1
    assert result.stderr == (
        "SlopLang runtime error at line 1: operands of '+' must both be numbers "
        "or both be strings, got string and number\n"
    )


def test_number_plus_string_is_a_runtime_error():
    result = run_source("hallucinate(1 + “slop”)✨")
    assert result.exit_code == 1
    assert result.stderr == (
        "SlopLang runtime error at line 1: operands of '+' must both be numbers "
        "or both be strings, got number and string\n"
    )
