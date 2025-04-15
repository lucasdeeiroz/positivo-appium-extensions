from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
import time

class AppiumZoomExtensions4:
    """Extensão com repetição de zoom até atingir scale desejado"""
    
    def __init__(self):
        self._builtin = BuiltIn()
        self.BASE_OFFSET = 50
        self.MARGIN = 0.3  # Margem de 30%
        self.MAX_ATTEMPTS = 5  # Máximo de tentativas
        self.RETRY_DELAY = 0.5  # Espera entre tentativas
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('Force Zoom On Element')
    def ensure_zoom_on_element(self, locator, scale=1.5, duration_ms=100, pause_s=0.5):
        """Repete o zoom até atingir o scale desejado (com margem de 30%)"""
        if scale <= 1.0:
            raise ValueError("Scale deve ser > 1.0")
        
        attempt = 1
        min_acceptable = scale * (1 - self.MARGIN)
        
        while attempt <= self.MAX_ATTEMPTS:
            # Captura estado inicial
            initial_state = self._capture_zoom_state(locator)
            
            # Executa o zoom
            self._perform_zoom(locator, scale, duration_ms, pause_s)
            
            # Captura estado final
            final_state = self._capture_zoom_state(locator)
            time.sleep(self.RETRY_DELAY)
            
            # Calcula scale efetivo
            effective_scale = self._calculate_effective_scale(initial_state, final_state)
            
            # Verifica se atingiu o objetivo
            if effective_scale >= min_acceptable:
                self._builtin.log(f"Zoom {effective_scale:.2f}x alcançado na tentativa {attempt}")
                return True
                
            self._builtin.log(f"Tentativa {attempt}: Zoom {effective_scale:.2f}x (alvo: {scale}x)")
            attempt += 1
        
        raise AssertionError(f"Falha ao atingir zoom {scale}x após {self.MAX_ATTEMPTS} tentativas. Último scale: {effective_scale:.2f}x")

    def _capture_zoom_state(self, locator):
        """Captura estado atual do zoom"""
        element = self._find_element(locator)
        return {
            'attributes': {
                'size': element.size,
                'location': element.location,
                'zoom_level': self._get_zoom_level(element)  # Implemente conforme seu app
            },
            'timestamp': time.time()
        }
    
    def _get_zoom_level(self, element):
        """Extrai o nível de zoom do elemento (implementação específica por app)"""
        # Exemplo para Google Maps:
        try:
            zoom_text = element.find_element(AppiumBy.ID, 'zoom_level_indicator').text
            return float(zoom_text.replace('x', ''))
        except:
            return 1.0  # Fallback
    
    def _calculate_effective_scale(self, initial_state, final_state):
        """Calcula o scale efetivo alcançado"""
        # Prioriza o zoom_level se disponível
        if initial_state['attributes']['zoom_level'] > 1.0:
            return final_state['attributes']['zoom_level'] / initial_state['attributes']['zoom_level']
        
        # Fallback: cálculo baseado em tamanho do elemento
        initial_area = initial_state['attributes']['size']['width'] * initial_state['attributes']['size']['height']
        final_area = final_state['attributes']['size']['width'] * final_state['attributes']['size']['height']
        return (final_area / initial_area) ** 0.5  # Raiz quadrada para escala linear
    
    def _perform_zoom(self, locator, scale, duration_ms, pause_s):
        """Executa o gesto de zoom"""
        element = self._find_element(locator)
        location = element.location
        size = element.size
        
        center_x = location['x'] + (size['width'] / 2)
        center_y = location['y'] + (size['height'] / 2)
        final_offset = self.BASE_OFFSET * scale
        
        actions = ActionChains(self._driver)
        actions.w3c_actions.devices = []
        
        finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
        finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')
        
        # Configura movimentos
        finger1.create_pointer_move(x=center_x - self.BASE_OFFSET, y=center_y)
        finger1.create_pointer_down(button=MouseButton.LEFT)
        finger1.create_pause(pause_s)
        finger1.create_pointer_move(x=center_x - final_offset, y=center_y, duration=duration_ms)
        finger1.create_pointer_up(button=MouseButton.LEFT)
        
        finger2.create_pointer_move(x=center_x + self.BASE_OFFSET, y=center_y)
        finger2.create_pointer_down(button=MouseButton.LEFT)
        finger2.create_pause(pause_s)
        finger2.create_pointer_move(x=center_x + final_offset, y=center_y, duration=duration_ms)
        finger2.create_pointer_up(button=MouseButton.LEFT)
        
        actions.perform()
    
    def _find_element(self, locator):
        """Localiza elemento com tratamento de erros"""
        driver = self._driver
        if locator.startswith('//'):
            return driver.find_element(AppiumBy.XPATH, locator)
        
        parts = locator.split('=', 1)
        if len(parts) != 2:
            raise ValueError("Formato de locator inválido")
        
        strategy, value = parts
        strategies = {
            'id': AppiumBy.ID,
            'xpath': AppiumBy.XPATH,
            'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
            'class': AppiumBy.CLASS_NAME
        }
        
        return driver.find_element(strategies[strategy], value)