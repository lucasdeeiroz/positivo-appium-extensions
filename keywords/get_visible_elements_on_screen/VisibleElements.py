from robot.api.deco import keyword
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
import json


class VisibleElements:
    """
    Keyword personalizada a ser incluída na AppiumLibrary que retorna elementos visíveis na tela, filtrados por tipo.
    Ideal para testes de validação visual em dispositivos mobile.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def __init__(self):
    # Inicializa a instância BuiltIn
        self._builtin = BuiltIn()

    def _get_appium_driver(self):
    # Pega o driver atual conectado com o Appium
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()
    
    def _find_all_elements(self, driver):
    # Busca todos os elementos da tela atual via xpath genérico e retorna uma lista dos elementos encontrados
        return driver.find_elements(By.XPATH, "//*")

    def _passes_filter(self, el, filter_type):
    # Aplica o filtro desejado e avalia se um elemento passa por ele
    # Tem como parâmetros o elemento a ser avaliado e o tipo de filtro
        """Args:
            el (WebElement): elemento a ser avaliado.
            filter_type (str): Tipo de filtro ('all' | 'clickable' | 'text' | 'button' | 'input').

        Returns:
            bool: True se o elemento atende ao filtro, False caso contrário."""
        
        class_name = el.get_attribute("class") or "" #-> obtém o nome da classe do elemento. Se for None, usa string vazia ("")
        text = el.text or "" #-> obtém o texto visível no elemento. Se for None, retorna string vazia ("")
        clickable = el.get_attribute("clickable") == "true" #-> verifica se o atributo "clickable" é true, retornando True ou False

        if filter_type == "all": #-> todo elemento que tiver acessibility_id e for visível é aceito. Sem restrição extra
            return True
        if filter_type == "clickable": #-> só passa se o elemento tiver clickable="true"
            return clickable
        if filter_type == "text": #-> só passa se o text do elemento for visível (não vazio)
            return bool(text.strip()) #-> usa strip pra ignorar espaços
        if filter_type == "button": #-> retorna True se a classe do elemento contém a palavra "Button"
            return "Button" in class_name
        if filter_type == "input": #-> retorna True se a classe contém "EditText" (que, no caso, é o componente típico de campos de input em Android)
            return "EditText" in class_name
        return False #-> retorna False caso nenhum filtro seja reconhecido (oq na prática não deveria acontecer, já que antes de passar o filtro, a gente valida o filter_type)

    def _build_debug_dict(self, el, rid):
    # Cria um dicionário com os atributos do elemento visível, caso o parâmetro debug=True seja passado na keyword
    # Tem como parâmetro o elemento a ser inspecionado e o valor do acessibility_id do elemento
    # Pode servir pra validar se aid foi atribuído corretamente ou pra depurar testes que falham pq o botão "sumiu"
        """Args:
            el (WebElement): elemento que passou pelos filtros.
            accessibility_id (str): Valor do atributo 'accessibility-id' do elemento.

        Returns:
            dict: Dados estruturados do elemento (usado no modo debug)."""
        
        return {
            "resource_id": rid,
            "accessibility_id": el.get_attribute("content-desc") or "null",
            "text": el.text or "", #-> mostra o texto visível do elemento. se não houver texto, retorna "" pra manter o campo presente
            "class": el.get_attribute("class") or "", #-> retorna a classe do elemento (pra saber o tipo do componente visual). tbm retorna "" caso não haja
            "clickable": el.get_attribute("clickable") == "true" #-> verifica de clickable é true e converte pra booleano
        }

    @keyword("Get Visible Elements On Screen")
    def get_visible_elements_on_screen(self, filter_type: str = "all", debug: bool = False):
    # O valor padrão do filter_type é all. caso queira refinar o filtro, passa o filtro desejado
    # O valor padrão do debug é False. caso queira analisar o modo debug: True
        """
        Retorna os elementos visíveis na tela que possuem resource_ids válidos,
        com filtros opcionais por tipo de elemento. Se debug=True, retorna JSON estruturado.

        Args:
            filter_type (str): Tipo de elemento desejado. Opções: 'all' | 'clickable' | 'text' | 'button' | 'input'.
            debug (bool): se True, retorna JSON com atributos extras (modo debug); se False, retorna apenas IDs.

        Returns:
            list: Lista de resource_ids (ou dicionários, se debug=True)."""

        valid_filters = {'all', 'clickable', 'text', 'button', 'input'} #-> cria a lista de filtros válidos
        filter_type = filter_type.strip().lower() #-> coloca todas as letras minusculas e sem espaço pra evitar erro por problema na digitação
        if filter_type not in valid_filters:
            self._builtin.fail(f"Filter inválido '{filter_type}'. Opções: {valid_filters}")

        driver = self._get_appium_driver()
        try:
            elements = self._find_all_elements(driver)
        except WebDriverException as e:
            self._builtin.log(f"Erro ao buscar elementos: {e}", level="ERROR")
            return []
        
        # antes de qqr filtragem, vamo incluir um log em nível DEBUG pra diagnósticos que eventualmente sejam necessários
        self._builtin.log(f"Elementos na tela (pré-filtro): {len(elements)}", level="DEBUG")

        visible_elements = []
        for el in elements: #-> percorre os elementos capturados via driver.find_elements(By.XPATH, "//*")
            try:
                # primeiro filtro -> visibilidade real
                if not el.is_displayed(): #-> verifica se o elemento tá visualmente presente e renderizado na tela
                    continue #-> caso não seja visível, é ignorado

                # segundo filtro -> precisa ter resource_id
                res_id = el.get_attribute("resource-id")
                if not res_id or not res_id.strip() or res_id.strip().lower() == "null":
                    continue #-> caso não tenha rid, é ignorado
                rid = res_id.strip()

                # terceiro filtro -> tipo do elemento
                if not self._passes_filter(el, filter_type): #-> a filtragem só acontece depois da verificação do is_displayed() e do accessibility-id (pra enxugar o processo)
                    continue #-> caso não passe pelo filtro especificado, é ignorado

                if debug: #-> aqi ele define o modo de retorno
                    visible_elements.append(self._build_debug_dict(el, rid)) #-> modo debug
                else:
                    visible_elements.append(rid) #-> modo normal

            except (StaleElementReferenceException, NoSuchElementException) as ex:
            # NoSuchElementException -> "O elemento que você está tentando acessar não existe"
            # |-> (o seletor pode ta incorreto, e elemento ainda nao foi renderizado na tela, o atributo nao existe)
            # StaleElementReferenceException -> "O elemento que você está tentando acessar não está mais presente no DOM"
            # |-> (qnd o DOM é recarregado ou re-renderizado dinamicamente, a ref foi capturada, mas o elemento foi removido ou recriado na tela)
                self._builtin.log(f"Ignorando elemento por exceção {type(ex).__name__}: {ex}", level="DEBUG")
                continue
                # é válido incluir um contador de exceções pra reportar qnts de cada tipo ocorrem?

        # depois do loop, ele loga a quantidade de elementos que passaram por todas as etapas
        count = len(visible_elements) #-> numero de elementos
        self._builtin.log (f"Total de elementos visíveis (pós-filtro): {count}", level="INFO")

        if debug:
            debug_output = json.dumps(visible_elements, indent=2) #-> o json.dumps vai converter a lista de dicionários pra um texto legível, com identação
            self._builtin.log("DEBUG JSON:\n" + debug_output, level="INFO")

        else:
            self._builtin.log("Elementos visíveis:\n" + json.dumps(visible_elements, indent=2), level="INFO")
        return visible_elements #-> e retorna a lista final de elementos

# FLUXO: todos os elementos da tela -> is_displayed() == True? -> tem accessibility_id? -> passa no filtro? -> ADD NO RESULTADO