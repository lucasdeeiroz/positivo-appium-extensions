from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class TerminateApplicationExtension:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Terminate Application Extension")
    def terminate_application(self, app_id):
        """Termina o aplicativo especificado pelo app_id."""
        self.driver.terminate_app(app_id)
