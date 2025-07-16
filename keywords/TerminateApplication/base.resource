*** Settings ***

Library     AppiumLibrary
# Library     ./TerminateApplication.py
# Library     ./TerminateApplicationV2.py
Library     TerminateApplicationExtension.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     15
${DEVICE_NAME}          emulator-5554
${APP_PACKAGE}          com.google.android.youtube
${APP_ACTIVITY}         com.google.android.youtube.HomeActivity
${TIMEOUT}              5

*** Keywords ***
Start Session Youtube
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    automationName=UiAutomator2

Waiting Time
    Sleep    ${TIMEOUT}

Encerrar Aplicativo
    Terminate Application Extension    ${APP_PACKAGE}

Fechar Sessao
    Close Application
