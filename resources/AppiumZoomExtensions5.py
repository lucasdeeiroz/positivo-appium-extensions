from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import KEY
from appium.webdriver.common.appiumby import AppiumBy

def pinch_and_zoom(driver):
    # Obter tamanho da tela
    size = driver.get_window_size()
    width = size['width']
    height = size['height']

    center_x = width // 2
    center_y = height // 2

    finger1 = PointerInput(PointerInput.TOUCH, "finger1")
    finger2 = PointerInput(PointerInput.TOUCH, "finger2")

    seq1 = [
        finger1.create_pointer_move(duration=0, x=center_x, y=center_y),
        finger1.create_pointer_down(),
        finger1.create_pause(0.1),
        finger1.create_pointer_move(duration=600, x=width // 3, y=height // 3),
        finger1.create_pointer_up(button=0)
    ]

    seq2 = [
        finger2.create_pointer_move(duration=0, x=center_x, y=center_y),
        finger2.create_pointer_down(),
        finger2.create_pause(0.1),
        finger2.create_pointer_move(duration=600, x=width * 3 // 4, y=height * 3 // 4),
        finger2.create_pointer_up(button=0)
    ]

    actions = ActionChains(driver)
    actions.w3c_actions.devices = [finger1, finger2]
    actions.w3c_actions.add_action_sequence(seq1)
    actions.w3c_actions.add_action_sequence(seq2)
    actions.perform()
