from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import subprocess

class NetworkStatus:
    """
    Keyword que interpreta a bitmask de conexão retornada pelo Appium e identifica o status da rede do dispositivo Android.
    Considera também o modo avião via ADB.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

# a info sobre o tipo de conexão é entregue em bits (binário, então: 0 e 1)
# os numeros inteiros que a gente usa no dia a dia (nesse caso 0, 1, 2, 4 e 6) são armazenados como combinações de bits 
# quando a gente usa o bitmask, a gente faz um combinação de múltiplos significados dentro de um mesmo número
# por isso, a gente usa o bitwise AND pra comparar cada bit na mesma posição dos dois numeros e retornar 1 (caso ambos sejam 1) ou 0
# dessa forma, a gente interpreta esses bits e compara com o retorno encontrado

    def __init__(self):
        self._builtin = BuiltIn()

    def _obter_driver_appium(self):
    # Pega o driver atual conectado com o Appium
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()
    
    def _interpretar_bitmask(self, status): # Interpreta os bits:
    # usando bitwise AND pra interpretar o numero retornado
    # ele so verifica se dados/wifi estão ligados, não se estão realmente funcionando
        """
        Retorna os flags interpretados a partir do bitmask:
        (tem_wifi, tem_dados, sem_rede)
        """
        tem_wifi = (status & 2) != 0
        tem_dados = (status & 4) != 0
        sem_rede = status == 0
        return tem_wifi, tem_dados, sem_rede
    
    def _modo_aviao_ativo(self):
        """
        Retorna True se o modo avião estiver ativado via settings, False caso contrário.
        """
        try:
            resultado = subprocess.run(
                ['adb', 'shell', 'settings', 'get', 'global', 'airplane_mode_on'],
                capture_output=True,
                text=True,
                timeout=2
            )
            return resultado.stdout.strip() == '1'
        except Exception as e:
            self._builtin.log(f"Erro ao verificar modo avião: {e}", level='WARN')
            return False
        
     # Retorna a string adequada com base nos bits e (opcionalmente) na conectividade
    def _definir_status_rede(self, tem_wifi, tem_dados, em_modo_aviao, sem_rede):
    # usa if/elif pra construir a lógica e retornar uma string clara com o status
        """
        Com base nos bits ativos e na verificação de conexão, retorna o status final da rede em string.
        """
        if em_modo_aviao:
            return 'AIRPLANE_MODE'
        elif sem_rede: #-> pro caso de nenhum bit ativo (dados, wifi e modo avião desligados) -> NÃO HÁ CONEXÃO ATIVA
            return 'NONE'
        elif tem_wifi and tem_dados:
            return 'WIFI_AND_DATA'
        elif tem_wifi:
            return 'WIFI_ONLY'           
        elif tem_dados:
            return 'DATA_ONLY'
        # tem um fallback final pro caso de nenhuma das condições anteriores ser atendida (oq não deveria acontecer em condições normais)
        else: #-> serve pra cobrir possíveis anomalias no valor de "status" ou erro de leitura do bitmask
            return 'UNKNOWN'

    @keyword('Obter Status de Rede Legível')
    def obter_status_de_rede_legivel(self):
    # default de validar_conectividade é false. nesse caso, ele so analisa o bitmask, sem testar a conexão com a internet
        """
        Retorna uma string legível representando o tipo de conexão de rede atual.

        Usa:
        - `driver.network_connection` para identificar tipo de rede (Wi-Fi, dados)
        - `adb shell settings get global airplane_mode_on` para detectar modo avião

        Retornos possíveis:
        - WIFI_AND_DATA
        - WIFI_ONLY
        - DATA_ONLY
        - AIRPLANE_MODE
        - NONE
        - UNKNOWN
        """

        driver = self._obter_driver_appium()
        status = driver.network_connection # Obtém o status da rede como inteiro (bitmask)

        # Exibe bitmask e binário lidos para debug
        # pra facilitar o entendimento e tornar o script transparente e fácil de depurar
        self._builtin.log(f"Bitmask lido: {status} (binário: {bin(status)})", level='INFO')

        tem_wifi, tem_dados, sem_rede = self._interpretar_bitmask(status)
        em_modo_aviao = self._modo_aviao_ativo()

        # Exibe interpretação dos bits (ou seja: mostra se os bits tão ativos com True e False)
        self._builtin.log(f"Wi-Fi ativo: {tem_wifi}", level='INFO')
        self._builtin.log(f"Dados móveis ativos: {tem_dados}", level='INFO')
        self._builtin.log(f"Modo avião ativo: {em_modo_aviao}", level='INFO')
        self._builtin.log(f"Sem rede ativa: {sem_rede}", level='INFO')

        # Define o status final com base nos bits e, se aplicável, na conectividade
        status_final = self._definir_status_rede(tem_wifi, tem_dados, em_modo_aviao, sem_rede)
        self._builtin.log(f"Status final interpretado: {status_final}", level='INFO')

        return status_final