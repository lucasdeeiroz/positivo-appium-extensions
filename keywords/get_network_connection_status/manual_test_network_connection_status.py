from keywords.get_network_connection_status.NetworkStatus import NetworkStatus

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
def criar_mock_subprocess(modo_aviao_ativo):
    def mock_subprocess_run(args, capture_output=True, text=True, timeout=2, stdout=None, stderr=None):
        class Resultado:
            def __init__(self, stdout_text):
                self.stdout = stdout_text

        if 'airplane_mode_on' in args:
            return Resultado('1\n' if modo_aviao_ativo else '0\n')
        
        return Resultado('')

    return mock_subprocess_run


# === EXECUÇÃO ===
if __name__ == "__main__":
    import subprocess

    # Lista de testes com bitmask e modo avião
    casos_de_teste = [
        {"bitmask": 0, "desc": "Sem rede (NONE)", "modo_aviao": False},
        {"bitmask": 1, "desc": "Modo avião ativado (AIRPLANE_MODE)", "modo_aviao": True},
        {"bitmask": 2, "desc": "Wi-Fi ativo", "modo_aviao": False},
        {"bitmask": 4, "desc": "Dados móveis ativos", "modo_aviao": False},
        {"bitmask": 6, "desc": "Wi-Fi e dados ativos", "modo_aviao": False},
        {"bitmask": 8, "desc": "Bitmask desconhecido (UNKNOWN)", "modo_aviao": False},
    ]

    for caso in casos_de_teste:
        print(f"\n--- Teste: {caso['desc']} ---")

        # Substitui o subprocess.run por um mock personalizado
        subprocess.run = criar_mock_subprocess(caso["modo_aviao"])

        # Instancia o mock BuiltIn e AppiumLibrary
        builtin = MockBuiltIn()
        builtin.mock_appium = MockAppiumLibrary(caso["bitmask"])

        # Instancia a keyword e injeta o BuiltIn mockado
        net = NetworkStatus()
        net._builtin = builtin

        status = net.obter_status_de_rede_legivel()
        print(f"Status final retornado: {status}")