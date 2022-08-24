import sys

import typer


def main(name: str = "world"):
    print(f"Hello {name}")
    print(sys.argv)


if __name__ == "__main__":
    typer.run(main)
