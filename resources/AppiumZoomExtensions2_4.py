from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
import time
import re

class AppiumZoomExtensions2_4:
    """Zoom universal baseado em coordenadas de elementos, bounds ou tela inteira"""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self._builtin = BuiltIn()
        self.BASE_OFFSET = 50
        self.MIN_SCALE = 1.1
        self.DEFAULT_DURATION = 50
        self.DEFAULT_PAUSE = 0.3
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('Universal Zoom On Area with Bounds')
    def universal_zoom(self, locator=None, bounds=None, scale=2.0, duration_ms=None, pause_s=None, attempts=3):
        if scale <= 1.0:
            raise ValueError("Scale deve ser maior que 1.0")
        if duration_ms is None:
            duration_ms = self._calculate_duration(scale)
        if pause_s is None:
            pause_s = self.DEFAULT_PAUSE

        for attempt in range(1, attempts + 1):
            try:
                if bounds:
                    coords = self._parse_bounds(bounds)
                elif locator:
                    coords = self._get_element_coordinates(locator)
                else:
                    coords = self._get_screen_coordinates()
                
                center_x = coords['x'] + (coords['width'] / 2)
                center_y = coords['y'] + (coords['height'] / 2)
                final_offset = self.BASE_OFFSET * scale

                self._perform_zoom_gesture(
                    center_x, center_y,
                    self.BASE_OFFSET, final_offset,
                    duration_ms, pause_s
                )

                return True

            except Exception as e:
                if attempt == attempts:
                    # Fallback para zoom no centro da tela
                    self._fallback_zoom_on_screen(scale, duration_ms, pause_s)
                    return False
                time.sleep(0.5)

    def _parse_bounds(self, bounds_str):
        """Converte '[x1,y1][x2,y2]' em dicionário com x, y, width, height"""
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds_str)
        if not match:
            raise ValueError(f"Formato de bounds inválido: {bounds_str}")
        
        x1, y1, x2, y2 = map(int, match.groups())
        return {
            'x': x1,
            'y': y1,
            'width': x2 - x1,
            'height': y2 - y1
        }

    def _get_element_coordinates(self, locator):
        element = self._find_element(locator)
        location = element.location
        size = element.size
        return {
            'x': location['x'],
            'y': location['y'],
            'width': size['width'],
            'height': size['height']
        }

    def _get_screen_coordinates(self):
        window_size = self._driver.get_window_size()
        return {
            'x': 0,
            'y': 0,
            'width': window_size['width'],
            'height': window_size['height']
        }

    def _calculate_duration(self, scale):
        base_duration = self.DEFAULT_DURATION
        return min(int(base_duration * (scale - 1)), 1000)

    def _perform_zoom_gesture(self, center_x, center_y, initial_offset, final_offset, duration_ms, pause_s):
        actions = ActionChains(self._driver)
        actions.w3c_actions.devices = []

        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

        finger1.create_pointer_move(x=center_x - initial_offset, y=center_y)
        finger1.create_pointer_down(button=MouseButton.LEFT)
        finger1.create_pause(pause_s)
        finger1.create_pointer_move(x=center_x - final_offset, y=center_y, duration=duration_ms)
        finger1.create_pointer_up(button=MouseButton.LEFT)

        finger2.create_pointer_move(x=center_x + initial_offset, y=center_y)
        finger2.create_pointer_down(button=MouseButton.LEFT)
        finger2.create_pause(pause_s)
        finger2.create_pointer_move(x=center_x + final_offset, y=center_y, duration=duration_ms)
        finger2.create_pointer_up(button=MouseButton.LEFT)

        actions.perform()

    def _fallback_zoom_on_screen(self, scale, duration_ms, pause_s):
        """Executa zoom no centro da tela como fallback"""
        driver = self._driver
        window_size = driver.get_window_size()
        center_x = window_size['width'] / 2
        center_y = window_size['height'] / 2
        initial_offset = self.BASE_OFFSET
        final_offset = self.BASE_OFFSET * scale

        self._perform_zoom_gesture(center_x, center_y, initial_offset, final_offset, duration_ms, pause_s)

    def _find_element(self, locator):
        driver = self._driver
        if locator.startswith('//'):
            return driver.find_element(AppiumBy.XPATH, locator)

        parts = locator.split('=', 1)
        if len(parts) != 2:
            raise ValueError("Formato de locator inválido. Use 'strategy=value' ou XPath")

        strategy, value = parts
        strategy_map = {
            'id': AppiumBy.ID,
            'xpath': AppiumBy.XPATH,
            'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
            'class': AppiumBy.CLASS_NAME
        }

        if strategy not in strategy_map:
            raise ValueError(f"Estratégia '{strategy}' não suportada")

        return driver.find_element(strategy_map[strategy], value)
