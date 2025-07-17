*** Settings ***
Resource    base_scroll.resource

*** Test Cases ***
Deve realizar scroll down no Google Maps
    [Tags]    scroll
    Start session Google Maps
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@resource-id="com.google.android.apps.maps:id/navigation_bar_item_large_label_view"]
    Sleep    5
    Scroll Element
    ...    xpath=//android.widget.FrameLayout[@resource-id="com.google.android.apps.maps:id/home_bottom_sheet_container"]
    ...    direction=left
    ...    percent=0.8
    ...    speed=300
    Sleep    2

Deve realizar scroll down no Timer
    [Tags]    scroll
    Start session Timer
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@text="Timer"]
    Sleep    5
    Scroll Element
    ...    xpath=//android.view.View[@resource-id="com.digitalchemy.timerplus:id/second_picker"]
    ...    direction=down
    ...    percent=0.8
    ...    speed=300
    Sleep    2
