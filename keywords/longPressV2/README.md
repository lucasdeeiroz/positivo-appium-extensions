# Long Press — AppiumLibrary Extension

**LongP** is a custom keyword designed to perform the long press gesture on elements in Android or iOS apps during automated tests with Appium and Robot Framework.
It uses Selenium WebDriver’s ActionChains to simulate pressing and holding an element for a specified duration.

## Purpose

- Make long press actions easier without writing repetitive code in test cases.
- Precisely control the duration of the press.
- Support any locator strategy compatible with WebDriver (`id`, `xpath`, `accessibility id`, etc.).
- Enable advanced interaction tests such as:
  - Opening context menus
  - Selecting multiple items
  - Activating hidden features that require a long press

## How It Works

The keyword accepts:

- `locator` — element identifier in the format `strategy=value`, e.g.:
  - `id=com.app.example:id/button`
  - `xpath=//android.widget.TextView[@text="Option"]`
- `duration` (optional) — press time in milliseconds (default: 1000 = 1 second)

Execution flow:

1. The locator is split into strategy and value.
2. The element is located using the Appium driver.
3. An ActionChains object is created to:
   - Click and hold the element (`click_and_hold`)
   - Pause for the specified duration (`pause(duration/1000)`)
   - Release the element (`release`)
4. The action is executed with `.perform()`

## How To Execute

Run all test cases with:

```shell
robot test_long_press.robot
```

Requirements:

- AppiumLibrary and the LongP keyword must be imported.
- A connected physical device or emulator.

Example usage in a `.robot` file:

```robotframework
*** Settings ***
Library    AppiumLibrary
Library    AppiumLongPressExtensions.py

*** Test Cases ***
Long Press Example
		Open Application    http://localhost:4723/wd/hub    platformName=Android    deviceName=emulator-5554    appPackage=com.example    appActivity=.MainActivity
		LongP    id=com.app.example:id/menu_button    2000
```

## Technical Details

- Built using ActionChains from Selenium WebDriver.
- Works directly with the Appium driver instance from AppiumLibrary.
- Accepts any WebDriver-supported locator strategy.
- Converts milliseconds to seconds before executing the pause.

## Code Structure

Class: `AppiumLongPressExtensions`

- Scope: Global (implicitly when loaded as a Robot Framework library)
- Methods:
  - `_driver` → gets the current Appium driver instance
  - `long_press(locator, duration)` → performs the long press

## Test Structure

The keyword was validated in:

- **Mocked Tests**
  - Default press (1s) — duration omitted
  - Extended press (3s) — `duration=3000`
  - Non-existent element — ensures exception handling
  - Invalid locator format — ensures error is raised
- **Emulator Tests**
  - Opened context menu in a list
  - Selected multiple items via long press
  - Activated a hidden feature requiring long press
- **Physical Device Tests (Pending)**
  - Not yet validated on physical devices but compatible with both Android

# Keyword: LongP

This keyword allows you to perform a long press on a screen element using Appium.

## How to use

1. Make sure to import the `AppiumLongPressExtensions.py` file in your `.robot` or `.resource` file:

```robotframework
Library    ./AppiumLongPressExtensions.py
```

2. Use the `LongP` keyword in your tests:

```robotframework
LongP    <locator>    <duration>
```

### Arguments

- `locator`: Element locator in the format `strategy=value` (e.g. `id=my_id`, `xpath=//my/xpath`).
- `duration`: (optional) Long press duration in milliseconds (default: 1000ms).

### Examples

```robotframework
LongP    id=com.google.android.calculator:id/digit_8    8000
LongP    xpath=//android.widget.TextView[@content-desc="Gmail"]    5000
```

## Test usage examples

See the [`test_long_press.robot`](./test_long_press.robot) file for complete usage examples, including success and error handling cases.

## Notes

- The locator must be in the format `strategy=value`. Otherwise, an error will be raised.
- The `duration` argument is optional, but can be provided to set the long press time.
- If the element is not found or does not support long press, an error will be raised.
