import typer


def main(name: str = "world"):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
