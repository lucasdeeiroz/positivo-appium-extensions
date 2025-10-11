"""
Zoom Element Library
====================

Custom Robot Framework library for performing a realistic pinch-out (zoom-in)
gesture on Android/iOS using Appium and Selenium W3C Pointer Actions.

Overview
--------
- Works on a target element (by locator) or at screen center when no locator is provided.
- Adjustable zoom scale (> 1.0), gesture duration, direction (vertical/horizontal),
  movement amplitude, and interpolation steps.
- Validates input arguments and constrains finger coordinates to the visible screen bounds.
- Produces clear Robot Framework logs for troubleshooting and reproducibility.

Requirements
------------
- Python 3.7+
- Appium Server configured and running
- Robot Framework:
    pip install robotframework
- AppiumLibrary:
    pip install robotframework-appiumlibrary
- Selenium (bundled with AppiumLibrary dependencies)

Import in Robot Framework
-------------------------
Library    GestureZoom.py
Library    AppiumLibrary

Usage
-----
Perform Zoom Gesture    locator=<strategy=value>|None    scale=<float>    duration=<ms>
...                     direction=<vertical|horizontal>  movement=<px>    pause=<s>    steps=<int>

Examples
--------
*** Settings ***
Library    GestureZoom.py
Library    AppiumLibrary

*** Test Cases ***
Zoom On Element (Vertical)
    Perform Zoom Gesture    locator=id=map_view    scale=1.8    duration=700    direction=vertical    movement=280

Zoom At Screen Center (Horizontal)
    Perform Zoom Gesture    scale=2.0    direction=horizontal    movement=300    steps=60

Parameters
----------
locator    (str | None)  Locator of the element to zoom in on. If None, uses the screen center. Default: None.
scale      (float)       Zoom scale factor (> 1.0 required). Default: 1.5.
duration   (int)         Gesture duration in milliseconds. Default: 500.
direction  (str)         Gesture direction: "vertical" or "horizontal". Default: "vertical".
movement   (int|float)   Distance in pixels each finger moves from the center. Default: 300.
pause      (float)       Pause in seconds before movement starts. Default: 0.1.
steps      (int)         Number of interpolation steps for gesture realism. Default: 50.

Notes
-----
- Uses Selenium ActionChains (W3C Pointer Actions) to synthesize a two-finger zoom-in.
- Finger start positions are placed close to the center and move outward symmetrically.
- Coordinates are clamped to the device screen size to avoid out-of-bounds gestures.

Errors/Exceptions
-----------------
- ValueError: if `scale` ≤ 1.0, invalid `direction`, non-positive `duration`/`movement`,
  or malformed `locator` (must be "strategy=value" when provided).
- RuntimeError: if Appium driver is unavailable, the element cannot be found, or any
  error occurs during gesture execution (wrapped with a descriptive message).
- WebDriverException (from underlying driver): if the session becomes invalid or the device
  cannot perform the requested pointer actions.
"""


import random
import warnings

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton


