*** Settings ***
Documentation    Suite de testes do uso do clique em ponto específico

Library     AppiumLibrary

Resource    ./base.resource

*** Test Cases ***
Deve poder fazer um clique no número 5 com point_click
    [Tags]    click
    Start Session Calculator

    ${x}=    Evaluate    410
    ${y}=    Evaluate    1630

    Point Click    ${x}    ${y}    200

    Sleep    2
    Close Session
    

Deve poder fazer um clique no número 5 com tap_with_positions
    [Tags]    tap_click
    Start Session Calculator

    ${x}=    Evaluate    410
    ${y}=    Evaluate    1630
    ${positions}=    Create List    ${x}    ${y}

    Tap With Positions    200    ${positions}

    Sleep    2
    Close Session


Deve poder fazer a conta 9+5 na calculadora com point_click
    [Tags]    addition
    Start Session Calculator

    Point Click    ${670}    ${1350}    100
    Point Click    ${920}    ${1900}    100
    Point Click    ${400}    ${1630}    100
 
    Sleep    2
    
    Close Session


Deve poder fazer a conta 9+5 na calculadora com tap_with_positions
    [Tags]    tap_addition
    Start Session Calculator


    Tap With Positions    100    ${670, 1350} 
    Tap With Positions    100    ${920, 1900}
    Tap With Positions    100    ${400, 1630}
    
    Sleep    2
    
    Close Session


Deve clicar fora da tela com point_click
    [Tags]    outside
    Start Session Calculator

    ${x}=    Evaluate    2000
    ${y}=    Evaluate    4000

    Point Click    ${x}    ${y}    200

    Sleep    2
    Close Session
    

Deve clicar fora da tela com tap_with_positions
    [Tags]    tap_outside
    Start Session Calculator

    ${x}=    Evaluate    2000
    ${y}=    Evaluate    4000
    ${positions}=    Create List    ${x}    ${y}

    Tap With Positions    200    ${positions}

    Sleep    2
    Close Session
