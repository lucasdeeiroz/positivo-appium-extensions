*** Settings ***

Resource    ../../resources/base_perform_zoom.resource

*** Test Cases ***

Zoom on Google Maps using a locator
    [Documentation]    Must perform Zoom on Google Maps application using a locator  
    [Tags]    maps
    Start session Google Maps
    Sleep    10    
    Perform Zoom    locator=xpath=//android.widget.ScrollView 
    Sleep    5

Zoom on Google Maps without a locator

    [Documentation]    Must perform Zoom on Google Maps without receiving a locator
    [Tags]    maps
    Start session Google Maps
    Sleep    10
    Perform Zoom
    Sleep    5


Error message when element doesnt exist or path is invalid
    
    [Documentation]    Should get an error message when element is not visible
    [Tags]    maps
    Start session Google Maps
    Sleep    10
    Perform Zoom    locator=//android.widget.ScrollView
    Sleep    5

Error message when Zoom Scale is invalid

    [Documentation]    Should get an error message when Zoom Scale is invalid
    [Tags]     maps
    Start session Google Maps
    Sleep    10
    Perform Zoom    locator=xpath=//android.widget.ScrollView    scale=0.5
    Sleep    5

Error message when Duration is invalid

    [Documentation]    Should get an error message when Zoom Scale is invalid
    [Tags]     maps
    Start session Google Maps
    Sleep    10
    Perform Zoom    locator=xpath=//android.widget.ScrollView    duration=999999
    Perform Zoom    locator=xpath=//android.widget.ScrollView    duration=99.99
    Sleep    5

