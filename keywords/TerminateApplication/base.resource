*** Settings ***

Library     AppiumLibrary
Library     TerminateApplicationExtension.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     15
${DEVICE_NAME}          emulator-5554
${AUTOMATION_NAME}      UiAutomator2

*** Keywords ***
Start Session Youtube
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    appPackage=com.google.android.youtube
    ...    appActivity=com.google.android.youtube.HomeActivity
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=true