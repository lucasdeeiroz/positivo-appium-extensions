# Long Press (Long-Press) - AppiumLibrary Extension

A keyword for performing long press gestures on Android or iOS app elements during automated testing with Appium and Robot Framework.

## Basic Usage

```robotframework
*** Settings ***
Library    AppiumLibrary
Library    AppiumLongPressExtensions.py

*** Test Cases ***
Long Press Example
    Long-Press    id=button_id    2000    # Press for 2 seconds
```

## Arguments

- `locator`: Element identifier in `strategy=value` format
  - Example: `id=button_id`, `xpath=//android.widget.Button`
  - Supports any WebDriver strategy (id, xpath, accessibility id, etc)
- `duration`: (optional) Press duration in milliseconds
  - Default: 1000ms (1 second)

## Practical Examples

```robotframework
# Press button for 8 seconds
LongP    id=com.app.example:id/menu_button    8000

# Press text element for 5 seconds
LongP    xpath=//android.widget.TextView[@text="Options"]    5000

# Press using default duration (1 second)
LongP    accessibility_id=menu_button
```

## How to Run Tests

Run all test cases with:

```shell
robot test_long_press.robot
```

### Requirements

- AppiumLibrary installed
- Physical device or emulator connected
- Appium Server running

## Technical Details

- Uses Selenium WebDriver's ActionChains
- Works with any WebDriver locator strategy
- Accepts custom duration in milliseconds
- Handles errors for non-existent elements
- Validated on Android emulators (physical device tests pending)

## Use Cases

- Opening context menus
- Selecting multiple items
- Activating features that require long press
- Custom gestures on interface elements

For complete usage examples, including error handling, see [`test_long_press.robot`](./test_long_press.robot).
