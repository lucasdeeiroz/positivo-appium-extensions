*** Settings ***

Library     AppiumLibrary
# Library     ./ClickAPoint.py
Library     ./click_a_point.py

*** Keywords ***
Start Session Calculator
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.calculator
    ...                 appActivity=com.android.calculator2.Calculator

Close Session
    Close Application