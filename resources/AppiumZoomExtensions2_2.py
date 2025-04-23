from robot.api.deco import keyword
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn

class AppiumZoomExtensions2_2:
    """Extensão da AppiumLibrary com funcionalidade de Zoom baseado no centro de um elemento"""

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('Zoom On Element by Coordinates')
    def zoom_on_element_center(self, locator, initial_offset=50, final_offset=800, duration_ms=500, pause_s=0.3):
        """Zoom usando o centro do elemento como ponto de origem (sem rect direto na ação)"""
        driver = self._driver

        # Detecta automaticamente o tipo de localizador
        if locator.startswith("//"):
            element = driver.find_element(By.XPATH, locator)
        else:
            element = driver.find_element(By.ID, locator)

        # Calcula o centro do elemento com base nas dimensões
        rect = element.rect
        center_x = rect['x'] + rect['width'] / 2
        center_y = rect['y'] + rect['height'] / 2

        actions = ActionChains(driver)
        actions.w3c_actions.devices = []

        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

        # Zoom a partir do centro do elemento
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
