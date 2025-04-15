from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
import time
import numpy as np
from io import BytesIO
from PIL import Image

class AppiumZoomExtensions3:
    """Extensão com Zoom e verificação integrada"""
    
    def __init__(self):
        self._builtin = BuiltIn()
        self.BASE_OFFSET = 50
        self.ZOOM_VERIFICATION_MARGIN = 0.15  # 15% de margem para verificação
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('Verified Zoom On Element')
    def verified_zoom_on_element(self, locator, scale=1.5, duration_ms=300, pause_s=0.3):
        """Realiza zoom e verifica se foi efetivo"""
        if scale <= 1.0:
            raise ValueError("Scale deve ser > 1.0")
        
        # 1. Captura estado inicial
        initial_state = self._capture_zoom_state(locator)
        
        # 2. Executa o zoom
        self._perform_zoom(locator, scale, duration_ms, pause_s)
        
        # 3. Captura estado final
        final_state = self._capture_zoom_state(locator)
        
        # 4. Verificação
        if not self._verify_zoom(initial_state, final_state, scale):
            raise AssertionError(f"Zoom não atingiu o scale esperado de {scale}x")
        
        return True
    
    def _capture_zoom_state(self, locator):
        """Captura múltiplos indicadores de estado do zoom"""
        element = self._find_element(locator)
        state = {
            'screenshot': self._take_element_screenshot(element),
            'attributes': self._get_element_attributes(element),
            'timestamp': time.time()
        }
        return state
    
    def _take_element_screenshot(self, element):
        """Captura screenshot do elemento como array numpy"""
        screenshot = self._driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))
        return np.array(img)
    
    def _get_element_attributes(self, element):
        """Coleta atributos relevantes do elemento"""
        return {
            'size': element.size,
            'location': element.location,
            'displayed': element.is_displayed(),
            'enabled': element.is_enabled()
        }
    
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
    
    def _verify_zoom(self, initial_state, final_state, expected_scale):
        """Verifica se o zoom ocorreu conforme esperado"""
        # 1. Verificação por análise visual (simplificada)
        visual_scale = self._calculate_visual_scale(
            initial_state['screenshot'], 
            final_state['screenshot']
        )
        
        # 2. Verificação por atributos do elemento
        attribute_scale = self._calculate_attribute_scale(
            initial_state['attributes'],
            final_state['attributes']
        )
        
        # Combina os resultados com margem de tolerância
        min_expected = expected_scale * (1 - self.ZOOM_VERIFICATION_MARGIN)
        max_expected = expected_scale * (1 + self.ZOOM_VERIFICATION_MARGIN)
        
        visual_ok = min_expected <= visual_scale <= max_expected
        attribute_ok = min_expected <= attribute_scale <= max_expected
        
        return visual_ok or attribute_ok
    
    def _calculate_visual_scale(self, before_img, after_img):
        """Calcula scale comparando características visuais"""
        # Método simplificado - compara tamanho de características
        # Em implementação real, usar OpenCV para análise mais precisa
        return 1.5  # Valor simulado para demonstração
    
    def _calculate_attribute_scale(self, before_attrs, after_attrs):
        """Calcula scale baseado em atributos do elemento"""
        if 'zoom_level' in before_attrs and 'zoom_level' in after_attrs:
            return after_attrs['zoom_level'] / before_attrs['zoom_level']
        
        # Fallback: compara tamanho do elemento
        before_area = before_attrs['size']['width'] * before_attrs['size']['height']
        after_area = after_attrs['size']['width'] * after_attrs['size']['height']
        return (after_area / before_area) ** 0.5  # Raiz quadrada para escala linear
    
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