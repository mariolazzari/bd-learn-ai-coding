import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTERPRETER = ROOT / "sloperator.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INTERPRETER), *args], capture_output=True, encoding="utf-8"
    )


def test_runs_a_file():
    completed = run_cli(str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 0
    assert completed.stdout == "hello, slop\n"
    assert completed.stderr == ""


def test_error_goes_to_stderr_after_earlier_output(tmp_path: Path):
    program = tmp_path / "boom.slop"
    program.write_text("hallucinate(“before”)✨\nhallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == "before\n"
    assert completed.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
    assert "Traceback" not in completed.stderr


def test_missing_file_and_usage():
    assert run_cli().returncode == 2
    missing = run_cli(str(ROOT / "nope.slop"))
    assert missing.returncode == 2
    assert "could not read" in missing.stderr


def test_check_mode_accepts_syntax_without_executing(tmp_path: Path):
    program = tmp_path / "runtime_error.slop"
    program.write_text("hallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_check_mode_does_not_print(tmp_path: Path):
    program = tmp_path / "print.slop"
    program.write_text("hallucinate(“executed”)✨\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 0
    assert "executed" not in completed.stdout


def test_check_flag_may_follow_the_path(tmp_path: Path):
    program = tmp_path / "ok.slop"
    program.write_text("slop x = 1✨\n", encoding="utf-8")
    completed = run_cli(str(program), "--check")
    assert completed.returncode == 0


def test_check_reports_a_syntax_error(tmp_path: Path):
    program = tmp_path / "broken.slop"
    program.write_text("slop x = 1\n", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert "syntax error" in completed.stderr
    assert "Traceback" not in completed.stderr


def test_check_reports_a_lexical_error(tmp_path: Path):
    program = tmp_path / "quotes.slop"
    program.write_text('hallucinate("hi")✨\n', encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 1
    assert "lexical error" in completed.stderr


def test_validate_is_an_alias_for_check(tmp_path: Path):
    program = tmp_path / "ok.slop"
    program.write_text("slop x = 1✨\n", encoding="utf-8")
    assert run_cli("--validate", str(program)).returncode == 0


def test_check_usage_and_unknown_option():
    assert run_cli("--check").returncode == 2
    assert run_cli("--nope", "x.slop").returncode == 2
    assert "unknown option '--nope'" in run_cli("--nope", "x.slop").stderr
