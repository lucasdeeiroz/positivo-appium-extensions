from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import time

class ClickElements:
    """Class to execute sequential clicks on multiple elements."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Click Elements")
    def click_elements(self, elements_list, click_duration=100, interval_between_clicks=0.5):
        """Clicks sequentially on multiple elements using Appium's touch actions.
        
        Executes clicks on each element in the provided list, in sequence. 
        If an element is not found, a WARN level log message is generated and the keyword 
        continues with the next element without failing. A delay between clicks can be configured.
        
        [Arguments]
        - ``elements_list``: List of element locators (id, xpath, accessibility_id, etc.)
        - ``click_duration``: Duration of each click in milliseconds (1-2000)
        - ``interval_between_clicks``: Time between clicks in seconds (must be non-negative)
        
        [Return Values]
        None. The keyword completes after all elements are clicked or attempted.
        
        [Examples]
        | @{elements}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
        | Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
        
        | @{calculator_buttons}=    Create List    id=digit_1    id=digit_2    id=plus    id=equals
        | Click Elements    ${calculator_buttons}
        
        [Raises]
        - ``TypeError``: If parameters have incompatible types (non-list elements_list, non-numeric duration)
        - ``ValueError``: If parameter values are outside acceptable ranges (empty list, negative intervals)
        - ``RuntimeError``: If driver is unavailable or element operations fail
        """
        # Validate elements_list type
        if elements_list is None:
            raise TypeError("elements_list cannot be None - a list of locator strings is required")
        if not isinstance(elements_list, list):
            raise TypeError(f"elements_list must be a list of locator strings, got {type(elements_list).__name__}")
        
        # Validate elements_list is not empty
        if not elements_list:
            raise ValueError("The elements list cannot be empty - at least one locator is required")

        # Validate each element in the list is a string
        for idx, item in enumerate(elements_list):
            if not isinstance(item, str):
                raise TypeError(
                    f"All elements in elements_list must be strings (locators). "
                    f"Invalid item at position {idx}: {repr(item)} (type: {type(item).__name__})"
                )
                    
        # Validate click_duration
        if click_duration is None:
            raise TypeError("click_duration cannot be None - a positive number is required")
        if not isinstance(click_duration, (int, float)):
            raise TypeError(f"click_duration must be a number (int or float), got {type(click_duration).__name__}")
        if click_duration <= 0:
            raise ValueError(f"click_duration must be positive, got {click_duration}")
        if click_duration > 2000:
            raise ValueError(f"click_duration cannot exceed 2000ms, got {click_duration}")
            
        # Validate interval_between_clicks
        if interval_between_clicks is None:
            raise TypeError("interval_between_clicks cannot be None - a non-negative number is required")
        if not isinstance(interval_between_clicks, (int, float)):
            raise TypeError(f"interval_between_clicks must be a number (int or float), got {type(interval_between_clicks).__name__}")
        if interval_between_clicks < 0:
            raise ValueError(f"interval_between_clicks cannot be negative, got {interval_between_clicks}")
            
        try:
            # Validate driver existence
            driver = self._driver
            if driver is None:
                raise RuntimeError("Appium driver is not available - ensure a session is started")
            
            # Validate driver session
            try:
                session_id = driver.session_id
                if not session_id:
                    raise RuntimeError("Appium driver session is not valid - session may have been closed")
                self._builtin.log(f"Driver session is valid (ID: {session_id})", level='DEBUG')
            except AttributeError:
                raise RuntimeError("Failed to validate Appium driver session - driver object is invalid")
            except Exception as session_error:
                raise RuntimeError(f"Failed to validate Appium driver session: {str(session_error)}")

            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            
            self._builtin.log(f"Starting sequential click on {len(elements_list)} elements", level='INFO')
            
            for i, locator in enumerate(elements_list, 1):
                self._builtin.log(f"Clicking element {i}/{len(elements_list)}: {locator}", level='INFO')
                
                # Find element
                element = appium_lib._element_find(locator, True, True)
                if not element:
                    self._builtin.log(f"Element not found: {locator}", level='WARN')
                    continue
                
                # Get location and size
                location = element.location
                size = element.size
                
                # Calculate center coordinates
                center_x = location['x'] + size['width'] / 2
                center_y = location['y'] + size['height'] / 2
                
                # Execute click
                actions = ActionChains(driver)
                touch = actions.w3c_actions.add_pointer_input('touch', 'finger')
                
                touch.create_pointer_move(x=center_x, y=center_y)
                touch.create_pointer_down(button=0)
                touch.create_pause(click_duration / 1000)
                touch.create_pointer_up(button=0)
                
                actions.perform()
                
                self._builtin.log(f"Click executed on element {i}: {locator}", level='INFO')
                
                # Pause between clicks (except for the last one)
                if i < len(elements_list):
                    time.sleep(interval_between_clicks)
                    
        except (TypeError, ValueError) as e:
            # Re-raise parameter validation exceptions without modification
            raise
        except RuntimeError as e:
            # Re-raise runtime errors without modification
            raise
        except Exception as e:
            # Wrap other exceptions with detailed context
            raise RuntimeError(f"Error executing multiple clicks: {str(e)}")