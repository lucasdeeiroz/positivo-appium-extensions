*** Settings ***
Library    AppiumLibrary
Library    ./ThemeChanger.py

*** Variables ***
${APPIUM_URL}         http://localhost:4723
${PLATFORM_NAME}      Android
${DEVICE_NAME}        XiaomiDevice
${UDID}               a83af8e7
${AUTOMATION_NAME}    UiAutomator2
${APP_PACKAGE}        com.miui.home
${APP_ACTIVITY}       .launcher.Launcher

*** Test Cases ***
Muda Tema Para Escuro em "Configurações" na Tela Inicial
    [Documentation]    Testa a mudança do tema do dispositivo de claro para escuro
    [Tags]    theme    dark_theme    ui_automation

    # Abre a tela inicial
    Open Application  ${APPIUM_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    udid=${UDID}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    noReset=true

    Sleep    2s

    # Chama keyword que agora abre "com.android.settings" internamente
    Change To Dark Theme    timeout=45

    Sleep    2s
    Log    Tema escuro aplicado com sucesso
    Close Application

Muda Tema Para Claro em "Configurações" na Tela Inicial
    [Documentation]    Testa a mudança do tema do dispositivo de escuro para claro
    [Tags]    theme    light_theme    ui_automation

    Open Application  ${APPIUM_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    udid=${UDID}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    noReset=true

    Sleep    2s
    Change To Light Theme    timeout=45
    Sleep    2s
    Log    Tema claro aplicado com sucesso
    Close Application

Teste Completo de Alternância de Temas
    [Documentation]    Testa a alternância completa entre temas claro e escuro
    [Tags]    theme    full_test    ui_automation

    Open Application  ${APPIUM_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    udid=${UDID}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    noReset=true

    Sleep    2s
    Log    Iniciando mudança para tema escuro...
    Change To Dark Theme    timeout=45
    Sleep    3s

    Log    Iniciando mudança para tema claro...
    Change To Light Theme    timeout=45
    Sleep    3s

    Log    Teste de alternância de temas concluído com sucesso
    Close Application


