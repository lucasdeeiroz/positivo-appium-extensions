import time
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.interaction import KEY

# Define a classe 'Appiumclick' que conterá nossa palavra-chave personalizada
class Appiumclick:

    # O método construtor (_init_) é chamado quando uma instância da classe é criada
    def __init__(self):
        # Obtém uma instância da biblioteca 'BuiltIn' do Robot Framework
        # Isso permite usar palavras-chave do 'BuiltIn' dentro desta classe
        self._builtin = BuiltIn()

    # Define uma propriedade chamada '_driver'
    # Esta propriedade permite acessar o driver atual do Appium de forma conveniente
    @property
    def _driver(self):
        # Usa o 'BuiltIn' para obter a instância da biblioteca 'AppiumLibrary'
        # e então acessa seu atributo '_current_application()', que é o driver do Appium
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    # Define a palavra-chave personalizada 'ClickC' usando o decorador '@keyword'
    # Esta palavra-chave receberá um 'locator' (identificador do elemento),
    # um 'xoffset' (deslocamento horizontal) e um 'yoffset' (deslocamento vertical)
    @keyword('ClickC')
    def clickC(self, locator, xoffset, yoffset):
        # Obtém o driver do Appium usando a propriedade '_driver' definida acima
        driver = self._driver
        # Obtém a instância da biblioteca 'AppiumLibrary' para usar seus métodos
        appium_lib = self._builtin.get_library_instance('AppiumLibrary')

        # Log para informar que a verificação do driver está começando
        self._builtin.log("Verificando se o driver está ativo", level='INFO')
        # Verifica se o driver foi inicializado. Se não, lança um erro.
        if not driver:
            raise RuntimeError("Driver não está inicializado ou conectado ao dispositivo.")

        # Log para informar a busca pelo elemento
        self._builtin.log(f"Procurando elemento com locator: {locator}", level='INFO')
        try:
            # Tenta encontrar o elemento na tela usando o 'locator' fornecido
            # Usa o método 'get_webelement' da 'AppiumLibrary'
            element = appium_lib.get_webelement(locator)
        except Exception as e:
            # Se o elemento não for encontrado, lança um erro 'ValueError' com detalhes
            raise ValueError(f"Elemento com locator '{locator}' não encontrado: {e}")

        # Obtém a localização (coordenadas x, y do canto superior esquerdo) do elemento
        location = element.location
        # Obtém o tamanho (largura e altura) do elemento
        size = element.size
        # Log com a localização e tamanho encontrados
        self._builtin.log(f"Localização do elemento: {location}, Tamanho: {size}", level='INFO')

        try:
            # Tenta converter os offsets (deslocamentos) para números de ponto flutuante (float)
            xoffset = float(xoffset)
            yoffset = float(yoffset)
        except Exception:
            # Se a conversão falhar, lança um erro, pois os offsets devem ser números
            raise ValueError("xoffset e yoffset devem ser números (pixels ou fração de 0 a 1 para porcentagem)")

        # Verifica se o 'xoffset' está entre 0 e 1 (inclusive)
        if 0 <= xoffset <= 1:
            # Se sim, interpreta como uma porcentagem da largura do elemento
            # e calcula o deslocamento em pixels
            xoffset_px = int(size['width'] * xoffset)
        else:
            # Se não, interpreta como um valor direto em pixels
            xoffset_px = int(xoffset)

        # Faz o mesmo para o 'yoffset', mas usando a altura do elemento
        if 0 <= yoffset <= 1:
            yoffset_px = int(size['height'] * yoffset)
        else:
            yoffset_px = int(yoffset)

        # Calcula a coordenada X final para o clique:
        # Posição X do elemento + deslocamento X em pixels
        x = location['x'] + xoffset_px
        # Calcula a coordenada Y final para o clique:
        # Posição Y do elemento + deslocamento Y em pixels
        y = location['y'] + yoffset_px
        # Log com as coordenadas finais calculadas
        self._builtin.log(f"Coordenadas calculadas para clique: ({x}, {y}) (offsets: {xoffset_px}, {yoffset_px})", level='INFO')

        # Obtém o tamanho atual da janela (tela) do dispositivo
        window_size = driver.get_window_size()
        # Log com o tamanho da tela
        self._builtin.log(f"Tamanho da tela: {window_size}", level='INFO')

        # Verifica se as coordenadas calculadas (x, y) estão dentro dos limites da tela
        if not (0 <= x <= window_size['width'] and 0 <= y <= window_size['height']):
            # Se estiverem fora da tela, lança um erro
            raise ValueError(f"Coordenadas ({x}, {y}) estão fora da tela do dispositivo.")

        try:
            # Log informando que o clique será executado usando W3C Actions
            self._builtin.log("Executando clique usando W3C Actions", level='INFO')
            # Cria um objeto 'PointerInput' para simular um toque ('touch') com um dedo ('finger')
            touch = PointerInput("touch", "finger")
            # Cria um 'ActionBuilder' associado ao driver e ao tipo de ponteiro 'touch'
            # Isso permitirá construir a sequência de ações de toque
            actions = ActionBuilder(driver, mouse=touch)

            # Adiciona a ação de mover o ponteiro (dedo) para as coordenadas (x, y) calculadas
            actions.pointer_action.move_to_location(x, y)

            # Adiciona a ação de pressionar o ponteiro (dedo) na tela (início do toque)
            actions.pointer_action.pointer_down()

            # Adiciona uma pequena pausa (0.2 segundos) para simular um toque mais realista
            # e garantir que a ação seja registrada corretamente
            time.sleep(0.2)

            # Adiciona a ação de levantar o ponteiro (dedo) da tela (fim do toque)
            actions.pointer_action.pointer_up()

            # Executa todas as ações adicionadas ao 'ActionBuilder' na sequência definida
            actions.perform()

            # Log informando que o clique foi bem-sucedido
            self._builtin.log("Clique realizado com sucesso via W3C Actions", level='INFO')
        except Exception as e:
            # Se ocorrer qualquer erro durante a execução das ações W3C,
            # loga o erro e o relança para que o Robot Framework o trate
            self._builtin.log(f"Erro ao executar W3C Actions: {e}", level='ERROR')
            raise