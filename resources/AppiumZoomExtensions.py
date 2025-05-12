from robot.api.deco import keyword
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from robot.libraries.BuiltIn import BuiltIn

class AppiumZoomExtensions:
    """Extensão da AppiumLibrary com funcionalidade de Zoom In"""
    
    def __init__(self):
        self._builtin = BuiltIn()
    
    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()
    
    @keyword('Zoom in Center')
    def custom_zoom(self, initial_offset=50, final_offset=800, duration_ms=500, pause_s=0.3):
        """Zoom in the middle of the screen"""
        driver = self._driver
        window_size = driver.get_window_size()
        center_x = window_size['width']/2
        center_y = window_size['height']/2
    
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