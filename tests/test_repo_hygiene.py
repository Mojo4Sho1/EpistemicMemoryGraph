"""Repository hygiene checks for tracked transient artifacts."""

from __future__ import annotations

import re
import subprocess


def test_no_tracked_python_bytecode_or_pycache() -> None:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    tracked_paths = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    pattern = re.compile(r"(^|/)__pycache__/|\.py[co]$")
    offenders = tuple(path for path in tracked_paths if pattern.search(path))
    assert offenders == ()
