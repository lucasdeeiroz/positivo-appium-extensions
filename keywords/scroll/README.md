# Scroll Element Library

Biblioteca customizada para **Robot Framework** e **Appium**, responsável por executar gestos de *scroll/swipe* dentro de elementos específicos da interface de aplicativos móveis.  
Desenvolvida para oferecer **controle preciso sobre direção, distância e velocidade**, garantindo interações confiáveis mesmo em áreas internas de elementos complexos.

---

## Sumário
1. [Visão Geral](#visão-geral)  
2. [Pré-requisitos](#pré-requisitos)  
3. [Instalação](#instalação)  
4. [Uso](#uso)  
5. [Parâmetros](#parâmetros)  
6. [Exemplos de Uso](#exemplos-de-uso)  
7. [Observações](#observações)  
8. [Licença](#licença)

---

## Visão Geral
O keyword `Scroll Inside` é um *wrapper* para o comando **`mobile: swipeGesture`** do Appium, permitindo:
- Localização de elementos por diferentes estratégias (`id`, `xpath`, `accessibility_id`, etc.).
- Definição da direção (`up`, `down`, `left`, `right`).
- Controle do percentual de deslocamento dentro do elemento.
- Ajuste de velocidade do gesto.

Essa abordagem evita *scrolls* imprecisos na tela inteira, atuando diretamente **apenas no elemento alvo**.

---

## Pré-requisitos
- **Python** 3.7+
- **Appium Server** configurado e em execução.
- **Robot Framework** instalado:
  ```bash
  pip install robotframework
  ```
- **AppiumLibrary** para Robot Framework:
  ```bash
  pip install robotframework-appiumlibrary
  ```

---

## Instalação
1. Adicione o arquivo `scroll.py` ao diretório do seu projeto de testes.
2. Importe a biblioteca no seu arquivo `.robot`:
   ```robot
   Library    scroll.py
   Library    AppiumLibrary
   ```

---

## Uso
### Sintaxe
```robot
Scroll Inside    <locator>    direction=<up|down|left|right>    percent=<0.01-1.0>    speed=<ms>
```

### Formatos de Localizador Suportados
- `id=com.exemplo:id/meu_elemento`
- `xpath=//android.widget.TextView[@text="Exemplo"]`
- `accessibility_id=MeuElemento`
- `class_name=android.widget.Button`
- `android_uiautomator=new UiSelector().text("Exemplo")`
- `ios_predicate=name == "Exemplo"`
- `ios_class_chain=**/XCUIElementTypeButton[`name == "Exemplo"`]`

Também é possível passar apenas `//meu/xpath` que será interpretado automaticamente como `xpath=...`.

---

## Parâmetros
| Nome         | Tipo  | Obrigatório | Padrão  | Descrição |
|--------------|-------|-------------|---------|-----------|
| `locator`    | str   | ✅          | —       | Localizador do elemento alvo |
| `direction`  | str   | ❌          | `down`  | Direção do scroll (`up`, `down`, `left`, `right`) |
| `percent`    | float | ❌          | `0.75`  | Percentual do deslocamento (0.01 a 1.0) |
| `speed`      | int   | ❌          | `800`   | Velocidade do gesto em milissegundos |

---

## Exemplos de Uso
```robot
*** Settings ***
Library    scroll.py
Library    AppiumLibrary

*** Test Cases ***
Scroll Para Baixo Por XPath
    Scroll Inside    xpath=//android.widget.ScrollView    direction=down

Scroll Para Cima Usando ID
    Scroll Inside    id=com.exemplo:id/lista    direction=up    percent=0.5    speed=1000
```

---

## Observações
- O `Scroll Inside` atua **apenas dentro do elemento localizado**, não afetando a tela inteira.
- O comando `mobile: swipeGesture` é compatível com drivers Appium que utilizam **W3C Actions**.
- Valores muito baixos em `percent` podem resultar em gestos imperceptíveis.

---

## Licença
Este projeto é de uso livre, podendo ser modificado e distribuído para fins pessoais ou comerciais.
