from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import warnings

class AppiumZoomExtensions6_1:
    """Classe para executar gestos de zoom in com Appium."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Perform Zoom_2")
    def perform_zoom_in_gesture(self, locator, scale=1.5, duration=50, direction="vertical", pause_s=0.5):
        """
        Performs a zoom in gesture on an Android application.

        Args:
            locator (str): Element locator.
            scale (float): Gesture scale (must be > 1.0).
            duration (int): Movement duration in milliseconds.
            direction (str): Gesture direction ("vertical" or "horizontal").
            pause_s (float): Pause in seconds before the movement starts.
        """
        # Validate arguments
        if not isinstance(locator, str) or not locator:
            raise ValueError("The 'locator' argument must be a non-empty string.")
        if scale <= 1.0:
            raise ValueError("The 'scale' argument must be greater than 1.0 for Zoom In.")
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("The 'duration' argument must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("The 'direction' argument must be 'vertical' or 'horizontal'.")
        if not isinstance(pause_s, (int, float)) or pause_s < 0:
            raise ValueError("The 'pause_s' argument must be a non-negative number.")

        try:
            driver = self._driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            element = appium_lib._element_find(locator, True, True)
            if not element:
                raise RuntimeError(f"Element not found for locator: {locator}")

            location = element.location
            x, y = location['x'], location['y']
            width, height = element.size['width'], element.size['height']
            center_x, center_y = x + width / 2, y + height / 2

            # Calculate end positions for fingers (starting closer to center, moving outward)
            if direction.lower() == "vertical":
                finger1_start_x, finger1_start_y = center_x, center_y - 10
                finger2_start_x, finger2_start_y = center_x, center_y + 10
                finger1_end_x, finger1_end_y = center_x, center_y - (center_y * (scale - 1))
                finger2_end_x, finger2_end_y = center_x, center_y + (center_y * (scale - 1))
            elif direction.lower() == "horizontal":
                finger1_start_x, finger1_start_y = center_x - 10, center_y
                finger2_start_x, finger2_start_y = center_x + 10, center_y
                finger1_end_x, finger1_end_y = center_x - (center_x * (scale - 1)), center_y
                finger2_end_x, finger2_end_y = center_x + (center_x * (scale - 1)), center_y

            # Adjust to stay within screen
            def adjust(x, y):
                return max(0, min(x, screen_width)), max(0, min(y, screen_height))

            finger1_start_x, finger1_start_y = adjust(finger1_start_x, finger1_start_y)
            finger2_start_x, finger2_start_y = adjust(finger2_start_x, finger2_start_y)
            finger1_end_x, finger1_end_y = adjust(finger1_end_x, finger1_end_y)
            finger2_end_x, finger2_end_y = adjust(finger2_end_x, finger2_end_y)

            actions = ActionChains(driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            finger1.create_pointer_move(x=finger1_start_x, y=finger1_start_y)
            finger2.create_pointer_move(x=finger2_start_x, y=finger2_start_y)

            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pointer_down(button=MouseButton.LEFT)

            finger1.create_pause(pause_s)
            finger2.create_pause(pause_s)

            finger1.create_pointer_move(x=finger1_end_x, y=finger1_end_y, duration=duration)
            finger2.create_pointer_move(x=finger2_end_x, y=finger2_end_y, duration=duration)

            finger1.create_pointer_up(button=MouseButton.LEFT)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()

        except Exception as e:
            raise RuntimeError(f"Error while performing the zoom in gesture: {str(e)}")
