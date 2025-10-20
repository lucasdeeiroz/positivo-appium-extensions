from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import time
import re

class WaitMultipleElements:
    """Class to wait for multiple elements simultaneously."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # Estratégias de localização válidas
    VALID_STRATEGIES = ['id', 'xpath', 'accessibility_id', 'class_name', 'css selector', 'name', 
                        'android uiautomator', 'ios class chain', 'ios predicate']
    # Tempo máximo permitido para timeout (5 minutos)
    MAX_TIMEOUT = 300

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()
        
    def _validate_locator(self, locator):
        """
        Valida se um locator está no formato strategy=value e usa uma estratégia válida.
        """
        if not isinstance(locator, str):
            raise ValueError(f"Locator must be a string, got {type(locator).__name__}: {repr(locator)}")
            
        # Aceita xpath começando com // sem precisar de prefixo
        if locator.startswith('//'):
            return True
            
        # Verifica o formato strategy=value
        match = re.match(r'^([a-zA-Z_\s]+)=(.+)$', locator)
        if not match:
            raise ValueError(f"Invalid locator format: {locator}. Must be 'strategy=value' or start with '//'")
            
        strategy = match.group(1).lower().strip()
        if strategy not in self.VALID_STRATEGIES:
            valid_strategies_str = ', '.join(self.VALID_STRATEGIES)
            raise ValueError(f"Invalid strategy in locator '{locator}'. Valid strategies are: {valid_strategies_str}")
            
        return True

    @keyword("Wait Multiple Elements")
    def wait_multiple_elements(self, elements_list, timeout=10, wait_for_all=True, polling_interval=0.5):
        """Waits for multiple elements to be visible with configurable strategies.
        
        Continuously polls for element visibility using the provided locators
        and applies different waiting strategies based on the wait_for_all parameter.
        
        [Arguments]
        - ``elements_list``: List of element locators in format 'strategy=value' or XPath starting with '//'
        - ``timeout``: Maximum time to wait in seconds (1-300)
        - ``wait_for_all``: If True, waits until ALL elements are visible; if False, waits until ANY element is visible
        - ``polling_interval``: Time between visibility checks in seconds (must be less than timeout)
        
        [Return Values]
        Dictionary with locator strings as keys and boolean visibility status as values:
        - True: Element is visible
        - False: Element is not visible
        
        [Examples]
        | @{locators}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
        | ${result}=      Wait Multiple Elements    ${locators}    timeout=15    wait_for_all=True
        | Should Be True  ${result['id=button1']}
        
        | @{locators}=    Create List    id=loading    id=error
        | ${result}=      Wait Multiple Elements    ${locators}    wait_for_all=False
        | Log             ${result}
        
        [Raises]
        - ``ValueError``: If parameters are invalid (empty list, malformed locators, invalid timeout values)
        - ``TimeoutError``: If elements do not become visible within the timeout period
        - ``RuntimeError``: If Appium driver is unavailable or session is invalid
        """
        # Input validation
        if not isinstance(elements_list, list):
            raise ValueError("elements_list must be a list of locators")
        
        if not elements_list:
            raise ValueError("The elements list cannot be empty")
            
        # Validate each locator format
        for idx, locator in enumerate(elements_list):
            try:
                self._validate_locator(locator)
            except ValueError as e:
                raise ValueError(f"Invalid locator at position {idx}: {str(e)}")

        # Timeout validation
        try:
            timeout = float(timeout)
            if timeout <= 0:
                raise ValueError("timeout must be a positive number")
            if timeout > self.MAX_TIMEOUT:
                raise ValueError(f"timeout cannot exceed {self.MAX_TIMEOUT} seconds")
        except (ValueError, TypeError) as e:
            raise ValueError("timeout must be a positive numeric value") from e

        # Polling interval validation
        try:
            polling_interval = float(polling_interval)
            if polling_interval <= 0:
                raise ValueError("polling_interval must be a positive number")
            if polling_interval >= timeout:
                raise ValueError("polling_interval must be smaller than timeout")
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
            # Validar disponibilidade do driver
            driver = self._driver
            if driver is None:
                raise RuntimeError("Appium driver is not available - ensure Appium session is initialized")
                
            # Validar sessão do driver
            try:
                session_id = driver.session_id
                if not session_id:
                    raise RuntimeError("Appium driver session is not valid - session may have been closed")
                self._builtin.log(f"Driver session is valid (ID: {session_id})", level='DEBUG')
            except Exception as session_error:
                raise RuntimeError(f"Failed to validate Appium driver session: {str(session_error)}")

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
            if isinstance(e, (TimeoutError, ValueError)):
                raise
            elif isinstance(e, RuntimeError) and "Appium driver" in str(e):
                raise
            elif "Invalid locator" in str(e):
                raise ValueError(str(e))
            else:
                raise RuntimeError(f"Error waiting for multiple elements visibility: {str(e)}")