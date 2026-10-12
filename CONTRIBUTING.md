# Contributing

Thanks for helping improve ascii-render. This guide keeps contributions
consistent and reviewable.

## Getting started

1. Fork the repo and create a feature branch from `main`.
2. Create a virtual environment and install the package in editable mode
   with dev dependencies:

   ```bash
   python -m venv .venv
   .venv/bin/pip install -e ".[dev]"
   ```

3. Run the checks you changed before opening a pull request:

   ```bash
   python -m ruff check .
   python -m ruff format .
   python -m pytest
   ```

## Code style

- Keep the core pipeline stateless and deterministic when practical.
- Prefer small, focused changes over large refactors without tests.
- Add tests for new behavior, edge cases, and bug fixes.
- Format code with Ruff before committing.

## Pull requests

- Describe the why, not just the what.
- Reference any related issue if one exists.
- Make sure the package still installs, the CLI still runs, and the tests
  still pass on the target branch.

## Reporting issues

Include the following when practical:

- Python version
- Operating system
- Exact commands used
- Input file type and size, if relevant
- Full error output

## Conduct

Please be respectful and constructive. We follow the project's
[Code of Conduct](CODE_OF_CONDUCT.md).
