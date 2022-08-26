# sub-pre-commit

When dealing with more complex repositories or simply put monorepos
`pre-commit` will come to its limits. The reason is mainly that `pre-commit`
only allows for one global config file which will create difficulties when
your project parts have different needs. In particular monorepos will have
this issue when combining different technologies.

`sub-pre-commit` tries to solve this by allowing you to create a config file
for each of the parts in your mono repo. Let's create a simple example
by using the following file structure:

```
.
├── .pre-commit-config.yaml
├── ...
└── src
    ├── frontend
    │   ├── package.json
    │   ├── .eslintrc.js
    │   ├── ...
    │   └── .pre-commit-config.yaml
    └── backend
        ├── pyproject.toml
        ├── .flake8
        ├── ...
        └── .pre-commit-config.yaml
```

The different parts of the project now have their own config file, but
if we use the normal `script` or even `system` hooks `pre-commit` provides
we cannot get this working.

Let's see how `pre-commit` works for explanation:
* When you call `pre-commit` it will collect all staged files.
* It will then execute all hooks configured in the `pre-commit-config.yaml`
  you have put into the repository root.
* Each hook will be passed a list of the staged file names and thus can use
  this list to only work on those files.

This is all fine, but now we have two different project parts which have their
respective linter config files (in this example `.eslintrc.js` and `.flake8`)
inside sub folders. You may use these files with normal `pre-commit`, but this
may result in file rules mismatches. This means if you configured `flake8`
to handle files in `migrations/` a different way then `pre-commit` will not
be able to handle this correctly as it runs in the repository root - which
means the path would have to be passed as `src/backend/migrations/`, but
using this will break your normal CLI usage.

This of course could work if you just put the `.pre-commit-config.yaml` into
`src/backend/`, but then `pre-commit` would fail to use the config. Also we
still could only have one pre-commit hook installed and thus cannot support
frontend and backend.

**This is where `sub-pre-commit` comes into play.**

Let's put the following contents into the `.pre-commit-config.yaml` in the
repository root:

```yaml
repos:
  - repo: https://github.com/ddanier/sub-pre-commit.git
    rev: v0.1.0
    hooks:
      - id: sub-pre-commit
        alias: frontend
        name: "pre-commit for src/frontend/"
        args: ["-p", "src/frontend"]
        files: "^src/frontend/.*"
      - id: sub-pre-commit
        alias: backend
        name: "pre-commit for src/backend/"
        args: ["-p", "src/backend"]
        files: "^src/backend/.*"
```

`sub-pre-commit` will now be called by `pre-commit` like any other hook. It will
then execute `pre-commit` again, but will first:
* Take the list of files `pre-commit` passed and remove the prefix - according
  to the path given in `-p`.
* If no files match the own path prefix - the `sub-pre-commit` will just exit.
  (This is just to be sure, the config already filtered for the correct path)
* Change the working directory into the folder passed using `-p`.
* Then it will execute `pre-commit run` passing all those matched files.
  (Actually what happens is quite more complex, as `pre-commit` will not allow
  this. `sub-pre-commit` will run a monkey patched version of `pre-commit`. See
  "Warnings" below)
* Your linter config paths now just match. 😉👍

Looking at `src/backend/.pre-commit-config.yaml` this could then look like:

```yaml
repos:
  - repo: https://github.com/PyCQA/flake8
    rev: v5.0.4
    hooks:
      - id: flake8
        args: ["--config=.flake8"]
        additional_dependencies:
          - flake8-builtins
          - flake8-annotations
          # ...
```

## Warnings

`sub-pre-commit` will itself install `pre-commit` as a dependency, so it can
patch the behaviour of `pre-commit` to not always run all commands from the git
repository root. This may cause issues in the future and makes choosing the
`sub-pre-commit` version accordingly. `sub-pre-commit` will include tags for
different versions of `pre-commit`, so you are required to keep those in sync.
Running `pre-commit autoupdate` might break your configuration as the
`pre-commit` version included in `sub-pre-commit` might then be different.

Use at your own risk.
