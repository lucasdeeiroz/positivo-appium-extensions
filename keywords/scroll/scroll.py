# Import locator strategies supported by Appium (like ID, XPATH, etc.)
from appium.webdriver.common.appiumby import AppiumBy

# Enables using Python functions as Robot Framework keywords
from robot.api.deco import keyword

# Provides access to Robot Framework's internal functionalities (e.g., logging, library access)
from robot.libraries.BuiltIn import BuiltIn


# Main class that defines the custom Robot Framework library
class scroll:
    # GLOBAL scope: the same instance is reused across all test cases
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Initializes the BuiltIn library to access Robot Framework utilities (e.g., log)
        self._builtin = BuiltIn()

    @property
    def driver(self):
        # Gets the current Appium driver instance from AppiumLibrary
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    # Define the custom keyword "Scroll Inside" to be used in .robot files
    @keyword("Scroll Inside")
    def scroll_element(self, **kwargs):
        """
        Performs a swipe gesture inside a specific element, identified by ID, XPath, or other strategies.

        Parameters:
        - locator_value: value used to locate the element (e.g., //android.widget.TextView, com.example:id/button)
        - locator_type: locator strategy (optional). If not provided, it will be auto-inferred.
        - direction: scroll direction — one of 'up', 'down', 'left', 'right'. Default: 'down'
        - percent: scroll distance relative to the element size (0.01 to 1.0). Default: 0.75
        - speed: swipe speed in pixels per second. Default: 800
        """

        # Read keyword arguments
        locator_value = kwargs.get("locator_value", None)  # Required
        locator_type = kwargs.get("locator_type", None)    # Optional
        direction = kwargs.get("direction", "down")        # Default: 'down'
        percent = float(kwargs.get("percent", 0.75))       # Default: 0.75
        speed = int(kwargs.get("speed", 800))              # Default: 800

        # Validate required parameter
        if not locator_value:
            raise ValueError("Missing required parameter: 'locator_value'.")

        # If locator_type is not provided, try to infer it automatically
        if not locator_type:
            locator_type = self._infer_locator_type(locator_value)

        # Validate parameter values
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("Invalid 'direction'. Must be one of: 'up', 'down', 'left', 'right'.")
        if not (0.01 <= percent <= 1.0):
            raise ValueError("Invalid 'percent'. Must be between 0.01 and 1.0.")
        if speed <= 0:
            raise ValueError("'speed' must be a positive number.")

        # Map supported locator types to AppiumBy constants
        locator_strategies = {
            "id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "class_name": AppiumBy.CLASS_NAME,
            "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
            "ios_predicate": AppiumBy.IOS_PREDICATE,
            "ios_class_chain": AppiumBy.IOS_CLASS_CHAIN,
            "name": AppiumBy.NAME
        }

        # Convert string type into AppiumBy strategy
        strategy = locator_strategies.get(locator_type.lower())
        if not strategy:
            raise ValueError(f"Unsupported locator_type: '{locator_type}'")

        try:
            # Get the Appium driver instance
            driver = self.driver

            # Locate the element using the strategy and locator value
            element = driver.find_element(strategy, locator_value)

            # Perform the swipe gesture using mobile: swipeGesture
            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,
                "direction": direction,
                "percent": percent,
                "speed": speed
            })

            # Log success message in the Robot Framework report
            self._builtin.log(
                f"[SUCCESS] Scrolled element located by {locator_type}='{locator_value}' using direction='{direction}', percent={percent}, speed={speed}.",
                "INFO"
            )

        except Exception as e:
            # Log error in Robot Framework report
            self._builtin.log(
                f"[ERROR] Failed to scroll element '{locator_value}' (type: {locator_type}): {str(e)}",
                "ERROR"
            )
            # Raise exception to fail the test
            raise

    # Helper function to guess the locator type based on the locator_value
    def _infer_locator_type(self, locator_value):
        """
        Attempts to automatically detect the locator type based on the provided locator_value.
        """
        if locator_value.startswith("//") or locator_value.startswith("("):
            return "xpath"
        elif "=" in locator_value and not locator_value.startswith("com."):
            return "android_uiautomator"
        elif locator_value.startswith("android.widget.") or locator_value.startswith("com."):
            return "id"
        elif locator_value.isidentifier():  # simple name like "LoginButton"
            return "accessibility_id"
        else:
            return "accessibility_id"  # fallback for safety