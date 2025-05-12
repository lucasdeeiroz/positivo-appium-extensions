*** Settings ***
Documentation    Suite de testes do uso do clique em ponto específico

Library     AppiumLibrary
Library     ../click_point/click_point.py

*** Test Cases ***
Deve poder clicar em um ponto específico do Google Maps
    [Tags]    click_point
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.apps.maps
    ...                 appActivity=com.google.android.maps.MapsActivity
    
    # Obtém as dimensões da tela
    ${width}=    Get Window Width
    ${height}=   Get Window Height
    
    # Clica no centro da tela
    ${center_x}=    Evaluate    ${width}/2
    ${center_y}=    Evaluate    ${height}/2
    Click A Point    ${center_x}    ${center_y}    200
    Sleep    2
    
    # Clica em outro ponto (exemplo: topo direito)
    ${top_right_x}=    Evaluate    ${width}-50
    ${top_right_y}=    Evaluate    50
    Click A Point    ${top_right_x}    ${top_right_y}    200
    Sleep    2
    
    Close Application

Deve falhar ao usar coordenadas inválidas
    [Tags]    error
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.apps.maps
    ...                 appActivity=com.google.android.maps.MapsActivity
    
    Run Keyword And Expect Error    ValueError*    Click A Point    x=abc    y=100
    
    Close Application