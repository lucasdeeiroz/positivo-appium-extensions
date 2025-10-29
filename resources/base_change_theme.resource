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
    [Documentation]    Configure environment before test execution
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
    [Documentation]    Clean up after test execution
    Close Application

Verify Theme Change
    [Documentation]    Verify if the current theme matches the expected theme
    [Arguments]    ${expected_theme}
    ${current_theme}=    Get Current Theme
    Should Be Equal As Strings    ${current_theme}    ${expected_theme}
    Log    Tema verificado: ${current_theme}