from NetworkStatus import NetworkStatus

# Mock do driver do Appium
class MockDriver:
    def __init__(self, network_status):
        self.network_connection = network_status

# Mock da biblioteca AppiumLibrary
class MockAppiumLibrary:
    def __init__(self, network_status):
        self.driver = MockDriver(network_status)

    def _current_application(self):
        return self.driver

# Mock do BuiltIn do Robot Framework
class MockBuiltIn:
    def get_library_instance(self, name):
        return self.mock_appium

    def log(self, message, level):
        print(f"[{level}] {message}")

# Mock genérico para subprocess.run
def criar_mock_subprocess(modo_aviao_ativo, conectado):
    def mock_subprocess_run(args, capture_output=True, text=True, timeout=2, stdout=None, stderr=None):
        class Resultado:
            def __init__(self, stdout_text):
                self.stdout = stdout_text

        if 'airplane_mode_on' in args:
            return Resultado('1\n' if modo_aviao_ativo else '0\n')

        if 'dumpsys' in args and 'connectivity' in args:
            if conectado:
                mock_output_string = '''
                # COLOQUE AQUI OS 100% DA SAÍDA REAL DO DUMPSYS CONNECTIVITY
                '''
                print(f"DEBUG: Mocking dumpsys connectivity. Output size: {len(mock_output_string)} chars.")
                # print(f"DEBUG: Mocked output content:\n{mock_output_string}") -> descomenta aqi se quiser ver o conteúdo completo

                return Resultado(mock_output_string)
            else:
                return Resultado('networkagentinfo{network{103} ... score(policies : transport_primary&ever_evaluated ...)')
        
        return Resultado('')

    return mock_subprocess_run


# === EXECUÇÃO ===
if __name__ == "__main__":
    import subprocess

    # Lista de testes com bitmask, modo avião e conectividade real 
    casos_de_teste = [
        {"bitmask": 0, "desc": "Sem rede (NONE)", "modo_aviao": False, "conectado": False},
        {"bitmask": 1, "desc": "Modo avião ativado (AIRPLANE_MODE)", "modo_aviao": True, "conectado": False},
        {"bitmask": 2, "desc": "Wi-Fi ativo com conexão", "modo_aviao": False, "conectado": True},
        {"bitmask": 2, "desc": "Wi-Fi ativo sem conexão", "modo_aviao": False, "conectado": False},
        {"bitmask": 4, "desc": "Dados móveis ativos com conexão", "modo_aviao": False, "conectado": True},
        {"bitmask": 6, "desc": "Wi-Fi e dados com conexão", "modo_aviao": False, "conectado": True},
        {"bitmask": 6, "desc": "Wi-Fi e dados sem conexão", "modo_aviao": False, "conectado": False},
    ]

    for caso in casos_de_teste:
        print(f"\n--- Teste: {caso['desc']} ---")

        # Substitui o subprocess.run por um mock personalizado
        subprocess.run = criar_mock_subprocess(caso["modo_aviao"], caso["conectado"])

        # Instancia o mock BuiltIn e AppiumLibrary
        builtin = MockBuiltIn()
        builtin.mock_appium = MockAppiumLibrary(caso["bitmask"])

        # Instancia a keyword e injeta o BuiltIn mockado
        net = NetworkStatus()
        net._builtin = builtin

        status = net.obter_status_de_rede_legivel(validar_conectividade=True)
        print(f"Status final retornado: {status}")