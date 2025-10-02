from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.extensions.applications import Applications


class TerminateApplicationExtension:
    """
    Class to handle application termination in Appium
    This class provides keywords to terminate an application
    Additionally, it allows retrieval of the current application ID(appPackage) and activity(appActivity) for your own use.
    This is useful for testing scenarios where you need to ensure the application is closed
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        """Returns the current Appium driver instance."""
        try:
            return self._builtin.get_library_instance("AppiumLibrary")._current_application()
        except Exception as e:
            raise RuntimeError(f"Failed to get AppiumLibrary instance. Ensure AppiumLibrary is imported and a session is active. Error: {str(e)}")

    @keyword("Terminate Application Extension")
    def terminate_application(self, app_id):
        """
        Terminates the application specified by app_id.
        
        Args:
            app_id (str): The application package identifier (e.g., 'com.example.app')
        
        Raises:
            ValueError: If app_id is empty or invalid
            RuntimeError: If driver is not available or termination fails
            
        Example:
            | Terminate Application Extension | com.google.android.youtube |
        """
        # Validate app_id parameter
        if not app_id:
            raise ValueError("app_id parameter cannot be empty")
        
        if not isinstance(app_id, str):
            raise TypeError(f"app_id must be a string, got {type(app_id).__name__}")
        
        app_id = app_id.strip()
        if not app_id:
            raise ValueError("app_id parameter cannot be empty or whitespace only")
        
        # Validate app_id format (basic Android package name validation)
        if not self._is_valid_package_name(app_id):
            raise ValueError(f"Invalid app_id format: '{app_id}'. Expected format: 'com.example.app'")
        
        try:
            driver = self.driver
            self._builtin.log(f"Attempting to terminate application: {app_id}", level="INFO")
            
            # Check if app is running before terminating
            if not driver.is_app_installed(app_id):
                raise RuntimeError(f"Application '{app_id}' is not installed on the device")
            
            result = driver.terminate_app(app_id)
            
            if result:
                self._builtin.log(f"Successfully terminated application: {app_id}", level="INFO")
            else:
                self._builtin.log(f"Application '{app_id}' was not running or already terminated", level="WARN")
                
            return result
            
        except RuntimeError:
            # Re-raise RuntimeError with original message
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to terminate application '{app_id}': {str(e)}")

    @keyword("Get Current App Id")
    def get_current_app_id(self):
        """
        Returns the appPackage (app_id) of the current session.
        
        Returns:
            str: The application package identifier
            
        Raises:
            RuntimeError: If driver is not available or app_id cannot be retrieved
            
        Example:
            | ${app_id}= | Get Current App Id |
            | Log | Current app: ${app_id} |
        """
        try:
            driver = self.driver
            app_id = driver.desired_capabilities.get("appPackage")
            
            if not app_id:
                raise RuntimeError("Could not retrieve appPackage from current session. Session may not be active.")
            
            self._builtin.log(f"Current application ID: {app_id}", level="INFO")
            return app_id
            
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to get current app ID: {str(e)}")
    
    def _is_valid_package_name(self, package_name):
        """
        Validates if the package name follows Android package naming conventions.
        
        Args:
            package_name (str): The package name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not package_name or not isinstance(package_name, str):
            return False
        
        # Basic validation: must contain at least one dot and alphanumeric characters
        parts = package_name.split('.')
        if len(parts) < 2:
            return False
        
        # Each part should contain only alphanumeric characters and underscores
        for part in parts:
            if not part or not all(c.isalnum() or c == '_' for c in part):
                return False
            # Cannot start with a number
            if part[0].isdigit():
                return False
        
        return True