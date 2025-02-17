import subprocess


def test_code_quality():
    """Runs code quality script and checks if it completes successfully."""
    result = subprocess.run(["python", "app/code_quality_tests.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Code quality check failed: {result.stdout}"