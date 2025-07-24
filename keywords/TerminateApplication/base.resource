*** Settings ***

Library     AppiumLibrary
Library     TerminateApplicationExtension.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     15
${DEVICE_NAME}          H6JVGU5HCY45CIT8
#${DEVICE_NAME}          emulator-5554
${AUTOMATION_NAME}      UiAutomator2

*** Keywords ***
Start Session Youtube
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    appPackage=com.google.android.youtube
    #      For use with xiaomi youtube app uncomment the line below
    ...    appActivity=com.google.android.youtube/.app.honeycomb.Shell$HomeActivity
    #      For use with emulator youtube app uncomment the line below
    # ...  appActivity=com.google.android.youtube.HomeActivity
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=true

Start Session TikTok
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    appPackage=com.zhiliaoapp.musically
    ...    appActivity=com.zhiliaoapp.musically/com.ss.android.ugc.aweme.splash.SplashActivity
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=true