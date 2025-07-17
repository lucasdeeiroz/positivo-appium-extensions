from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import time

class ThemeChanger:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def appium(self):
        return self._builtin.get_library_instance("AppiumLibrary")

    @property
    def driver(self):
        return self.appium._current_application()

    def _is_element_visible(self, locator):
        try:
            element = self.appium._element_find(locator, True, True)
            return element.is_displayed()
        except:
            return False

    def _click_element(self, locator, timeout=10):
        try:
            element = self.appium._element_find(locator, True, True)
            if element and element.is_displayed():
                element.click()
                time.sleep(1)
                return True
            return False
        except Exception as e:
            self._builtin.log(f"Erro ao clicar no elemento {locator}: {str(e)}", "WARN")
            return False

    def _swipe_to_find_element(self, locator, max_swipes=5):
        for _ in range(max_swipes):
            if self._is_element_visible(locator):
                return True
            self.driver.swipe(500, 1500, 500, 800, 500)  # Swipe simples
            time.sleep(0.5)
        return False
        
    def _open_settings_app(self):
  
        try:
            self._builtin.run_keyword("Close Application")

        # Abre nova sessão com app de configurações
            self._builtin.run_keyword(
            "Open Application",
            "http://localhost:4723",
            "platformName=Android",
            "deviceName=XiaomiDevice",
            "udid=a83af8e7",
            "automationName=UiAutomator2",
            "appPackage=com.android.settings",
            "appActivity=com.android.settings.Settings",
            "noReset=true"
            )
            time.sleep(2)
            self._builtin.log("App de configurações aberto com nova sessão", "INFO")
            return True
        except Exception as e:
            self._builtin.log(f"Erro ao abrir app de configurações: {str(e)}", "ERROR")
        return False


    def _navigate_to_display_settings(self):
        locators = [
            "xpath=//android.widget.TextView[@text='Configurações']",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]/android.widget.RelativeLayout/android.widget.TextView"
        ]
        for locator in locators:
            if self._swipe_to_find_element(locator):
                return self._click_element(locator)
        return False

    def _find_and_click_theme_option(self):
        locators = [
            "xpath=//android.widget.TextView[contains(@text,'Tela e brilho')]",
            "xpath=//android.widget.TextView[contains(@text,'Dark')]"
        ]
        for locator in locators:
            if self._swipe_to_find_element(locator):
                return self._click_element(locator)
        return False

    def _enable_theme(self, mode="dark"):
        control_locators = {
            "dark": [
                "com.android.settings:id/dark_mode_view",
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.ImageView"
            ],
            "light": [
                "com.android.settings:id/light_mode_view",
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.ImageView"
            ]
        }
        for locator in control_locators[mode]:
            if self._is_element_visible(locator):
                return self._click_element(locator)
        return False

    @keyword("Change To Dark Theme")
    def change_to_dark_theme(self, timeout=30):
        start_time = time.time()
        try:
            if not self._open_settings_app():
                raise RuntimeError("Não foi possível abrir Configurações")

            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout abrindo Configurações")

            if not self._navigate_to_display_settings():
                raise RuntimeError("Não encontrou configurações de Tela")

            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout em configurações de Tela")

            if not self._find_and_click_theme_option():
                raise RuntimeError("Não encontrou opção de Tema")

            if not self._enable_theme(mode="dark"):
                raise RuntimeError("Não conseguiu habilitar Tema Escuro")

            self.driver.press_keycode(3)  # HOME
        except Exception as e:
            self._builtin.log(f"Erro ao mudar tema: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao mudar para tema escuro: {str(e)}")

    @keyword("Change To Light Theme")
    def change_to_light_theme(self, timeout=30):
        start_time = time.time()
        try:
            if not self._open_settings_app():
                raise RuntimeError("Não foi possível abrir Configurações")

            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout abrindo Configurações")

            if not self._navigate_to_display_settings():
                raise RuntimeError("Não encontrou configurações de Tela")

            if not self._find_and_click_theme_option():
                raise RuntimeError("Não encontrou opção de Tema")

            if not self._enable_theme(mode="light"):
                raise RuntimeError("Não conseguiu habilitar Tema Claro")

            self.driver.press_keycode(3)
        except Exception as e:
            self._builtin.log(f"Erro ao mudar tema: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao mudar para tema claro: {str(e)}")
