from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import time

class WaitMultipleElements:
    """Class to wait for multiple elements simultaneously."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Wait Multiple Elements")
    def wait_multiple_elements(self, elements_list, timeout=10, wait_for_all=True, polling_interval=0.5):
        """
        Waits for multiple elements to be visible.

        Args:
            elements_list (list): List of element locators
            timeout (int): Maximum time to wait in seconds
            wait_for_all (bool): If True, waits for ALL elements; if False, waits for ANY element
            polling_interval (float): Time between checks in seconds
        
        Returns:
            dict: Dictionary with locator as key and visibility status as value
        """
        # Input validation
        if not isinstance(elements_list, list):
            raise ValueError("elements_list must be a list of locators")
        
        if not elements_list:
            raise ValueError("The elements list cannot be empty")

        # Timeout validation and conversion
        try:
            timeout = float(timeout)
            if timeout <= 0:
                raise ValueError("timeout must be a positive number")
        except (ValueError, TypeError) as e:
            raise ValueError("timeout must be a positive numeric value") from e

        # Polling interval validation
        try:
            polling_interval = float(polling_interval)
            if polling_interval <= 0:
                raise ValueError("polling_interval must be a positive number")
        except (ValueError, TypeError) as e:
            raise ValueError("polling_interval must be a positive numeric value") from e

        # Wait_for_all validation
        if not isinstance(wait_for_all, bool):
            # Convert Robot Framework strings to boolean
            if str(wait_for_all).lower() in ['true', '1', 'yes']:
                wait_for_all = True
            elif str(wait_for_all).lower() in ['false', '0', 'no']:
                wait_for_all = False
            else:
                raise ValueError("wait_for_all must be a boolean value")

        try:
            driver = self._driver
            if not driver:
                raise RuntimeError("Appium driver is not available")

            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            
            self._builtin.log(f"Starting wait for {len(elements_list)} elements to be visible (wait_for_all={wait_for_all}, timeout={timeout}s)", level='INFO')
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                results = {}
                visible_elements = 0
                
                # Check all elements in each iteration
                for locator in elements_list:
                    try:
                        element = appium_lib._element_find(locator, True, False)
                        if element and element.is_displayed():
                            results[locator] = True
                            visible_elements += 1
                            self._builtin.log(f"Element visible: {locator}", level='DEBUG')
                        else:
                            results[locator] = False
                    except Exception as e:
                        results[locator] = False
                        self._builtin.log(f"Element not found or error: {locator} - {str(e)}", level='DEBUG')
                
                # Check success conditions
                if wait_for_all and visible_elements == len(elements_list):
                    self._builtin.log(f"All {len(elements_list)} elements are visible", level='INFO')
                    return results
                elif not wait_for_all and visible_elements > 0:
                    self._builtin.log(f"{visible_elements} out of {len(elements_list)} elements are visible", level='INFO')
                    return results
                
                # Avoid unnecessary sleep on last iteration
                if time.time() - start_time + polling_interval < timeout:
                    time.sleep(polling_interval)
            
            # Timeout reached - generate final results for more informative logs
            final_results = {}
            visible_count = 0
            
            for locator in elements_list:
                try:
                    element = appium_lib._element_find(locator, True, False)
                    if element and element.is_displayed():
                        final_results[locator] = True
                        visible_count += 1
                    else:
                        final_results[locator] = False
                except Exception:
                    final_results[locator] = False
            
            # More specific error messages
            if wait_for_all:
                visible_locators = [loc for loc, status in final_results.items() if status]
                missing_locators = [loc for loc, status in final_results.items() if not status]
                
                error_msg = f"Timeout waiting for all elements to be visible. Found {visible_count}/{len(elements_list)} visible elements within {timeout}s.\n"
                error_msg += f"Visible: {visible_locators}\n"
                error_msg += f"Missing: {missing_locators}"
                
                raise TimeoutError(error_msg)
            else:
                if visible_count == 0:
                    raise TimeoutError(f"Timeout waiting for any element to be visible. No visible elements found within {timeout}s")
                else:
                    # This case shouldn't happen, but we keep it for safety
                    return final_results
                    
        except Exception as e:
            if isinstance(e, (TimeoutError, ValueError, RuntimeError)):
                raise
            raise RuntimeError(f"Error waiting for multiple elements visibility: {str(e)}")