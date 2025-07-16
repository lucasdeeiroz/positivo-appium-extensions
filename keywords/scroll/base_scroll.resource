*** Settings ***
Library    AppiumLibrary
Library    scroll_down.py
Library    scroll_up.py

*** Keywords ***
Start session Google Maps
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.maps
    ...    appActivity=com.google.android.maps.MapsActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true

Start session Google Earth
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.earth
    ...    appActivity=com.google.android.apps.earth.flutter.EarthFlutterActivity
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

Start session Calculadora
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.calculator
    ...    appActivity=com.android.calculator2.Calculator
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true
