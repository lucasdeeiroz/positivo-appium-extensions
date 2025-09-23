# Contributing to AppiumLibrary Extension – Custom Gestures


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

## Code Style Guidelines

- Follow **PEP8** for Python code formatting.
- Align with the structure used in AppiumLibrary:
  - Use the `@keyword` decorator to expose methods to Robot Framework.
  - Class names should be in `PascalCase`
  - Helper functions should be prefixed with `_` if private.
- Keep the code modular, readable, and well commented.

**Example:**

```python
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
- Organize test cases by gesture type or functionality
- Make sure to run all tests locally with *robot* and confirm they pass

**Example:**

*** Test Cases ***
Return all visible elements
    Get Visible Elements On Screen    all    auto    debug=True

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

- [ ] Your code follows AppiumLibrary conventions and is clearly commented  
- [ ] Your keyword is documented with a detailed docstring  
- [ ] You added logs via `self._builtin.log()` for easier debugging  
- [ ] You updated the `README.md` with usage examples or changes  
- [ ] You created positive and negative test cases for your keyword  
- [ ] You ran all tests locally and confirmed they pass  
- [ ] Your branch name is clear and descriptive (`feat/`, `fix/`, `docs/`, etc.)  
- [ ] Your commits are meaningful and linked to issues (if applicable)

---

## Release Notes

Changes will be documented in `CHANGELOG.md`, following [Keep a Changelog](https://keepachangelog.com/).

---

## Code of Conduct

We follow the Contributor Covenant Code of Conduct.
Respect, inclusion, and constructive collaboration are core values in this project.

---

## Questions?

If you have any questions, open an issue or leave a comment on your Pull Request.
Let's work together to improve Appium-based testing!

Thank you for contributing

---