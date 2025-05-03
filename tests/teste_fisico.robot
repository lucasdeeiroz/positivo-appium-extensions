*** Settings ***

Resource     ../resources/base_fisico.resource

*** Test Cases ***

Abrir Calculadora e Fazer Soma
    Start session Calculadora
    Click Element    id=com.miui.calculator:id/btn_1
    Click Element    id=com.miui.calculator:id/btn_plus
    Click Element    id=com.miui.calculator:id/btn_2
    Click Element    id=com.miui.calculator:id/btn_equal
    Sleep            2s

Deve dar zoom no Google Maps
    [Tags]    maps
    Start session Google Maps
    Perform Zoom In Gesture    id=
    Sleep    5