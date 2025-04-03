from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton

@keyword("Perform Pinch Gesture")
def perform_pinch_gesture(locator, scale=0.5, duration=50):
    """
    Realiza o gesto de pinça (pinch) em um aplicativo Android.
    """

    # Obtém o driver atual do AppiumLibrary
    appium_lib = BuiltIn().get_library_instance("AppiumLibrary")
    driver = appium_lib._current_application()

    # Localiza o elemento usando o locator e obtém suas coordenadas
    element = appium_lib._element_find(locator, True, True)
    location = element.location
    y = location['y']
    x = location['x']
    width = element.size['width']
    height = element.size['height']
    center_x = x + width / 2
    center_y = y + height / 2

    # Cria uma instância da classe ActionChains
    actions = ActionChains(driver)

    # Define dois ponteiros de toque (dedos)
    finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1') 
    finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

    # Configura o gesto de Zoom In (pinça)
    finger1.create_pointer_move(x=center_x - center_x * scale, y=center_y)
    finger2.create_pointer_move(x=center_x + center_x * scale, y=center_y)
    
    finger1.create_pointer_down(button=MouseButton.LEFT)
    finger2.create_pointer_down(button=MouseButton.LEFT)
    
    finger1.create_pause(0.5)
    finger2.create_pause(0.5)
    
    finger1.create_pointer_move(x=center_x - 100, y=center_y, duration=duration)
    finger2.create_pointer_move(x=center_x + 100, y=center_y, duration=duration)

    finger1.create_pointer_up(button=MouseButton.LEFT)
    finger2.create_pointer_up(button=MouseButton.LEFT)

    # Executa as ações
    actions.perform()