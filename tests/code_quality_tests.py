
"""
Code Quality and Formatting Check Script

This script performs the following tasks:
- Checks code style compliance using `flake8`
- Checks formatting using `black` (without modifying files)
- Automatically fixes formatting issues using `black` and `autopep8` when requested

Usage:
- Run checks only: `python code_quality_tests.py`
- Run checks and auto-fix: `python code_quality_tests.py --fix`
"""

import subprocess
import sys

def run_flake8():
    """Run flake8 to check for PEP8 compliance issues."""
    print("Running Flake8...")
    result = subprocess.run(
        [sys.executable, "-m", "flake8", "--max-line-length=88"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✔ Flake8 Passed: No style errors found.")
    else:
        print("❌ Flake8 Errors:")
        print(result.stdout)

def run_black_check():
    """Run black in check mode to verify formatting."""
    print("Running Black (Check Mode)...")
    result = subprocess.run(
        [sys.executable, "-m", "black", "--check", "--diff", "."],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✔ Black Passed: Code formatting is correct.")
    else:
        print("❌ Black Formatting Issues:")
        print(result.stdout)

def run_black_fix():
    """Run black to automatically format code."""
    print("Running Black (Auto-Fix Mode)...")
    result = subprocess.run(
        [sys.executable, "-m", "black", "."], capture_output=True, text=True
    )
    print(result.stdout)
    print("✔ Black Formatting Applied.")

def run_autopep8_fix():
    """Run autopep8 to fix minor style issues."""
    print("Running autopep8 (Auto-Fix Mode)...")
    result = subprocess.run(
        [sys.executable, "-m", "autopep8", "--in-place", "--aggressive", "--aggressive", "-r", "."],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print("✔ autopep8 Formatting Applied.")

if __name__ == "__main__":
    run_flake8()
    run_black_check()
    print("ℹ Use 'python code_quality_tests.py --fix' to auto-fix formatting errors.")
    if "--fix" in sys.argv:
        run_black_fix()
        run_autopep8_fix()