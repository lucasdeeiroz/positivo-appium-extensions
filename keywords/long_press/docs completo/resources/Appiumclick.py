from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class Appiumclick:

    def __init__(self):
        # Inicializa a classe e obtém uma instância da biblioteca BuiltIn do Robot Framework
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        # Retorna o driver atual do AppiumLibrary, que é usado para interagir com o dispositivo
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('ClickC')
    def click_at_coordinates(self, x, y):
        # Obtém o driver do Appium
        driver = self._driver

        # Certifica-se de que as coordenadas fornecidas são convertidas para inteiros
        x = int(x)
        y = int(y)

        # Realiza a ação de toque nas coordenadas fornecidas usando o comando clickGesture
        driver.execute_script("mobile: clickGesture", {"x": x, "y": y})

        # Registra a ação realizada no log do Robot Framework
        self._builtin.log(f"Clicked at coordinates ({x}, {y})", level='INFO')
