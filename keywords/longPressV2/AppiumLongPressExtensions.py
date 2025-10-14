from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains


class AppiumLongPressExtensions:
    """
    Library for performing long press actions on elements using Appium.
    Provides keywords for mobile automation requiring long press gestures.
    """

    def __init__(self):
        """
        Initializes the AppiumLongPressExtensions library and sets up the BuiltIn instance.
        """
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        """
        Returns the current Appium driver instance from AppiumLibrary.
        """
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("LongP")
    def long_press(self, locator, duration=1000):
        """
        Performs a long press on the specified element for a given duration.

        Args:
            locator (str): The locator of the element to long press.
            duration (int): Duration of the long press in milliseconds. Default is 1000ms.
        Raises:
            ValueError: If the element is not found.
            RuntimeError: If the Appium driver is not initialized.
        """
        driver = self._driver

        locator_parts = locator.split("=", 1)
        if len(locator_parts) != 2:
            raise ValueError("Locator deve estar no formato 'estrategia=valor'")

        strategy, value = locator_parts

        element = driver.find_element(strategy, value)

        actions = ActionChains(driver)
        actions.click_and_hold(element).pause(duration / 1000).release().perform()
