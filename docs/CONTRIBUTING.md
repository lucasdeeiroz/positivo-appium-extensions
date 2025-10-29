# Contributing to AppiumLibrary Extension

Thank you for your interest in contributing to this project!  
This library extends the Robot Framework's AppiumLibrary with new and restructured keywords aligned with Appium 2.0, covering both gesture-based actions and broader mobile automation needs.  

This guide explains how to contribute with quality and in alignment with the best practices of the open source community.

---

## Table of Contents

- How to Contribute
- Project Structure
- Code Style Guidelines
- Commit Message Guidelines
- Documentation Standards
- Required Tests
- Pull Request Process
- Pull Request Checklist
- Release Notes
- Code of Conduct
- Questions?

---

## How to Contribute

You can contribute in several ways:
- Creating new keywords (like gestures, swipes, taps)
- Fixing bugs or unexpected behaviors
- Improving existing keywords
- Expanding test coverage
- Documentation contributions are highly welcome and include:
  - Improvements to `README.md` (installation, examples, troubleshooting)
  - Robot examples (in `tests/`) demonstrating the keywords
  - Keyword docstrings (description, arguments, usage examples, common errors)
  - Inline code comments that improve readability

**Principles:**
- Clarity > quantity: prioritize executable examples and concise steps
- Keep examples in sync with the current behavior of the keyword
- If you change a keyword’s signature/behavior, immediately update README, docs, and examples
- Before starting, check if an **issue already exists** for your idea. If not, feel free to open one.

---

## Project Structure

- `keywords/` → Python classes implementing new keywords  
- `resources/` → Robot resources (variables, setups)  
- `tests/` → Robot Framework test suites organized by functionality  
- `docs/` → Extended documentation and usage guides

---

## Tooling Setup

To ensure consistent code style and automated checks across all contributors, set up the following tools locally:

```bash
pip install --upgrade pip
pip install pre-commit black ruff
pre-commit install
```

Create a `.pre-commit-config.yaml` file at the project root:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        args: ["--line-length", "120", "--target-version", "py312"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: ["--select", "E,F,W,I,B,UP", "--target-version", "py312"]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

**Quick tips**
- Run all hooks manually: `pre-commit run --all-files`
- Run lint manually: `ruff check .`
- Reformat code manually: `black .`

---

## Code Style Guidelines

- Formatter: Use Black with line-length = 120 (helps readability in long Robot/Appium calls)
- Linter: Use Ruff with rules E,F,W,I,B,UP and target-version = py312
  - `I` handles import sorting; no separate `isort` is needed
- Follow **PEP8** for Python code formatting.
- Align with the structure used in AppiumLibrary:
  - Use the `@keyword` decorator to expose methods to Robot Framework
  - Class names should be in `PascalCase`
  - Helper functions should be prefixed with `_` if private
- Keep the code modular, readable, and well commented.
- If you change user-facing behavior or arguments, update docstrings and README/docs accordingly

**Example:**

```python
from robot.api.deco import keyword

@keyword("Get Visible Elements On Screen")
def get_visible_elements_on_screen(...):
    """Description of the keyword goes here"""
    ...
```

---

## Commit Message Guidelines

- Use [Conventional Commits](https://www.conventionalcommits.org/)  
- Examples:
- `feat: add pinch gesture keyword with W3C actions`
- `fix: handle stale element in visible elements`
- `docs: add usage examples for Tap At Percentage`
- `chore: reorganize resources structure and update paths`
- `test: add negative test case for Scroll To Element with invalid locator`
- `refactor: simplify gesture helper methods and improve readability`

---

## Documentation Standards

- A clear docstring explaining its purpose, arguments, and examples
- Informative logs using *self._builtin.log()*
- Updates to the *README.md* file with usage instructions
- If applicable, additions to the *docs/* folder for more detailed documentation

---

## Required Tests

- Each keyword must have positive and negative test cases
- All tests must be written using Robot Framework syntax
- Unit tests with mocks are welcome when helpful
- Organize test cases by type or functionality
- Make sure to run all tests locally with *robot* and confirm they pass

**Example:**

```robot
*** Test Cases ***
Return all visible elements
    Get Visible Elements On Screen    all    auto    debug=True
```

---

## Pull Request Process

1. Fork this repository
2. Create a descriptive branch for your change
3. Write your code and the required test cases
4. Document your changes thoroughly
5. Push and open a Pull Request (PR)

Each PR should include:
- A description of what was implemented or fixed
- Instructions on how to test the functionality
- References to related issues (if applicable)
- Screenshots or logs (if helpful for verification)

---

## Pull Request Checklist

Before submitting your PR, make sure:

- [ ] Your code is formatted with Black (120 columns) and passes Ruff lint (E,F,W,I,B,UP, py312) 
- [ ] Pre-commit hooks were executed locally (pre-commit run --all-files)
- [ ] Your code follows AppiumLibrary conventions and is clearly commented  
- [ ] Your keyword is documented with a detailed docstring  
- [ ] You added logs via `self._builtin.log()` for easier debugging  
- [ ] You updated the `README.md` with usage examples or changes  
- [ ] You created positive and negative test cases for your keyword  
- [ ] You ran all tests locally and confirmed they pass  
- [ ] Your branch name is clear and descriptive (`feat/`, `fix/`, `docs/`, etc.)  
- [ ] Your commits are meaningful and linked to issues (if applicable)

---

## Code of Conduct

We follow the Contributor Covenant Code of Conduct.
Respect, inclusion, and constructive collaboration are core values in this project.

---

## Questions?

If you have any questions, open an issue or leave a comment on your Pull Request.

Thank you for contributing

---

**Project context:**  
Developed under the **CEPEDI Technology Residency Program**, coordinated by **SOFTEX** and supported by **MCTI**.