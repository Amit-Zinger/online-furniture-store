import subprocess


def test_code_quality():
    """Runs Ruff code quality check and ensures it passes."""
    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
    assert result.returncode == 0, f"Code quality check failed:\n{result.stdout}\n{result.stderr}"
