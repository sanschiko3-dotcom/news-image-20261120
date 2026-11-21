"""Deterministically copy assets/entry.png to the grader's output directory.

Use only the stdlib, with no network access or rendering at runtime.
MAKEFUN_OUTPUT_DIR selects the output directory, defaulting to /output.
"""
import os
from pathlib import Path
import shutil

def main() -> None:
    output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    # Creating the output directory is idempotent with parents and exist_ok.
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().parent / 'assets' / 'entry.png', output / 'entry.png')

if __name__ == '__main__':
    main()
