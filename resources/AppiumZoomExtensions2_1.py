from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy

class AppiumZoomExtensions2_1:
    """Extensão da AppiumLibrary com funcionalidade de Zoom (apenas aumento)"""
    
    def __init__(self):
        self._builtin = BuiltIn()
        self.BASE_OFFSET = 50  # Distância base para cálculo do zoom

    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('Zoom On Element Alternative')
    def zoom_on_element(self, locator, scale=2.5, duration_ms=100, pause_s=0.5):
        if scale <= 1.0:
            raise ValueError("Scale must be greater than 1.0")

        driver = self._driver

        # Estratégia de localização
        if locator.startswith('//'):
            element = driver.find_element(AppiumBy.XPATH, locator)
        else:
            strategy, value = locator.split('=', 1)
            strategy_mapping = {
                'id': AppiumBy.ID,
                'xpath': AppiumBy.XPATH,
                'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
                'class': AppiumBy.CLASS_NAME
            }
            if strategy not in strategy_mapping:
                raise ValueError(f"Estratégia '{strategy}' não suportada")
            element = driver.find_element(strategy_mapping[strategy], value)

        # Verifica se o elemento está visível e habilitado
        if not element.is_displayed() or not element.is_enabled():
            raise Exception("Elemento não está interativo")

        # Pega centro do elemento
        rect = element.rect
        center_x = rect['x'] + rect['width'] / 2
        center_y = rect['y'] + rect['height'] / 2

        initial_offset = self.BASE_OFFSET
        final_offset = self.BASE_OFFSET * scale

        actions = ActionChains(driver)
        actions.w3c_actions.devices = []

        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

        # Primeiro dedo
        finger1.create_pointer_move(duration=0, x=center_x - initial_offset, y=center_y - 30)
        finger1.create_pointer_down(button=0)
        finger1.create_pause(pause_s)
        finger1.create_pointer_move(duration=duration_ms, x=center_x - final_offset, y=center_y - 60)
        finger1.create_pointer_up(button=0)

        # Segundo dedo
        finger2.create_pointer_move(duration=0, x=center_x + initial_offset, y=center_y + 30)
        finger2.create_pointer_down(button=0)
        finger2.create_pause(pause_s)
        finger2.create_pointer_move(duration=duration_ms, x=center_x + final_offset, y=center_y + 60)
        finger2.create_pointer_up(button=0)

        actions.perform()
