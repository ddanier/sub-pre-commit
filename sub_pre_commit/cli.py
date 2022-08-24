from typing import ItemsView, List, Optional
from pathlib import Path

import sys
import os

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
    if files:
        for file in files:
            if file.is_relative_to(path):
                relevant_files.append(file)
        if not relevant_files:
            print("Nothing to check, existing")
            return
    
    print(relevant_files)
    


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
