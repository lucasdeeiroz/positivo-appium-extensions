from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import subprocess

class NetworkStatus:
    """
    Keyword que tem como objetivo obter o status de rede do dispositivo Android via Appium.
    Permite interpretar a bitmask de conexão e opcionalmente validar conectividade real com a internet.
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
    # usamos bitwise AND pra interpretar o numero retornado
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
            valor = resultado.stdout.strip()
            return valor == '1'
        except Exception as e:
            self._builtin.log(f"Erro ao verificar modo avião: {e}", level='WARN')
            return False
        
    def _validar_conectividade_real(self, validar):
    # Se ativado, valida se há conexão real via dumpsys connectivity
    # roda -> adb shell dumpsys connectivity usando o módulo subprocess pra checar se a internet realmente ta funcionando
    # adb shell -> executa um comando dentro do Android via ADB
    # dumpsys connectivity -> verifica a conectividade
    # se essa resposta vier, é pq a conexão realmente funciona.
    # Se não vier, ou der erro, a rede pode estar ativa, mas sem internet
    # caso o adb shell falhe em dispositivos reais (por restrições do Android/fabricantes, ou até por políticas de segurança)
    # ela vai tratar como exceção e cair direto em NO_CONNECTION, sem quebrar o teste. mas não impacta da leitura do bitmask
        """
        Se 'validar' for True, verifica via `dumpsys connectivity` se há rede Wi-Fi ativa e validada.
        Retorna True se a conectividade for confirmada, False se não houver. None se não for solicitado.
        Considera apenas NetworkAgentInfo que esteja 'connected' e contenha 'is_validated'.
        """
        if not validar:
        # Se o argumento for False, então ele nem testa e retorna None
            return None #-> o None é uma forma de dizer: não validei a conexão real, só interpretei o bitmask

        try:
            resultado = subprocess.run(
                ['adb', 'shell', 'dumpsys', 'connectivity'],
                capture_output=True,
                text=True,
                timeout=5
            )
            saida = resultado.stdout.lower()
            # Verifica se há alguma rede Wi-Fi ativa e validada
            # Log para depuração da saída completa (limitado para não poluir demais)
            self._builtin.log(f"Saída do dumpsys (inteira, para depuração):\\n{saida[:1000]}...", level='DEBUG')

            # Divide a saída em blocos de NetworkAgentInfo.
            # Se NetworkAgentInfo{ pode não estar no início do primeiro bloco,
            # então todos os blocos precisarão ser inspecionados.
            blocos = saida.split('networkagentinfo{')
            self._builtin.log(f"Total de blocos NetworkAgentInfo encontrados (após split): {len(blocos)}", level='DEBUG')

            for i, bloco in enumerate(blocos):
                # Não ignora o primeiro bloco, pois ele pode conter NetworkAgentInfo,
                # especialmente se a string 'networkagentinfo{' não estiver no início exato da saída.
                
                self._builtin.log(f"Analisando bloco {i}:\\n{bloco[:500]}...", level='DEBUG') # Limita o log do bloco

                tem_wifi_keyword = 'ni{wifi' in bloco
                tem_connected = 'connected' in bloco
                tem_validated = 'validated' in bloco

                self._builtin.log(f"Bloco {i} - 'wifi' presente: {tem_wifi_keyword}", level='DEBUG')
                self._builtin.log(f"Bloco {i} - 'connected' presente: {tem_connected}", level='DEBUG')
                self._builtin.log(f"Bloco {i} - 'validated' presente: {tem_validated}", level='DEBUG')

                if tem_wifi_keyword and tem_connected and tem_validated:
                    self._builtin.log(f"BLOCO {i} ATENDE TODAS AS CONDIÇÕES! Retornando True.", level='INFO')
                    return True

            self._builtin.log("Nenhum bloco NetworkAgentInfo atendeu a todas as condições.", level='INFO')
            return False
        except Exception as e: #-> cai aqi se falhar (sem resposta, timeout, erro no adb)
            self._builtin.log(f"Erro ao validar conectividade via dumpsys: {e}", level='WARN')
            return False
        
    # Retorna a string adequada com base nos bits e (opcionalmente) na conectividade
    def _definir_status_rede(self, tem_wifi, tem_dados, em_modo_aviao, sem_rede, conectado):
    # usa if/elif pra construir a lógica e retornar uma string clara com o status
        """
        Com base nos bits ativos e na verificação de conexão, retorna o status final da rede em string.
        """
        if em_modo_aviao:
            return 'AIRPLANE_MODE'
        elif sem_rede: #-> pro caso de nenhum bit ativo (dados, wifi e modo avião desligados) -> NÃO HÁ CONEXÃO ATIVA
            return 'NONE'
        # se os dois bits estiverem ligados, o Appium retorna status = 6 -> aí verificamos o valor de "conectado"
        # se "conectado" for True, realmente tem acesso à internet -> 'WIFI_AND_DATA_CONNECTED'
        # se "conectado" for False, os dois estão ativos, mas sem acesso real -> 'WIFI_AND_DATA_NO_CONNECTION'
        elif tem_wifi and tem_dados:
            return 'WIFI_AND_DATA_CONNECTED' if conectado else 'WIFI_AND_DATA_NO_CONNECTION'
        # pro caso de "conectado" ser None (validação não foi feita) -> 'WIFI_ONLY'
        # se "conectado" for True -> tbm retorna 'WIFI_ONLY'
        # mas se for False -> 'WIFI_ONLY_NO_CONNECTION'
        elif tem_wifi:
            return 'WIFI_ONLY' if conectado is None else (
                'WIFI_ONLY' if conectado else 'WIFI_ONLY_NO_CONNECTION'
            )
        elif tem_dados: #-> segue a mesma lógica do tem_wifi, mas pra dados móveis
            return 'DATA_ONLY' if conectado is None else (
                'DATA_ONLY' if conectado else 'DATA_ONLY_NO_CONNECTION'
            )
        # tem um fallback final pro caso de nenhuma das condições anteriores ser atendida (oq não deveria acontecer em condições normais)
        else: #-> serve pra cobrir possíveis anomalias no valor de "status" ou erro de leitura do bitmask
            return 'UNKNOWN'

    @keyword('Obter Status de Rede Legível')
    def obter_status_de_rede_legivel(self, validar_conectividade=False):
    # default de validar_conectividade é false. nesse caso, ele so analisa o bitmask, sem testar a conexão com a internet
        """
        Retorna uma string legível representando o tipo de conexão de rede atual.

        Usa:
        - `driver.network_connection` para identificar tipo de rede (Wi-Fi, dados)
        - `adb shell settings get global airplane_mode_on` para identificar modo avião
        - `adb shell dumpsys connectivity` para validar conexão real (se solicitado)

        Argumentos:
        | validar_conectividade | (Opcional) Se True, tenta validar a conexão via `dumpsys connectivity`. Default: False |

        Retornos possíveis:
        - WIFI_AND_DATA
        - WIFI_ONLY
        - DATA_ONLY
        - AIRPLANE_MODE
        - NONE
        - Se validar_conectividade=True: *_CONNECTED / *_NO_CONNECTION (caso validar_conectividade=True)

        Exemplo:
        | ${status}= | Obter Status de Rede Legível | validar_conectividade=${True} |
        """

        driver = self._obter_driver_appium()
        status = driver.network_connection # Obtém o status da rede como inteiro (bitmask)

        # Exibe bitmask e binário lidos para debug
        # pra facilitar o entendimento e tornar o script transparente e fácil de depurar
        self._builtin.log(f"Bitmask lido: {status} (binário: {bin(status)})", level='INFO')

        tem_wifi, tem_dados, sem_rede = self._interpretar_bitmask(status)
        em_modo_aviao = self._modo_aviao_ativo()
        # Valida a conexão real se solicitado -> pro caso de validar_conectividade ser True
        conectado = self._validar_conectividade_real(validar_conectividade)

        # Exibe interpretação dos bits (ou seja: mostra se os bits tão ativos com True e False)
        self._builtin.log(f"Wi-Fi ativo: {tem_wifi}", level='INFO')
        self._builtin.log(f"Dados móveis ativos: {tem_dados}", level='INFO')
        self._builtin.log(f"Modo avião ativo: {em_modo_aviao}", level='INFO')
        self._builtin.log(f"Sem rede ativa: {sem_rede}", level='INFO')

        # Define o status final com base nos bits e, se aplicável, na conectividade
        status_final = self._definir_status_rede(tem_wifi, tem_dados, em_modo_aviao, sem_rede, conectado)
        self._builtin.log(f"Status final interpretado: {status_final}", level='INFO')

        return status_final