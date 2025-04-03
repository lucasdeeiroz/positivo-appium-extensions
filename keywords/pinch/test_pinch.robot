*** Settings ***
Documentation    Suite de testes do uso do pinch no Google Maps

Library     keywords/pinch/pinch.py

*** Test Cases ***
Deve poder fazer gesto de pinça
    Start session
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.apps.maps
    ...                 appActivity=com.google.android.maps.MapsActivity

    Perform Pinch Gesture    xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]
    Sleep    5

    Close Application