from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn



class TerminateApplicationExtension:
    """
    Class to handle application termination in Appium
    This class provides keywords to terminate an application
    Adictionaly, it allows retrieval of the current application ID(appPackage) and activity(appActivity) for your own use.
    This is useful for testing scenarios where you need to ensure the application is closed
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Terminate Application Extension")
    def terminate_application(self, app_id):
        """Terminates the application specified by app_id."""
        self.driver.terminate_app(app_id)

    @keyword("Get Current App Id")
    def get_current_app_id(self):
        """Returns the appPackage (app_id) of the current session."""
        return self.driver.desired_capabilities.get("appPackage")