class GestureZoom:
    """Custom Gesture Extension Class for AppiumLibrary with enhanced zoom gesture."""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        # Retrieves the current Appium driver instance from AppiumLibrary
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    def _get_element_center(self, locator):
        # Identifies the element and calculates its center point
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        element = appium_lib._element_find(locator, True, True)
        if not element:
            raise RuntimeError(f"Element not found for locator: {locator}")
        location = element.location
        size = element.size
        x, y = location['x'], location['y']
        width, height = size['width'], size['height']
        return x + width / 2, y + height / 2, element

    def _calculate_finger_final_positions(self, x, y, scale, movement, direction):
        # Defines the final finger positions based on gesture center, scale, and movement range
        displacement = scale * movement
        if direction.lower() == "vertical":
            return (x, y - displacement), (x, y + displacement)
        else:
            return (x - displacement, y), (x + displacement, y)

    def _adjust_to_screen_bounds(self, positions, screen_width, screen_height):
        # Ensures finger coordinates are within screen bounds
        adjusted_positions = []
        for x, y in positions:
            new_x = max(0, min(x, screen_width))
            new_y = max(0, min(y, screen_height))
            if (x, y) != (new_x, new_y):
                warnings.warn(
                    f"Finger position ({x}, {y}) adjusted to ({new_x}, {new_y}) to fit within screen bounds.")
            adjusted_positions.append((new_x, new_y))
        return adjusted_positions

    def _validate_zoom_args(self, locator, scale, duration, direction, movement):
        # Validates gesture arguments for correctness and safety
        if locator is not None:
            if not isinstance(locator, str) or not locator:
                raise ValueError("The 'locator' must be a non-empty string.")
            if '=' not in locator:
                raise ValueError(f"Locator '{locator}' must be in the format 'strategy=value'")
        if scale <= 1.0:
            raise ValueError("Scale must be greater than 1.0")
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("Direction must be 'vertical' or 'horizontal'.")
        if movement <= 0:
            raise ValueError("Movement must be positive")

    @keyword("Perform Zoom Gesture")
    def perform_zoom_gesture(self, locator=None, scale=1.5, duration=500, direction="vertical", movement=300, pause=0.1, steps=50):
        """
        Performs a realistic zoom gesture with perturbation.

        Args:
            locator (str): Element locator (optional; if None, uses screen center).
            scale (float): Gesture scale (> 1.0).
            duration (int): Total duration of the gesture in milliseconds.
            direction (str): Gesture direction ("vertical" or "horizontal").
            movement (int/float): Gesture amplitude in pixels.
            pause (int/float): Pause in seconds before movement begins.
            steps (int): Number of interpolation steps for gesture realism.
        """

        self._validate_zoom_args(locator, scale, duration, direction, movement)

        try:
            driver = self.driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            if locator is None:
                center_x = screen_width / 2
                center_y = screen_height / 2
                self._builtin.log("No locator provided. Using center of the screen.", "INFO")
            else:
                center_x, center_y, _ = self._get_element_center(locator)
                self._builtin.log(f"Element center at ({center_x}, {center_y})", "INFO")

            offset = 10
            f1_start = (center_x, center_y - offset) if direction == "vertical" else (center_x - offset, center_y)
            f2_start = (center_x, center_y + offset) if direction == "vertical" else (center_x + offset, center_y)

            f1_end, f2_end = self._calculate_finger_final_positions(center_x, center_y, scale, movement, direction)

            f1_start, f1_end, f2_start, f2_end = self._adjust_to_screen_bounds(
                [f1_start, f1_end, f2_start, f2_end], screen_width, screen_height)

            self._builtin.log(f"Finger 1 starts at ({f1_start})", "INFO")
            self._builtin.log(f"Finger 2 starts at ({f2_start})", "INFO")

            actions = ActionChains(driver)
            actions.w3c_actions.devices = []
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pointer_down(button=MouseButton.LEFT)

            finger1.create_pause(pause)
            finger2.create_pause(pause)

            for i in range(1, steps + 1):
                t = i / steps
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0]) + random.uniform(-0.0, 0.0)
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1]) + random.uniform(-0.0, 0.0)
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0]) + random.uniform(-0.0, 0.0)
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1]) + random.uniform(-0.0, 0.0)

                interp_f1_x, interp_f1_y = max(0, min(interp_f1_x, screen_width)), max(0, min(interp_f1_y, screen_height))
                interp_f2_x, interp_f2_y = max(0, min(interp_f2_x, screen_width)), max(0, min(interp_f2_y, screen_height))

                move_duration = int(duration / steps)
                finger1.create_pointer_move(x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            finger1.create_pointer_up(button=MouseButton.LEFT)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()
            self._builtin.log("Zoom gesture performed successfully.", "INFO")

        except Exception as e:
            raise RuntimeError(f"Error while performing the zoom gesture: {str(e)}")
