from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy

class AppiumZoomExtensions7:
    """Extensão da AppiumLibrary com funcionalidade de Zoom In"""
    
    def __init__(self):
        self._builtin = BuiltIn()
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('Zoom in_2')
    def custom_zoom(self, initial_offset=50, final_offset=800, duration_ms=500, pause_s=0.3, locator=None):
        """Zoom in the middle of the screen or on a specific element using locator strategies"""
        driver = self._driver

        if locator:
            # Estratégia de localização
            if locator.startswith('//'):
                element = driver.find_element(AppiumBy.XPATH, locator)
            else:
                try:
                    strategy, value = locator.split('=', 1)
                except ValueError:
                    raise ValueError(f"Locator '{locator}' deve estar no formato 'estratégia=valor' ou começar com '//'.")
                
                strategy_mapping = {
                    'id': AppiumBy.ID,
                    'xpath': AppiumBy.XPATH,
                    'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
                    'class': AppiumBy.CLASS_NAME
                }

                if strategy not in strategy_mapping:
                    raise ValueError(f"Estratégia '{strategy}' não suportada. Use uma das: {list(strategy_mapping.keys())}")

                element = driver.find_element(strategy_mapping[strategy], value)

            location = element.location
            size = element.size
            center_x = location['x'] + size['width'] / 2
            center_y = location['y'] + size['height'] / 2
        else:
            window_size = driver.get_window_size()
            center_x = window_size['width'] / 2
            center_y = window_size['height'] / 2

        actions = ActionChains(driver)
        actions.w3c_actions.devices = []

        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

        finger1.create_pointer_move(x=center_x-initial_offset, y=center_y)
        finger1.create_pointer_down(button=MouseButton.LEFT)
        finger1.create_pause(pause_s)
        finger1.create_pointer_move(x=center_x-final_offset, y=center_y, duration=duration_ms)
        finger1.create_pointer_up(button=MouseButton.LEFT)

        finger2.create_pointer_move(x=center_x+initial_offset, y=center_y)
        finger2.create_pointer_down(button=MouseButton.LEFT)
        finger2.create_pause(pause_s)
        finger2.create_pointer_move(x=center_x+final_offset, y=center_y, duration=duration_ms)
        finger2.create_pointer_up(button=MouseButton.LEFT)

        actions.perform()
