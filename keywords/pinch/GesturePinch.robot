*** Settings ***

Resource    GesturePinchResource.robot

*** Test Cases ***

Pinch on Google Maps using a locator
    [Documentation]    Must perform Pinch on Google Maps application using a locator  
    [Tags]    maps
    Start session Google Maps
    Sleep    10    
    Perform Pinch Gesture    locator=xpath=//android.widget.ScrollView 
    Sleep    5

Pinch on Google Maps without a locator

    [Documentation]    Must perform Pinch on Google Maps without receiving a locator
    [Tags]    maps
    Start session Google Maps
    Sleep    10
    Perform Pinch Gesture
    Sleep    5

Error message when element doesnt exist or path is invalid
    
    [Documentation]    Should get an error message when element is not visible
    [Tags]    maps
    Start session Google Maps
    Sleep    10
    Perform Pinch Gesture    locator=//android.widget.ScrollView
    Sleep    5

Error message when Pinch Scale is invalid

    [Documentation]    Should get an error message when Pinch Scale is invalid
    [Tags]     maps
    Start session Google Maps
    Sleep    10
    Perform Pinch Gesture    locator=xpath=//android.widget.ScrollView    scale=1.5
    Sleep    5