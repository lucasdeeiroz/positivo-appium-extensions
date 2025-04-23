from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy

class AppiumZoomExtensions2:
    """Extensão da AppiumLibrary com funcionalidade de Zoom (apenas aumento)"""
    
    def __init__(self):
        self._builtin = BuiltIn()
        self.BASE_OFFSET = 50  # Distância base para cálculo do zoom
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('Zoom On Element')
    def zoom_on_element(self, locator, scale=2.5, duration_ms=100, pause_s=0.5):
        """Realiza zoom IN no centro de um elemento específico usando fator de escala
        
        Args:
            locator: Estrategia e valor do locator (ex: "id=zoom_element")
            scale: Fator de zoom (deve ser > 1.0, ex: 1.5 = 150%)
            duration_ms: Duração do gesto (milissegundos)
            pause_s: Pausa após pressionar (segundos)
        """
        # Validação do scale
        if scale <= 1.0:
            raise ValueError("Scale must be greater than 1.0")
        
        driver = self._driver
        
        # Parse do locator
        if locator.startswith('//'):
            element = driver.find_element(AppiumBy.XPATH, locator)
        else:
            locator_parts = locator.split('=', 1)
            if len(locator_parts) != 2:
                raise ValueError("Must be on format strategy=locator")
            
            strategy, value = locator_parts
            strategy_mapping = {
                'id': AppiumBy.ID,
                'xpath': AppiumBy.XPATH,
                'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
                'class': AppiumBy.CLASS_NAME
            }
            
            if strategy not in strategy_mapping:
                raise ValueError(f"Estratégia '{strategy}' não suportada")
            
            element = driver.find_element(strategy_mapping[strategy], value)
        
        # Obtém dimensões do elemento
        location = element.location
        size = element.size
        
        # Calcula o centro do elemento
        center_x = location['x'] + (size['width'] / 2)
        center_y = location['y'] + (size['height'] / 2)
        
        # Calcula offsets baseado no scale
        initial_offset = self.BASE_OFFSET
        final_offset = self.BASE_OFFSET * scale  # Scale aplicado aqui
        
        # Cria e executa o gesto de zoom
        actions = ActionChains(driver)
        actions.w3c_actions.devices = []
        
        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')
        
        # Configura os movimentos dos dedos (afastamento)
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