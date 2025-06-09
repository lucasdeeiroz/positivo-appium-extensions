*** Settings ***
Library           AppiumLibrary

Resource          ../resources/base.resource

*** Test Cases ***
Click Element At Specific Coordinates
    [tags]   android
    Start session
    
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s

    ClickC     xpath=//android.widget.TextView[@content-desc="Camera"]     10    20
    Close session