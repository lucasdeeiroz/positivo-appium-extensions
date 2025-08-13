# Swipe Element Library

Biblioteca customizada para **Robot Framework** e **Appium**, responsável por executar gestos de swipe (drag gesture) em elementos da interface de aplicativos móveis.  
Desenvolvida para oferecer maior controle sobre direção, distância e velocidade dos gestos, evitando interações imprecisas próximas às bordas dos elementos.

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
O keyword `Swipe Element` é um wrapper para o comando **`mobile: dragGesture`** do Appium, permitindo:
- Localização de elementos por diferentes estratégias (`id`, `xpath`, `accessibility_id`, etc.)
- Definição da direção (`up`, `down`, `left`, `right`)
- Controle do percentual de deslocamento (incluindo valores acima de 100%)
- Ajuste de velocidade do gesto
- Margem inicial para evitar cliques nas extremidades

---

## Pré-requisitos
- **Python** 3.7+
- **Appium Server** configurado e em execução
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
1. Adicione o arquivo `swipe.py` ao diretório do seu projeto de testes.
2. Importe a biblioteca no seu arquivo `.robot`:
   ```robot
   Library    swipe.py
   Library    AppiumLibrary
   ```

---

## Uso
### Sintaxe
```robot
Swipe Element    <locator>    direction=<up|down|left|right>    percent=<0.01-2.0>    speed=<ms>
```

### Formatos de Localizador Suportados
- `id=com.exemplo:id/meu_elemento`
- `xpath=//android.widget.TextView[@text="Exemplo"]`
- `accessibility_id=MeuElemento`
- `class_name=android.widget.Button`
- `android_uiautomator=new UiSelector().text("Exemplo")`
- `ios_predicate=name == "Exemplo"`
- `ios_class_chain=**/XCUIElementTypeButton[`name == "Exemplo"`]`

---

## Parâmetros
| Nome         | Tipo  | Obrigatório | Padrão  | Descrição |
|--------------|-------|-------------|---------|-----------|
| `locator`    | str   | ✅          | —       | Localizador do elemento alvo |
| `direction`  | str   | ❌          | `right` | Direção do swipe (`up`, `down`, `left`, `right`) |
| `percent`    | float | ❌          | `0.5`   | Percentual do deslocamento (0.01 a 2.0) |
| `speed`      | int   | ❌          | `800`   | Velocidade do gesto em milissegundos |

---

## Exemplos de Uso
```robot
*** Settings ***
Library    swipe.py
Library    AppiumLibrary

*** Test Cases ***
Swipe Para Direita
    Swipe Element    xpath=//android.widget.TextView[@text="Exemplo"]    direction=right    percent=0.8    speed=500

Swipe Para Baixo Usando ID
    Swipe Element    id=com.exemplo:id/lista    direction=down    percent=1.5    speed=800
```

---

## Observações
- O parâmetro `percent` pode ultrapassar `1.0` para permitir que o swipe vá além do tamanho do elemento.
- Uma margem inicial fixa de **5%** é aplicada para evitar início do gesto nas bordas.
- O `mobile: dragGesture` requer que o driver Appium esteja usando as **W3C Actions**.

---

## Licença
Este projeto é de uso livre, podendo ser modificado e distribuído para fins pessoais ou comerciais.
