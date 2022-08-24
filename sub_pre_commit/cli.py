from typing import List, Optional
from pathlib import Path

import sys

import typer


def main(
    files: Optional[List[Path]] = typer.Option(None),
):
    print(f"Hello {name}")
    print(sys.argv)


if __name__ == "__main__":
    typer.run(main)
