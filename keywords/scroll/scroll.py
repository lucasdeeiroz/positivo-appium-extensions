# Importa o AppiumBy — enumeração que permite localizar elementos por diferentes estratégias (xpath, id, etc.)
from appium.webdriver.common.appiumby import AppiumBy

# Importa o decorador @keyword, que permite transformar a função Python em uma keyword do Robot Framework
from robot.api.deco import keyword

# Importa a biblioteca interna BuiltIn do Robot Framework — usada para logar mensagens e acessar outras bibliotecas
from robot.libraries.BuiltIn import BuiltIn

# Cria a classe que define sua biblioteca customizada de scroll
class scroll:
    # Define o escopo como GLOBAL — ou seja, a mesma instância será usada em todos os testes
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Instancia o BuiltIn para usar funções do Robot, como log()
        self._builtin = BuiltIn()

    @property
    def driver(self):
        # Retorna o driver Appium atualmente em uso, via AppiumLibrary
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    # Define a keyword "Scroll Element", agora com argumentos nomeados via **kwargs
    @keyword("Scroll Inside")
    def scroll_element(self, **kwargs):
        """
        Executa um gesto de swipe (arrasto) dentro de um elemento localizado por qualquer estratégia.

        Os parâmetros devem ser passados como argumentos nomeados no .robot:
        - locator_type: tipo de localizador (ex: 'xpath', 'id', 'accessibility_id', etc.). Padrão: 'xpath'
        - locator_value: valor do seletor (XPath, ID, etc.) — obrigatório!
        - direction: direção do swipe — 'up', 'down', 'left' ou 'right'. Padrão: 'down'
        - percent: proporção do gesto (entre 0.01 e 1.0). Padrão: 0.75
        - speed: velocidade do swipe em pixels por segundo. Padrão: 800
        """

        # Lê os argumentos nomeados com valores padrão
        locator_type = kwargs.get("locator_type", "xpath")
        locator_value = kwargs.get("locator_value", None)
        direction = kwargs.get("direction", "down")
        percent = float(kwargs.get("percent", 0.75))
        speed = int(kwargs.get("speed", 800))

        # Valida se os argumentos estão corretos
        if not locator_value:
            raise ValueError("O parâmetro 'locator_value' é obrigatório.")
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("O parâmetro 'direction' deve ser: 'up', 'down', 'left' ou 'right'.")
        if not (0.01 <= percent <= 1.0):
            raise ValueError("O parâmetro 'percent' deve estar entre 0.01 e 1.0.")
        if speed <= 0:
            raise ValueError("O parâmetro 'speed' deve ser um número positivo.")

        # Mapeia o tipo do localizador para o AppiumBy
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

        # Converte o locator_type em uma estratégia válida
        strategy = locator_strategies.get(locator_type.lower())
        if not strategy:
            raise ValueError(f"Tipo de localizador inválido: '{locator_type}'")

        try:
            # Acessa o driver do Appium
            driver = self.driver

            # Localiza o elemento na tela usando o tipo e valor informados
            element = driver.find_element(strategy, locator_value)

            # Executa o gesto de swipe dentro do elemento localizado
            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,
                "direction": direction,
                "percent": percent,
                "speed": speed
            })

            # Registra no log do Robot Framework que a operação foi bem-sucedida
            self._builtin.log(
                f"[SUCESSO] Scroll no elemento localizado por {locator_type}='{locator_value}' com direction='{direction}', percent={percent}, speed={speed}.",
                "INFO"
            )

        except Exception as e:
            # Se ocorrer algum erro, registra no log como erro
            self._builtin.log(
                f"[ERRO] Falha ao executar scroll: {str(e)}",
                "ERROR"
            )
            # E interrompe a execução do teste
            raise
