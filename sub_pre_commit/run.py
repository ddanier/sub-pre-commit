from pre_commit import main


def run() -> None:
    # Disable munching the args so pre-commit not only runs in the git root directory
    main._adjust_args_and_chdir = lambda args: None
    # Actually run pre-commit
    main.main()


if __name__ == "__main__":
    run()
