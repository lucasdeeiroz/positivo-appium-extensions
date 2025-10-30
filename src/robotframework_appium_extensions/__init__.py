"""
RobotFramework Appium Extensions
================================
Additional keywords for Robot Framework's AppiumLibrary.

Developed within the Technology Residency Program, executed by CEPEDI,
coordinated by SOFTEX, and supported by MCTI, with the participation
of Positivo Tecnologia as the partner company that proposed the development challenge.

This package can be imported in two ways:
- Full import:     `Library    robotframework_appium_extensions`
  → Loads all keywords automatically.

- Specific import: `Library    robotframework_appium_extensions.keywords.ClickElements`
  → Loads only the desired keyword module.
"""

import importlib
import pkgutil
from pathlib import Path


_keywords_path = Path(__file__).parent / "keywords"


for _, module_name, _ in pkgutil.iter_modules([str(_keywords_path)]):
    module = importlib.import_module(f"robotframework_appium_extensions.keywords.{module_name}")
    globals().update(vars(module))


__all__ = [
    module_name
    for _, module_name, _ in pkgutil.iter_modules([str(_keywords_path)])
]
