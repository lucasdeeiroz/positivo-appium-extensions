*** Settings ***
Library    AppiumLibrary
Library    ../src/robotframework_appium_extensions/keywords/ChangeTheme.py
Library    Collections
Library    BuiltIn

*** Variables ***
${APPIUM_URL}         http://localhost:4723
${PLATFORM_NAME}      Android
${DEVICE_NAME}        XiaomiDevice
${UDID}               a83af8e7
${AUTOMATION_NAME}    UiAutomator2
${APP_PACKAGE}        com.miui.home
${APP_ACTIVITY}       .launcher.Launcher
${THEME_CHANGE_DELAY}   3


*** Keywords ***
Setup Test Environment
    [Documentation]    Configura ambiente de teste inicial
    Open Application  ${APPIUM_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    udid=${UDID}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    noReset=true
    Set Device UDID    ${UDID}
    Sleep    2s
   
Teardown Test Environment
    [Documentation]    Limpa ambiente após teste
    Close Application

Verify Theme Change
    [Documentation]    Verifica se o tema foi alterado corretamente
    [Arguments]    ${expected_theme}
    ${current_theme}=    Get Current Theme
    Should Be Equal As Strings    ${current_theme}    ${expected_theme}
    Log    Tema verificado: ${current_theme}