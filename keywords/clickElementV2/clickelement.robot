*** Settings ***
Library           AppiumLibrary
Resource          ./base.resource

*** Test Cases ***
# Clica no centro do elemento 'Camera' (50% largura e 50% altura)
Click Camera At Center
    [Tags]    camera
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    ClickC    xpath=//android.widget.TextView[@content-desc="Camera"]    0.5    0.5
    Close session

# Clica no canto superior esquerdo do elemento 'Camera' (0% largura, 0% altura)
Click Camera At Top Left
    [Tags]    camera    position
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    ClickC    xpath=//android.widget.TextView[@content-desc="Camera"]    0    0
    Close session

# Clica a 10px da esquerda e 20px do topo do elemento 'Camera'
Click Camera At Absolute Offset
    [Tags]    camera    offset
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    ClickC    xpath=//android.widget.TextView[@content-desc="Camera"]    10    20
    Close session

# Clica no centro do botão 8 da calculadora (50% largura e altura)
Click Calculator Button 8 At Center
    [Tags]    calculadora
    Start session 1
    Wait Until Element Is Visible    id=com.google.android.calculator:id/digit_8    5s
    ClickC    id=com.google.android.calculator:id/digit_8    0.5    0.5
    Close session


################Casos de Erros################


# Testa o erro de elemento não encontrado
ClickC Element Not Found - Corrigido
    [Tags]    erro    localizador
    Start session
    Run Keyword And Expect Error    ValueError: Elemento com locator*    ClickC    xpath=//android.widget.TextView[@content-desc="NaoExiste"]    10    20
    Close session

# Testa o erro de coordenadas fora da tela
ClickC Coordinates Out Of Bounds - Corrigido
    [Tags]    erro    coordenadas
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    Run Keyword And Expect Error    ValueError: Coordenadas*fora da tela*    ClickC    xpath=//android.widget.TextView[@content-desc="Camera"]    1000    1000
    Close session

# Testa o erro de tipo de parâmetro inválido
ClickC Invalid Offset Type - Corrigido
    [Tags]    erro    parametro
    Start session 1
    Wait Until Element Is Visible    id=com.google.android.calculator:id/digit_8    5s
    Run Keyword And Expect Error    ValueError: xoffset e yoffset devem ser números*    ClickC    id=com.google.android.calculator:id/digit_8    abc    def
    Close session