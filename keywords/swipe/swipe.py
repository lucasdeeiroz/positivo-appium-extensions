from appium.webdriver.common.appiumby import AppiumBy
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class swipe:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Swipe Element")
    def swipe_element(self, **kwargs):
        """
        Realiza um swipe diretamente sobre um elemento, útil para sliders, carrosséis, notas etc.

        Argumentos:
        - Um locator no estilo chave=valor (xpath=..., id=..., etc.)
        - direction (str): 'up', 'down', 'left', 'right'. Default: 'left'
        - percent (float): tamanho relativo do swipe. Default: 0.5
        - speed (int): velocidade do swipe. Default: 800

        Exemplo:
            Swipe Element    xpath=//android.widget.ImageView[1]    direction=right    percent=0.6
        """

        locator_strategies = {
            "id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "class_name": AppiumBy.CLASS_NAME,
            "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
            "ios_predicate": AppiumBy.IOS_PREDICATE,
            "ios_class_chain": AppiumBy.IOS_CLASS_CHAIN,
            "name": AppiumBy.NAME
        }

        # Identifica a estratégia e valor do localizador
        locator_type = None
        locator_value = None
        for key in kwargs:
            if key.lower() in locator_strategies:
                locator_type = key.lower()
                locator_value = kwargs[key]
                break

        if not locator_type or not locator_value:
            raise ValueError("Você deve passar um localizador válido (ex: xpath=..., id=...).")

        # Parâmetros adicionais
        direction = kwargs.get("direction", "left")
        percent = float(kwargs.get("percent", 0.5))
        speed = int(kwargs.get("speed", 800))

        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("Direção deve ser: 'up', 'down', 'left', ou 'right'.")
        if not (0.01 <= percent <= 1.0):
            raise ValueError("Percent precisa estar entre 0.01 e 1.0")
        if speed <= 0:
            raise ValueError("Speed precisa ser um número positivo")

        try:
            driver = self.driver
            strategy = locator_strategies[locator_type]
            element = driver.find_element(strategy, locator_value)

            # Swipe real, sem inversão de direção como no scroll
            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,
                "direction": direction,
                "percent": percent,
                "speed": speed
            })

            self._builtin.log(
                f"[SUCCESS] Swipe executado em {locator_type}='{locator_value}' na direção='{direction}', percent={percent}, speed={speed}.",
                "INFO"
            )

        except Exception as e:
            self._builtin.log(f"[ERROR] Falha no swipe: {str(e)}", "ERROR")
            raise
