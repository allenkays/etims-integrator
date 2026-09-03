# Contributing

Thanks for contributing! Please follow these steps when working on the project.

Development setup
- Create a virtual environment and install deps:

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

Running tests
- Run the test suite with `pytest`:

  ```bash
  pytest -q
  ```

Branching and PRs
- Create feature branches from `develop` named `feature/your-feature`.
- Open PRs to `develop` for features and to `main` for release/hotfix branches.

Commit messages
- Use Conventional Commits (e.g. `feat:`, `fix:`, `chore:`).

PR checklist
- CI passes (tests and linting)
- Clear description and linked issue (if applicable)
- At least one approving review

Thank you for improving the project!
