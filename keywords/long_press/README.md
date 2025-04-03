# Keyword Long Press

Implementação da keyword para ação de Long Press.

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton

class AppiumLongPressExtensions:
"""Extensão da AppiumLibrary com funcionalidade de Long Press"""

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword('LongP')
    def long_press(self, locator, duration=1000):
        """Realiza um clique longo no elemento especificado

        Args:
            locator: Estrategia e valor do locator (ex: "id=button1")
            duration: Tempo do pressionamento em milissegundos (padrão: 1000ms)
        """
        driver = self._driver

        locator_parts = locator.split('=', 1)
        if len(locator_parts) != 2:
            raise ValueError("Locator deve estar no formato 'estrategia=valor'")

        strategy, value = locator_parts

        # Encontra o elemento usando AppiumBy
        element = driver.find_element(strategy, value)

        # Implementação alternativa usando ActionChains
        actions = ActionChains(driver)
        actions.click_and_hold(element).pause(duration/1000).release().perform()
