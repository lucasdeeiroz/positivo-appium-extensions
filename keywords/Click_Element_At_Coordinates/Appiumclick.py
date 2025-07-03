import time
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import KEY

class Appiumclick:

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('ClickC')
    def clickC(self, locator, xoffset, yoffset):
        driver = self._driver
        appium_lib = self._builtin.get_library_instance('AppiumLibrary')

        self._builtin.log("Checking if the driver is active", level='INFO')
        if not driver:
            raise RuntimeError("Driver is not initialized or not connected to the device.")

        self._builtin.log(f"Searching for element with locator: {locator}", level='INFO')
        try:
            element = appium_lib.get_webelement(locator)
        except Exception as e:
            raise ValueError(f"Element with locator '{locator}' not found: {e}")

        location = element.location
        size = element.size
        self._builtin.log(f"Element location: {location}, Size: {size}", level='INFO')

        try:
            xoffset = float(xoffset)
            yoffset = float(yoffset)
        except Exception:
            raise ValueError("xoffset and yoffset must be numbers (pixels or fractions from 0 to 1 for percentage)")

        if 0 <= xoffset <= 1:
            xoffset_px = int(size['width'] * xoffset)
        else:
            xoffset_px = int(xoffset)
        if 0 <= yoffset <= 1:
            yoffset_px = int(size['height'] * yoffset)
        else:
            yoffset_px = int(yoffset)

        x = location['x'] + xoffset_px
        y = location['y'] + yoffset_px
        self._builtin.log(f"Calculated click coordinates: ({x}, {y}) (offsets: {xoffset_px}, {yoffset_px})", level='INFO')

        window_size = driver.get_window_size()
        self._builtin.log(f"Screen size: {window_size}", level='INFO')

        if not (0 <= x <= window_size['width'] and 0 <= y <= window_size['height']):
            raise ValueError(f"Coordinates ({x}, {y}) are outside the device screen.")

        try:
            self._builtin.log("Performing click using W3C Actions", level='INFO')

            touch = PointerInput("touch", "finger")
            actions = ActionBuilder(driver, mouse=touch)

            actions.pointer_action.move_to_location(x, y)
            actions.pointer_action.pointer_down()
            time.sleep(0.2)
            actions.pointer_action.pointer_up()

            actions.perform()

            self._builtin.log("Click successfully performed via W3C Actions", level='INFO')
        except Exception as e:
            self._builtin.log(f"Error performing W3C Actions: {e}", level='ERROR')
            raise
