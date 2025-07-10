*** Settings ***
Library    AppiumLibrary
Library    ../keywords/NetworkStatus.py


Suite Setup       Inicializar Conexao Appium
Suite Teardown    Finalizar Conexao Appium

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${DEVICE_NAME}          Emulator
${UDID}                 emulator-5554

*** Keywords ***
Inicializar Conexao Appium
    Open Application    ${REMOTE_URL}
    ...                 automationName=uiautomator2
    ...                 platformName=${PLATFORM_NAME}
    ...                 deviceName=${DEVICE_NAME}
    ...                 udid=${UDID}
    ...                 noReset=true
    ...                 skipServerInstallation=true
    ...                 skipDeviceInitialization=true
    ...                 newCommandTimeout=300
    Log    Conexão Appium iniciada com sucesso

Finalizar Conexao Appium
    Close Application
    Log    Conexão Appium finalizada com sucesso
    
*** Test Cases ***
# caso de teste mockado com bitmask desconhecido pra testar o retorno UNKNOWN no teste manual
Status Com Apenas Wi-Fi Ativo
    [Tags]    wifi
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    WIFI_ONLY

Status Com Apenas Dados Móveis Ativos
    [Tags]    dados
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    DATA_ONLY

Status Com Wi-Fi E Dados Ativos
    [Tags]    combinado
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    WIFI_AND_DATA

Status Em Modo Avião (com wi-fi e dados desativados)
    [Tags]    aviao
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    AIRPLANE_MODE

Status Sem Conexão Ativa
    [Tags]    nenhum
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    NONE

Status Modo Avião com WI-Fi Ligado
# Mesmo com Wi-Fi e dados ativados, deve retornar AIRPLANE_MODE
    [Tags]    modo_aviao    conflito
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    AIRPLANE_MODE

Status Modo avião com Dados Ligados
# Mesmo com Wi-Fi e dados ativados, deve retornar AIRPLANE_MODE
# não consegui ligar os dados móveis no emulador enquanto o modo avião ta ativado
    [Tags]    modo_aviao    conflito
    ${status}=    Obter Status de Rede Legível
    Log    Status retornado: ${status}
    Should Be Equal    ${status}    AIRPLANE_MODE