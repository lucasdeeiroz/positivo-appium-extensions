*** Settings ***
Documentation    Suite de testes do uso do clique em ponto específico

Library     AppiumLibrary
Library     ./click_a_point.py

*** Test Cases ***
Deve poder fazer a conta 9+5 na calculadora com tap_with_positions
    [Tags]    tap_with_positions
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.calculator
    ...                 appActivity=com.android.calculator2.Calculator
    # ...                 noReset=true


    Tap With Positions    100    ${670, 1350} 
    Tap With Positions    100    ${920, 1900}
    Tap With Positions    100    ${400, 1630}
    
    Sleep    2
    
    Close Application


Deve poder fazer a conta 9+5 na calculadora com point_click
    [Tags]    point_click
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.calculator
    ...                 appActivity=com.android.calculator2.Calculator
    # ...                 noReset=true

    Point Click    ${670}    ${1350}    100
    Point Click    ${920}    ${1900}    100
    Point Click    ${400}    ${1630}    100
 
    Sleep    2
    
    Close Application