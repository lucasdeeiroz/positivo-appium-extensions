from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
import warnings

@keyword("Click A Point")
def click_a_point(x, y, duration=100):
    """
    Clicks at a specific point on the screen using absolute coordinates.

    Args:
        x (int): X coordinate on the screen.
        y (int): Y coordinate on the screen.
        duration (int): Duration of the click in milliseconds.
    """
    # Validate arguments
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        raise ValueError("The 'x' and 'y' arguments must be integers.")
        
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("The 'duration' argument must be a positive integer.")

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

        # Check if coordinates are within screen bounds
        if x < 0 or x > screen_width or y < 0 or y > screen_height:
            warnings.warn(f"Coordinates ({x}, {y}) are outside the screen bounds ({screen_width}x{screen_height}). Adjusting to fit.")
            x = max(0, min(x, screen_width))
            y = max(0, min(y, screen_height))

        # Create an instance of ActionChains
        actions = ActionChains(driver)

        # Define touch pointer
        touch = actions.w3c_actions.add_pointer_input('touch', 'finger')

        # Configure the click action
        touch.create_pointer_move(x=x, y=y)
        touch.create_pointer_down()
        touch.create_pause(duration / 1000)  # Convert to seconds
        touch.create_pointer_up()

        # Perform the actions
        actions.perform()
        
        return True

    except Exception as e:
        raise RuntimeError(f"Error while performing the click action: {str(e)}")