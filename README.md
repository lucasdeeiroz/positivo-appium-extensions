# Robot Framework - Appium Extensions (Android)

Custom keywords extending [Robot Framework’s AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary), optimized for **mobile automation on Android**.

These extensions include **15 new or restructured keywords** for gestures, UI interactions, network checks, image comparison, and utility operations.

[![PyPI](https://img.shields.io/pypi/v/robotframework-appium-extensions.svg)]( incluir url)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)

---

## Available Keywords

- Gestures:
    - Long Press
    - Pinch
    - Scroll
    - Scroll To Element
    - Swipe
    - Zoom

- Touch utilities:
    - Click Element
    - Click Elements
    - Tap At Percentage

- Visibility & Lookup:
    - Compare Images
    - Get Visible Elements On Screen
    - Wait Multiple Elements

- System/App:
    - ChangeTheme
    - Get Network Connection Status
    - TerminateApplication

Individual documentation are in keyword docstrings.

---

## Installation

- Install Python and dependencies
- Intall Appium via npm (npm install -g appium)
- Install UiAutomator2 for Android driver (appium driver install uiautomator2)
- Clone repository and install project dependencies

```bash
git clone https://github.com/<....>.git
cd robotframework-appium-extensions
pip install .
```

---

## Requirements

- Python 3.9+
- Robot Framework 4.0+
- Appium Server 2.0 with UiAutomator2 driver
- Appium-Python-Client 5.1.1+
- ADB and Android SDK tools
- OpenCV, NumPy, scikit-image for Compare Images

## Usage Example

```robot
*** Settings ***
Library    AppiumLibrary
Library    keywords/

*** Test Cases ***
Pinch Example
    Open Application    http://localhost:4723    platformName=Android    automationName=UiAutomator2
    Perform Pinch Gesture    locator=id=map_view    scale=0.6
```

---

## Known Limitations

- Platform: tested on Android 7.0+; iOS not supported.
- Multi-touch gestures: Android 9+ recommended for reliable Pinch/Zoom (W3C Actions).
- Device fragmentation: differences between manufacturers (Samsung/Xiaomi, etc.) may affect gesture behavior.
- Dynamic elements: fast-moving/animated elements may require explicit waits.
- Power saving mode: can cause inconsistencies; disable during tests.
- Performance: image comparison may be slow on high-resolution screens.

---

## Troubleshooting

- Device not detected: run adb devices → enable USB Debugging; restart ADB (`adb kill-server && adb start-server`).
- Appium session not starting: ensure Appium 2.x is running and uiautomator2 driver installed (`appium driver install uiautomator2`).
- Element not found: validate selectors in Appium Inspector; prefer `id/accessibility_id`; use explicit waits.
- Inconsistent gestures: increase `duration/steps`; add pauses (`pause_before/pause_after`); prefer Android 9+.
- Slow/timeouts: use a good-quality USB cable; disable Android animations; increase timeouts; close background apps.
- ADB errors: ensure `adb` is in your PATH; restart ADB; reconnect the device; check permissions.

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style
- Commit messages
- Tests and documentation
- PR process

---

## License

Licensed under Apache 2.0 [LICENSE](LICENSE)
