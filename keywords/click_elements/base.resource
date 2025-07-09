*** Settings ***

Library     AppiumLibrary
Library     ./ClickElements.py

*** Variables ***

${start}    QAX

*** Keywords ***
Start session Calculator
    Open Application            http://localhost:4723
    ...                         automationName=UIAutomator2
    ...                         platformName=Android
    ...                         DeviceName=Emulator
    ...                         udid=emulator-5554
    ...                         autoGrantPermissions=true
    ...                         appPackage=com.google.android.calculator
    ...                         appActivity=com.android.calculator2.Calculator
    ...                         noReset=true


Get started
    Wait Until Page Contains         ${start}                              7
    Click Text                       ${start}

Close session
    Close Application