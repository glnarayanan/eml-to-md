# Contributing to eml-to-md

Thanks for your interest in contributing! This document covers the guidelines and workflow for contributing to eml-to-md.

## Getting Started

```bash
git clone https://github.com/glnarayanan/eml-to-md.git
cd eml-to-md
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
```

This installs the package in editable mode along with dev dependencies (pytest, ruff).

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feat/your-feature-name
```

Use a descriptive branch name prefixed with the change type: `feat/`, `fix/`, `docs/`, `test/`, `refactor/`.

### 2. Make Your Changes

- **Code** lives in `src/eml_to_md/`
- **Tests** live in `tests/`
- **Test fixtures** (sample `.eml` files) live in `tests/fixtures/`

### 3. Run Tests and Lint

All tests must pass and code must be lint-clean before submitting:

```bash
pytest
ruff check src/ tests/
```

### 4. Commit

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

Write commit messages that explain **why**, not just what. Keep commits atomic — one logical change per commit.

### 5. Open a Pull Request

- Reference any related issues (e.g., `Fixes #12`)
- Describe what you changed and why
- Include any testing notes if the change is non-trivial

## Code Standards

- **Python 3.9+** — avoid syntax or stdlib features from 3.10+ unless gated
- **Type hints** on all public functions
- **Docstrings** on all public functions (Google style)
- **Ruff** for linting (`ruff check`), configured in `pyproject.toml`
- Follow existing patterns in the codebase for naming and structure

## Adding Test Fixtures

If you're adding a new email edge case:

1. Create a minimal `.eml` file in `tests/fixtures/`
2. Add a corresponding pytest fixture in `tests/conftest.py`
3. Write tests that exercise the new case

Keep fixture emails as small as possible — include only what's needed to reproduce the scenario.

## Reporting Bugs

Open a [GitHub issue](https://github.com/glnarayanan/eml-to-md/issues) with:

- The `.eml` file (or a minimal reproduction) that triggers the bug
- Expected vs. actual output
- Your Python version (`python --version`)

**Note:** If the bug involves a security vulnerability, see [SECURITY.md](SECURITY.md) instead.

## Suggesting Features

Open an issue tagged with the `enhancement` label. Describe the use case and, if possible, sketch out the API or CLI change you'd like to see.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
