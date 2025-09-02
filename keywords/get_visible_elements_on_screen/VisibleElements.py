from robot.api.deco import keyword
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
import json


class VisibleElements:
    """
    Custom AppiumLibrary keyword that returns visible elements on the screen using either resource-id or
    content-desc (accessibility_id on Android), optionally filtered by type.
    Useful for visual validation in mobile automation tests.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def __init__(self):
        self._builtin = BuiltIn()

    def _get_appium_driver(self):
    # Gets the current Appium driver instance
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()
    
    def _find_all_elements(self, driver):
    # Return all elements in the current screen using a generic XPath
        return driver.find_elements(By.XPATH, "//*")
    
    def _safe_attr(self, el, name):
    # Read attribute, strip, and normalize empty/null to ''.
    # Avoid repetition of the same try/except/strip/null pattern across the code
        try:
            val = el.get_attribute(name)
        except Exception:
            return ""
        if not val:
            return "" 
        val = str(val).strip()
        if not val or val.lower() == "null":
            return ""
        # Return a cleaned, non-empty value
        return val

    def _passes_filter(self, el, filter_type):
    # Check if the element matches the given filter type
        """Args:
            el (WebElement): the element to evaluate.
            filter_type (str): filter type options ('all' | 'clickable' | 'text' | 'button' | 'input').

        Returns:
            bool: Returns True if the element passes the filter, False otherwise."""
        
        class_name = self._safe_attr(el, "class") or self._safe_attr(el, "className")
        text = (el.text or "").strip()
        clickable_attr = self._safe_attr(el, "clickable")
        # Handle case-insensitivity (e.g., "True" vs "true")
        clickable = str(clickable_attr).strip().lower() == "true"

        if filter_type == "all":
            return True
        if filter_type == "clickable":
            return clickable
        if filter_type == "text":
            return bool(text)
        if filter_type == "button":
            return "Button" in class_name
        if filter_type == "input":
            return "EditText" in class_name
        # Returns False in case of an unrecognized filter (should not occur due to prior validation)
        return False
    
    def _choose_identifier(self, el, id_mode):
        """
        Returns (value, kind) according to id_mode:
          - 'auto': prefer resource-id; if empty, fallback to content-desc
          - 'resource_id': resource-id only
          - 'accessibility_id': content-desc only (Android accessibility_id alias)
        """
        rid = self._safe_attr(el, "resource-id")
        cdesc = self._safe_attr(el, "content-desc")

        if id_mode == "resource_id":
            return (rid, "resource_id") if rid else (None, None)
        if id_mode == "accessibility_id":
            return (cdesc, "accessibility_id") if cdesc else (None, None)
        # In id_mode="auto", for each element that passes filter_type:
        # - Try resource-id first; if not available, fallback to content-desc
        # - Elements with neither identifier are excluded
        # - Priority is given to resource-id, which is usually more stable
        # - Final list may mix resource-id and accessibility_id values

        if rid:
            return rid, "resource_id"
        if cdesc:
            return cdesc, "accessibility_id"
        return None, None

    def _build_debug_dict(self, el, chosen_value, chosen_kind):
    # Build a structured dictionary of element attributes for debug mode
        """Args:
            el (WebElement): the element that passed the visibility and `filter_type` checks.
            chosen_value (str): the identifier value selected according to `id_mode` (e.g., resource-id or content-desc).
            chosen_kind(str): the type of identifier selected. One of: 'resource_id' | 'accessibility_id' (on Android, accessibility_id is an alias of content-desc).

        Returns:
            dict: Structured data for debugging and inspection.
        """
        
        return {
            # Includes both id value and kind for better traceability
            "identifier": {"value": chosen_value, "kind": chosen_kind},
            "resource_id": self._safe_attr(el, "resource-id"),
            "accessibility_id": self._safe_attr(el, "content-desc"),
            "text": el.text or "",
            "class": self._safe_attr(el, "class"),
            "clickable": self._safe_attr(el, "clickable") == "true"
        }

    @keyword("Get Visible Elements On Screen")
    def get_visible_elements_on_screen(self, filter_type: str = "all", id_mode: str = "auto", debug: bool = False):
        """
        Returns the list of visible UI elements currently rendered on the screen.

        This keyword is useful for visual validation or exploratory checks during mobile automation tests.
        It applies optional filters by element type (e.g., clickable, text, button, input) and allows selecting
        which identifier should be used (`resource-id`, `accessibility_id`, or automatic fallback).

        Args:
            filter_type (str, optional):
                The type of elements to include in the result. Options are:
                - "all": no filtering, return every visible element (default)
                - "clickable": only elements with clickable="true"
                - "text": only elements with a non-empty text value
                - "button": only elements whose class contains "Button"
                - "input": only elements whose class contains "EditText"
            id_mode (str, optional):
                The identifier selection strategy. Options are:
                - "auto" (default): prefer resource-id; if empty, fallback to content-desc (accessibility_id)
                - "resource_id": only return resource-id values
                - "accessibility_id": only return content-desc values
            debug (bool, optional):
                Whether to return full element details as dictionaries (for debugging/inspection).
                If False (default), returns only a list of identifiers (strings).
                If True, returns a list of dictionaries with the following keys:
                - "identifier": { "value": <str>, "kind": "resource_id"|"accessibility_id" }
                - "resource_id": element resource-id (may be empty)
                - "accessibility_id": element content-desc (may be empty)
                - "text": element visible text (may be empty)
                - "class": element class name
                - "clickable": boolean flag if element is clickable

        Returns:
            list:
                - When debug=False: a list of identifier strings (resource-id or accessibility_id).
                - When debug=True: a list of dictionaries with extended element information.

        Examples:
            | *** Test Cases ***                                                               |
            | Return all visible elements                                                      |
            |     @{els}=    Get Visible Elements On Screen                                    |
            |     Should Not Be Empty    ${els}                                                |
            |                                                                                  |
            | Return only clickable elements in debug mode                                     |
            |     @{els}=    Get Visible Elements On Screen    clickable    auto    debug=True |
            |     FOR    ${el}    IN    @{els}                                                 |
            |         Should Be True    ${el['clickable']}                                     |
            |     END                                                                          |

        Raises:
            AssertionError:
                - If an invalid value is passed to `filter_type` or `id_mode`.
            WebDriverException:
                - If fetching elements from the driver fails.

        Notes:
            - On Android, "accessibility_id" is an alias for the "content-desc" attribute.
            - In auto mode, elements without either resource-id or content-desc are excluded.
            - Duplicates are automatically removed based on (kind, value) pairs.
        """

        valid_filters = {'all', 'clickable', 'text', 'button', 'input'}
        # Normalize input to lowercase (lower()) and strip (strip()) spaces to avoid typos
        filter_type = (filter_type or "").strip().lower()
        if filter_type not in valid_filters:
            self._builtin.fail(f"Invalid filter '{filter_type}'. Options: {valid_filters}")

        valid_ids = {"auto", "resource_id", "accessibility_id"}
        # Normalize input to lowercase (lower()) and strip (strip()) spaces to avoid typos
        id_mode = (id_mode or "").strip().lower()
        if id_mode not in valid_ids:
            self._builtin.fail(f"Invalid id_mode '{id_mode}'. Options: {valid_ids}")

        driver = self._get_appium_driver()
        try:
            elements = self._find_all_elements(driver)
        except WebDriverException as e:
            self._builtin.log(f"Error fetching elements: {e}", level="ERROR")
            return []
        
        self._builtin.log(f"Found {len(elements)} elements before filtering", level="DEBUG")

        visible_elements = []
        seen = set()
        for el in elements:
            try:
                # First filter: real visibility
                try:
                    if not el.is_displayed():
                        continue
                except (StaleElementReferenceException, NoSuchElementException):
                    continue

                # Second filter: match element type
                if not self._passes_filter(el, filter_type):
                    continue 

                # Third filter: must yield a chosen identifier
                chosen_value, chosen_kind = self._choose_identifier(el, id_mode)
                if not chosen_value:
                    continue

                # Deduplicate by (kind, value) tuple to avoid rare collisions
                # (e.g., when resource-id and content-desc happen to be identical)
                key = (chosen_kind, chosen_value)
                if key in seen:
                    continue
                seen.add(key)

                # Define return format
                if debug:
                    # debug mode
                    visible_elements.append(self._build_debug_dict(el, chosen_value, chosen_kind))
                else:
                    # normal mode
                    visible_elements.append(chosen_value)

            # Ignore elements that are no longer valid
            except (StaleElementReferenceException, NoSuchElementException) as ex:
            # NoSuchElementException: the element does not exist (e.g., invalid selector or not rendered yet)
            # StaleElementReferenceException: the element is no longer attached to the DOM (e.g., dynamic re-render)
                self._builtin.log(f"Ignored element due to {type(ex).__name__}: {ex}", level="DEBUG")
                continue

        # Log total elements that passed all filters
        count = len(visible_elements)
        self._builtin.log (f"Total visible elements after filtering: {count}", level="INFO")

        if debug:
            debug_output = json.dumps(visible_elements, indent=2)
            self._builtin.log("DEBUG JSON:\n" + debug_output, level="INFO")

        else:
            self._builtin.log("Visible elements:\n" + json.dumps(visible_elements, indent=2), level="INFO")
        return visible_elements