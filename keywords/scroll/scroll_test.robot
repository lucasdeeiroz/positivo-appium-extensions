*** Settings ***
Resource    base_scroll.resource

*** Test Cases ***
Deve realizar scroll down no Google Maps
    [Tags]    scroll
    Start session Google Maps
    Sleep    10
    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Enter compass mode"]
    Sleep    2
    Scroll Down Custom
    Sleep    2

Deve realizar scroll up no Google Maps
    [Tags]    scroll
    Start session Google Maps
    Sleep    10
    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Enter compass mode"]
    Sleep    2
    Scroll Up Custom
    Sleep    2
