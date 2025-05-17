*** Settings ***
Documentation    Suite de testes do uso do clique em ponto específico

Library     AppiumLibrary
Library     ./click_a_point.py

*** Test Cases ***
Teste de Estresse com Tap With Positions
    [Tags]    stress
    [Timeout]    300
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.calculator
    ...                 appActivity=com.android.calculator2.Calculator
    # ...                 noReset=true

    ${num0}=    Create List    ${150}    ${2170}
    ${dot}=    Create List    ${400}    ${2170}
    ${num1}=    Create List    ${150}    ${1900}
    ${num2}=    Create List    ${400}    ${1900}
    ${num3}=    Create List    ${670}    ${1900}
    ${num4}=    Create List    ${150}    ${1630}
    ${num5}=    Create List    ${400}    ${1630}
    ${num6}=    Create List    ${670}    ${1630}
    ${num7}=    Create List    ${150}    ${1350}
    ${num8}=    Create List    ${400}    ${1350}
    ${num9}=    Create List    ${670}    ${1350}
    ${equals}=    Create List    ${920}    ${2170}
    ${plus}=    Create List    ${920}    ${1900}
    ${minus}=    Create List    ${920}    ${1630}
    ${times}=    Create List    ${920}    ${1350}
    ${division}=    Create List    ${920}    ${1100}
    ${AC}=    Create List    ${150}    ${1100}

    # Criando lista de todos os botões para seleção aleatória
    @{all_numbers}=    Create List
    ...    ${num0}    ${num1}    ${num2}    ${num3}    ${num4}    ${num5}
    ...    ${num6}    ${num7}    ${num8}    ${num9}

    @{all_operations}=    Create List
    ...    ${plus}    ${minus}    ${times}    ${division}

    # Número de iterações para o teste de estresse
    ${repeticoes}=    Set Variable    100
    
    # Loop de estresse
    FOR    ${i}    IN RANGE    1    ${repeticoes}
        # Registra o progresso
        Log    Executando iteração ${i} de ${repeticoes}
        
        # Seleciona 4 botões aleatórios para clicar (fórmula aleatória)
        ${random_number1}=    Evaluate    random.choice($all_numbers)    random
        ${random_operation}=    Evaluate    random.choice($all_operations)    random
        ${random_number2}=    Evaluate    random.choice($all_numbers)    random

        # Clica nos botões aleatórios
        Tap With Positions    50    ${random_number1}
        Tap With Positions    50    ${random_operation}
        Tap With Positions    50    ${random_number2}
        Tap With Positions    50    ${equals}
        
        # Pequena pausa para visualizar o resultado
        Sleep    0.05
        
        # Limpa o resultado
        Tap With Positions    50    ${AC}
        
        # Verifica se o aplicativo ainda está respondendo a cada 10 iterações
        ${mod}=    Evaluate    ${i} % 10
        Run Keyword If    ${mod} == 0    Wait Until Page Contains Element    xpath=//*    timeout=2s
    END
    
    Log    Teste de estresse concluído com sucesso: ${repeticoes} iterações com cliques aleatórios
    Close Application