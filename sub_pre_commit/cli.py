import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer


def main(
    path: Path = typer.Option(
        ...,
        "--path", "-p",
        help="Path of the sub pre-commit call.",
    ),
    files: Optional[List[Path]] = typer.Argument(
        None,
        help="List of files to pass to sub pre-commit.",
    ),
    config_file: str = typer.Option(
        ".pre-commit-config.yaml",
        "--config-file", "-c",
        help="Path to the configuration file for sub pre-commit.",
    ),
) -> None:
    relevant_files = []
    if files:  # No files mean --all-files was used
        for file in files:
            if file.is_relative_to(path):
                relevant_files.append(file)
        if not relevant_files:
            print("Nothing to check")
            return

    print(f"Running pre-commit for {path}:")
    print("-" * 79)
    print("")

    os.chdir(str(path.resolve()))

    cmd = [
        "sub-pre-commit-run",
        "run",
        "--config-file",
        config_file,
    ]
    if files:
        cmd.extend([
            "--files",
            *[
                str(file.relative_to(path))
                for file
                in relevant_files
            ],
        ])
    else:
        cmd.append("--all-files")

    result = subprocess.run(cmd)

    print("")
    print("-" * 79)
    print("")

    if result.returncode != 0:
        sys.exit(1)


def run() -> None:
    typer.run(main)


if __name__ == "__main__":
    run()
