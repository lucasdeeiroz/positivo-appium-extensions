*** Settings ***
Resource    base_scroll.resource

*** Test Cases ***
Deve realizar swipe no Rgb
    [Tags]    scroll
    Start session Rgb
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@text="RGB Picker de cores"]
    Sleep    5
    Swipe Element
    ...    xpath=//android.widget.SeekBar[@resource-id="henry.rgb.color.picker:id/red_seekbar"]
    ...    direction=right
    ...    percent=0.7
    ...    speed=500
    Sleep    2

