from typing import List, Optional
from pathlib import Path

import os
import subprocess
import sys

import typer


def main(
    path: Path = typer.Option(
        ...,
        "--path", "-p",
        help="Path of the sub pre-commit call."
    ),
    files: Optional[List[Path]] = typer.Argument(
        None,
        help="List of files to pass to sub pre-commit.",
    ),
):
    relevant_files = []
    if files:  # No files means --all-files was used
        for file in files:
            if file.is_relative_to(path):
                relevant_files.append(file)
        if not relevant_files:
            print("Nothing to check, existing")
            return
    
    print(f"Running pre-commit for {path}")
    os.chdir(path)
    result = subprocess.run(
        [
            "pre-commit",
            "run",
            "--files",
            *[
                str(file.relative_to(path))
                for file
                in relevant_files
            ]
        ],
    )
    if result.returncode != 0:
        sys.exit(1)


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
