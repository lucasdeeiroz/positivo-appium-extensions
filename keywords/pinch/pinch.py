from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import warnings

@keyword("Perform Pinch Gesture")
def perform_pinch_gesture(locator, scale=0.5, duration=50, direction="vertical"):
    """
    Performs a pinch gesture on an Android application.

    Args:
        locator (str): Element locator.
        scale (float): Gesture scale (0.1 to 1.0).
        duration (int): Movement duration in milliseconds.
        direction (str): Gesture direction ("vertical" or "horizontal").
    """
    # Validate arguments
    if not isinstance(locator, str) or not locator:
        raise ValueError("The 'locator' argument must be a non-empty string.")
    if not (0.1 <= scale <= 1.0):
        raise ValueError("The 'scale' argument must be between 0.1 and 1.0.")
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("The 'duration' argument must be a positive integer.")
    if direction.lower() not in ["vertical", "horizontal"]:
        raise ValueError("The 'direction' argument must be 'vertical' or 'horizontal'.")

    try:
        # Get the current Appium driver
        appium_lib = BuiltIn().get_library_instance("AppiumLibrary")
        driver = appium_lib._current_application()

        if not driver:
            raise RuntimeError("The Appium driver is not available.")

        # Get screen dimensions
        screen_size = driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']

        # Locate the element using the locator and get its coordinates
        element = appium_lib._element_find(locator, True, True)
        if not element:
            raise RuntimeError(f"Element not found for locator: {locator}")

        location = element.location
        x, y = location['x'], location['y']
        width, height = element.size['width'], element.size['height']
        center_x, center_y = x + width / 2, y + height / 2

        # Calculate initial positions for fingers
        if direction.lower() == "vertical":
            finger1_start_x, finger1_start_y = center_x, center_y - center_y * scale
            finger2_start_x, finger2_start_y = center_x, center_y + center_y * scale
        elif direction.lower() == "horizontal":
            finger1_start_x, finger1_start_y = center_x - center_x * scale, center_y
            finger2_start_x, finger2_start_y = center_x + center_x * scale, center_y

        # Adjust positions to fit within screen bounds
        adjusted_positions = []
        for finger_x, finger_y in [(finger1_start_x, finger1_start_y), (finger2_start_x, finger2_start_y)]:
            adjusted_x = max(0, min(finger_x, screen_width))
            adjusted_y = max(0, min(finger_y, screen_height))
            if (finger_x != adjusted_x or finger_y != adjusted_y):
                warnings.warn(f"Finger position ({finger_x}, {finger_y}) adjusted to ({adjusted_x}, {adjusted_y}) to fit within screen bounds.")
            adjusted_positions.append((adjusted_x, adjusted_y))

        finger1_start_x, finger1_start_y = adjusted_positions[0]
        finger2_start_x, finger2_start_y = adjusted_positions[1]

        # Create an instance of ActionChains
        actions = ActionChains(driver)

        # Define two touch pointers (fingers)
        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1') 
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

        # Configure the pinch gesture
        finger1.create_pointer_move(x=finger1_start_x, y=finger1_start_y)
        finger2.create_pointer_move(x=finger2_start_x, y=finger2_start_y)

        finger1.create_pointer_down(button=MouseButton.LEFT)
        finger2.create_pointer_down(button=MouseButton.LEFT)

        finger1.create_pause(0.5)
        finger2.create_pause(0.5)

        if direction.lower() == "vertical":
            finger1.create_pointer_move(x=center_x, y=center_y - 100, duration=duration)
            finger2.create_pointer_move(x=center_x, y=center_y + 100, duration=duration)
        elif direction.lower() == "horizontal":
            finger1.create_pointer_move(x=center_x - 100, y=center_y, duration=duration)
            finger2.create_pointer_move(x=center_x + 100, y=center_y, duration=duration)

        finger1.create_pointer_up(button=MouseButton.LEFT)
        finger2.create_pointer_up(button=MouseButton.LEFT)

        # Perform the actions
        actions.perform()

    except Exception as e:
        raise RuntimeError(f"Error while performing the pinch gesture: {str(e)}")