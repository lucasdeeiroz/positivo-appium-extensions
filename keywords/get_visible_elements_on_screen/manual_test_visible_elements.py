from VisibleElements import VisibleElements
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import json

# cria um biultin fake -> .log() faz print e .fail() lança exceção
class FakeBuiltIn:
    def log(self, msg, level=None):
        print(f"[{level}] {msg}")
    def fail(self, msg):
        raise Exception(msg)
    
# Mock do VisibleElements (que a gente criou em Python) pra injetar o driver diretamente
class MockVisibleElements(VisibleElements):
    def __init__(self, mock_driver):
        self._driver = mock_driver
        self._builtin = FakeBuiltIn()

    def _get_appium_driver(self):
        return self._driver


# Mocks básicos para simular elementos
class Element:
    def __init__(self, displayed, rid, text="", cls="", clickable="false", raise_display=False):
        self.text = text
        self.attrs = {
            "resource-id": rid,
            "content-desc": None,
            "class": cls,
            "clickable": clickable
        }
        self.raise_display = raise_display
        self._displayed = displayed

    def is_displayed(self):
        if self.raise_display:
            raise StaleElementReferenceException("Elemento obsoleto simulado")
        return self._displayed

    def get_attribute(self, name):
        if name not in self.attrs:
            raise NoSuchElementException(f"Atributo '{name}' não encontrado")
        return self.attrs[name]


# Mock do driver Appium
class MockDriver:
    def __init__(self, elements):
        self.elements = elements

    def find_elements(self, by, locator):
        return self.elements


# === EXECUÇÃO MANUAL DOS TESTES ===
if __name__ == "__main__":
    print("=== Testes manuais: Get Visible Elements On Screen ===\n")

    casos = [
        # caso de VISIBILIDADE
        # nesse caso, temos um unico elemento visível, com resource_id, filtro = all
        # o elemento passa em todos os filtros, então, é incluído na lista retornada
        {
            "desc": "Elemento visível com resource_id",
            "elements": [Element(True, "btn_login", text="Entrar", cls="android.widget.Button", clickable="true")],
            "filter_type": "all",
            "debug": False,
            "esperado": ["btn_login"]
        },
        # caso de (IN)VISIBILIDADE
        # nesse caso, temos um unico elemento, com resource_id, mas tá invisível, filtro = all
        # como é necessário que o elemento seja visível,ele é descartado e espera-se que se retorne uma lista vazia: []
        {
            "desc": "Elemento invisível com resource_id",
            "elements": [Element(False, "btn_cancel")],
            "filter_type": "all",
            "debug": False,
            "esperado": []
        },
        # caso de FILTRO POR TIPO
        # nesse caso, temos dois elementos visíveis, com resource_id, um é button e o outro é textview, filtro = button
        # como o filtro é button, apenas o elemento da classe "Button" deve ser retornado
        {
            "desc": "Filtro por botão (classe Button)",
            "elements": [
                Element(True, "btn_ok", cls="android.widget.Button", clickable="true"),
                Element(True, "txt_header", cls="android.widget.TextView")
            ],
            "filter_type": "button",
            "debug": False,
            "esperado": ["btn_ok"]
        },
        # caso de FORMATO DEBUG
        # nesse caso, temos dois elementos visíveis, com resource_id, classe EditText (input), filtro = input, modo debug = true
        # como ambos atendem aos critérios, e o modo debug tá ativado, o retorno esperado deve conter dicionários completos com os atributos de cada elemento
        {
            "desc": "Filtro por input (classe EditText)",
            "elements": [
                Element(True, "inp_email", cls="android.widget.EditText"),
                Element(True, "inp_senha", cls="android.widget.EditText")
            ],
            "filter_type": "input",
            "debug": True,
            "esperado": [
                {"resource_id": "inp_email", "accessibility_id": "null", "text": "", "class": "android.widget.EditText", "clickable": False},
                {"resource_id": "inp_senha", "accessibility_id": "null", "text": "", "class": "android.widget.EditText", "clickable": False},
            ]
        },
        # caso de TRATAMENTO DE EXCEÇÃO
        # nesse caso, temos três elementos visíveis, mas um deles tá configurado pra lançar uma exceção com raise_display = true
        # dois dos 3 elementos atendem aos critérios e a exceção é tratada com try/except, sendo ignorada no log.
        {
            "desc": "Elemento que gera exceção (Stale)",
            "elements": [
                Element(True, "btn1"),
                Element(True, "btn2", raise_display=True), # o raise_display vai simular que o elemento virou obsoleto -> cai no except
                Element(True, "btn3")
            ],
            "filter_type": "all",
            "debug": False,
            "esperado": ["btn1", "btn3"]
        },
    ]

    for caso in casos:
        print(f"--- Teste: {caso['desc']} ---")
        driver = MockDriver(caso["elements"])
        visible = VisibleElements()
        visible = MockVisibleElements(driver)

        resultado = visible.get_visible_elements_on_screen(filter_type=caso["filter_type"], debug=caso["debug"])
        # if caso["debug"]:
        #     print("Resultado:")
        #     print(json.dumps(resultado, indent=2))
        #     print("Esperado :")
        #     print(json.dumps(caso["esperado"], indent=2))
        # else:
        #     print("Resultado:", resultado)
        #     print("Esperado :", caso["esperado"])
        print("✅ PASSOU\n" if resultado == caso["esperado"] else "❌ FALHOU\n")