# Importa o decorator 'keyword' para registrar funções como keywords no Robot Framework
from robot.api.deco import keyword

# Importa a biblioteca BuiltIn do Robot Framework para acessar funções internas e outras bibliotecas
from robot.libraries.BuiltIn import BuiltIn

# Define a classe da biblioteca customizada. 
# OBS: O nome da classe deve ser igual ao nome do arquivo (.py), em minúsculas e sem underline extra.
class scroll_down:
    # Define o escopo da biblioteca como GLOBAL, assim ela é compartilhada entre todos os testes
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Instancia a biblioteca BuiltIn, permitindo acessar funções e bibliotecas do Robot Framework
        self._builtin = BuiltIn()

    @property
    def driver(self):
        # Obtém a instância do driver atual da AppiumLibrary para manipular a aplicação em teste
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    # Registra o método como uma keyword chamada "Scroll Down Custom" no Robot Framework
    @keyword("Scroll Down Custom")
    def Scroll_Down_Custom(self, start_ratio=0.8, end_ratio=0.2, duration=500):
        """
        Realiza um gesto de scroll para baixo (deslizando de baixo para cima na tela)
        - start_ratio: Posição inicial do swipe como proporção da altura da tela (padrão: 0.8, ou 80%)
        - end_ratio: Posição final do swipe como proporção da altura da tela (padrão: 0.2, ou 20%)
        - duration: Duração do swipe em milissegundos (padrão: 500ms)
        """

        # Valida que os valores de start_ratio e end_ratio estão entre 0 e 1 (exclusivo)
        if not (0 < start_ratio < 1):
            raise ValueError("start_ratio deve estar entre 0 e 1 (exclusivo).")
        if not (0 < end_ratio < 1):
            raise ValueError("end_ratio deve estar entre 0 e 1 (exclusivo).")
        # Valida que a duração é positiva
        if duration <= 0:
            raise ValueError("duration deve ser um inteiro positivo.")

        # Obtém o driver do Appium para executar ações na tela
        driver = self.driver
        # Obtém o tamanho da tela do dispositivo (dicionário com 'width' e 'height')
        size = driver.get_window_size()
        width = size['width']    # largura da tela
        height = size['height']  # altura da tela

        # Define o eixo x como o centro da tela
        x = width // 2
        # Calcula o ponto de início (y_start) e fim (y_end) do swipe, baseado nas proporções informadas
        y_start = int(height * start_ratio)
        y_end = int(height * end_ratio)

        # Realiza o swipe (gesto de deslizar) na tela usando o driver do Appium:
        # - Começa no centro horizontal (x), na posição vertical y_start
        # - Termina no mesmo x, na posição y_end
        # - Duração do gesto definida por 'duration'
        driver.swipe(x, y_start, x, y_end, duration)

        # Registra no log do Robot Framework os detalhes do swipe realizado (para facilitar debug)
        self._builtin.log(
            f"Scroll Down de ({x}, {y_start}) para ({x}, {y_end})", 
            "INFO"
        )
