import subprocess
import sys


def run_flake8():
    """הרצת Flake8 לבדיקה אם הקוד עומד בתקני PEP8."""
    print("Running Flake8...")
    result = subprocess.run([sys.executable, "-m", "flake8", "--max-line-length=88"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Flake8 Passed: No style errors found.")
    else:
        print("Flake8 Errors:")
        print(result.stdout)


def run_black_check():
    """בדיקה האם הקוד עומד בתקן Black (ללא שינויים בפועל)."""
    print("Running Black (Check Mode)...")
    result = subprocess.run([sys.executable, "-m", "black", "--check", "--diff", "."], capture_output=True, text=True)
    if result.returncode == 0:
        print("Black Passed: Code formatting is correct.")
    else:
        print("Black Formatting Issues:")
        print(result.stdout)


def run_black_fix():
    """הרצת Black עם תיקון אוטומטי של הקוד."""
    print("Running Black (Auto-Fix Mode)...")
    result = subprocess.run([sys.executable, "-m", "black", "."], capture_output=True, text=True)
    print(result.stdout)
    print("Black Formatting Applied.")


if __name__ == "__main__":
    run_flake8()
    run_black_check()
    print("Use 'python code_quality_tests.py --fix' to auto-fix formatting errors.")
    if "--fix" in sys.argv:
        run_black_fix()
