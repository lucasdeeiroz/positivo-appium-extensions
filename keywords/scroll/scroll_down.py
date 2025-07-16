# Importa o AppiumBy, usado para localizar elementos (por XPath, ID, etc.) via Appium
from appium.webdriver.common.appiumby import AppiumBy

# Importa o decorador @keyword, que transforma o método em uma keyword acessível no Robot Framework
from robot.api.deco import keyword

# Importa BuiltIn, permitindo interagir com funções do próprio Robot Framework (log, chamadas de outras keywords, etc.)
from robot.libraries.BuiltIn import BuiltIn

# Define a classe customizada da biblioteca
# Por convenção, usa-se o mesmo nome do arquivo .py como nome da classe (em snake_case ou PascalCase)
class scroll_down:
    # Define o escopo da biblioteca como GLOBAL — ou seja, uma única instância será usada por todos os testes
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Inicializa a instância da biblioteca BuiltIn
        self._builtin = BuiltIn()

    @property
    def driver(self):
        # Acessa a instância do driver Appium ativo (controlado pela AppiumLibrary do Robot Framework)
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    # Transforma o método em uma keyword utilizável nos testes .robot com o nome "Scroll Inside Element"
    @keyword("Scroll Inside Element")
    def scroll_inside_element(self, xpath, direction="down", percent=0.75, speed=800):
        """
        Executa um gesto de swipe (arrasto) dentro de um elemento específico da tela, simulando o toque do dedo.

        Parâmetros:
        - xpath (str): Caminho XPath do elemento no qual o swipe será aplicado.
        - direction (str): Direção do movimento — pode ser 'up', 'down', 'left' ou 'right'. Padrão: 'down'.
        - percent (float): Proporção do elemento que será usada no gesto (entre 0.01 e 1.0). Padrão: 0.75.
        - speed (int): Velocidade do swipe em pixels por segundo. Padrão: 800.
        """

        # Validação dos parâmetros antes de tentar o gesto
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("O parâmetro 'direction' deve ser: 'up', 'down', 'left' ou 'right'.")
        if not (0.01 <= percent <= 1.0):
            raise ValueError("O parâmetro 'percent' deve estar entre 0.01 e 1.0.")
        if speed <= 0:
            raise ValueError("O parâmetro 'speed' deve ser um número positivo.")

        try:
            # Obtém o driver Appium ativo
            driver = self.driver

            # Localiza o elemento de destino através do XPath fornecido
            element = driver.find_element(AppiumBy.XPATH, xpath)

            # Executa o gesto de swipe dentro do elemento utilizando o comando do Appium 2.x
            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,   # ID interno do elemento localizado
                "direction": direction,    # Direção do swipe
                "percent": percent,        # Porcentagem da área usada para deslizar
                "speed": speed             # Velocidade em pixels por segundo
            })

            # Registra no log do Robot Framework os detalhes do gesto (útil para debug e relatórios)
            self._builtin.log(
                f"[SUCESSO] Scroll dentro do elemento '{xpath}' com direction='{direction}', percent={percent}, speed={speed}.",
                "INFO"
            )

        except Exception as e:
            # Em caso de erro, registra a falha com detalhes no log
            self._builtin.log(
                f"[ERRO] Falha ao executar scroll no elemento '{xpath}': {str(e)}",
                "ERROR"
            )

            # Lança a exceção novamente para interromper o teste (comportamento padrão de falha)
            raise
