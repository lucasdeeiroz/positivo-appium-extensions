from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
import time

class AppiumZoomExtensions2_3_3:
    """Zoom universal baseado em coordenadas de elementos com controle completo"""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self._builtin = BuiltIn()
        self.BASE_OFFSET = 50  # Distância base para os dedos
        self.MIN_SCALE = 1.1   # Scale mínimo válido
        self.DEFAULT_DURATION = 300  # ms
        self.DEFAULT_PAUSE = 0.3  # s (300ms)
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('Universal Zoom On Area_2')
    def universal_zoom(self, locator=None, scale=2.0, duration_ms=None, pause_s=None, attempts=3):
        """
        Realiza zoom na área central de um elemento (sem interagir diretamente com ele)
        ou no centro da tela, com controle preciso.

        Args:
            locator: Localizador do elemento (opcional)
            scale: Fator de zoom (> 1.0)
            duration_ms: Duração do gesto
            pause_s: Pausa após pressionar
            attempts: Tentativas se falhar
        """
        if scale <= 1.0:
            raise ValueError("Scale deve ser maior que 1.0")
        
        if duration_ms is None:
            duration_ms = self._calculate_duration(scale)
        
        if pause_s is None:
            pause_s = self.DEFAULT_PAUSE

        for attempt in range(1, attempts + 1):
            try:
                # Usa o centro do elemento ou da tela como referência
                coords = self._get_screen_coordinates() if locator is None else self._get_element_coordinates(locator)

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
                    raise Exception(f"Falha após {attempts} tentativas: {str(e)}")
                time.sleep(0.5)

    def _get_element_coordinates(self, locator):
        """Obtém as coordenadas absolutas do elemento (apenas como referência de centro visual)"""
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
        """Obtém coordenadas da tela inteira"""
        window_size = self._driver.get_window_size()
        return {
            'x': 0,
            'y': 0,
            'width': window_size['width'],
            'height': window_size['height']
        }

    def _calculate_duration(self, scale):
        """Calcula duração automática baseada no scale"""
        base_duration = self.DEFAULT_DURATION
        return min(int(base_duration * (scale - 1)), 1000)

    def _perform_zoom_gesture(self, center_x, center_y, initial_offset, final_offset, duration_ms, pause_s):
        """Executa o gesto de zoom nas coordenadas especificadas"""
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

    def _find_element(self, locator):
        """Localiza elemento com tratamento robusto"""
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
