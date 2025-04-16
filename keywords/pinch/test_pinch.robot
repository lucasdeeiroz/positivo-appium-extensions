*** Settings ***
Documentation    Suite de testes do uso do pinch no Google Maps

Library     AppiumLibrary
Library     ../pinch/pinch.py

*** Test Cases ***
Deve poder dar zoom out no Google Maps usando pinch verticalmente
    [Tags]    vertical
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

Deve poder dar zoom out no Google Maps usando pinch horizontalmente
    [Tags]    horizontal
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.apps.maps
    ...                 appActivity=com.google.android.maps.MapsActivity

    Perform Pinch Gesture    locator=xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    scale=0.5    duration=200   direction=horizontal
    Sleep    5

    Close Application

Deve falhar ao usar direção inválida
    [Tags]    error
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.apps.maps
    ...                 appActivity=com.google.android.maps.MapsActivity

    Run Keyword And Expect Error    ValueError    Perform Pinch Gesture    locator=xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    scale=0.5    duration=100    direction=diagonal
    Close Application