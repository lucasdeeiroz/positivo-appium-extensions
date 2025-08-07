*** Settings ***
Library    AppiumLibrary
Resource   base.resource

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
