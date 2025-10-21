*** Settings ***
Library    AppiumLibrary
Library    Swipe.py

*** Keywords ***
Start session Rgb
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=henry.rgb.color.picker
    ...    appActivity=.MainActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true
Start session Timer
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.digitalchemy.timerplus
    ...    appActivity=com.digitalchemy.timerplus.ui.main.MainActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true