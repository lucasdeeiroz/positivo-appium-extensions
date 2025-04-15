*** Settings ***

Resource     ../resources/base.resource

*** Keywords ***
Handle Backup Prompt If Visible
    
    Sleep    5
    ${backup_prompt_visible}    Run Keyword And Return Status
    ...    Wait Until Page Contains Element    //*[contains(@text, "Get started")]    5s
    
    Run Keyword If    ${backup_prompt_visible}    Process Backup Prompt

Process Backup Prompt
    Click Element    //android.widget.Switch[@resource-id="com.google.android.apps.photos:id/onboarding_toggle"]
    Wait Until Page Contains Element    //*[contains(@text, "Continue without backup")]    5s
    Click Element    //*[contains(@text, "Continue without backup")]
    Sleep    2s    

*** Test Cases ***

Deve realizar um zoom no Google Maps
    [Tags]    maps    
    Start session Google Maps

    Sleep    15
    Capture Page Screenshot    before_zoom.png
    Verified Zoom On Element    id=com.google.android.apps.maps:id/mainmap_container    scale=1.5    duration_ms=100    pause_s=0.5    
    Sleep    15
    Capture Page Screenshot    after_zoom.png
    

    Close session

Deve realizar um zoom em uma foto no Google Fotos
    [Tags]    zoom
    
    Start session Google Photos
    Handle Backup Prompt If Visible
    
    Wait Until Page Contains Element    //*[contains(@text, "Collections")]
    Click Element    //*[contains(@text, "Collections")]

    Wait Until Page Contains Element    //android.widget.TextView[@text="Screenshots"]
    Click Element    //android.widget.TextView[@text="Screenshots"]

    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Photo taken on Mar 31, 2025 2:10 AM"]
    Click Element    //android.widget.ImanpgeView[@content-desc="Photo taken on Mar 31, 2025 2:10 AM"]

    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Edit"]

    Sleep    5
    Capture Page Screenshot
    Zoom On Element    id=com.google.android.apps.photos:id/touch_capture_view    scale=2.5    duration_ms=500    pause_s=0.5
    Sleep    5
    Capture Page Screenshot
    
    Close session

Deve realizar um zoom no aplicativo da Camera
    [Tags]    camera

    Start session Camera
    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Options"]
    
    Sleep    5
    Capture Page Screenshot
    Zoom In Center
    Sleep    5
    Capture Page Screenshot

    Close session

#Deve realizar um zoom no Youtube
    #[Tags]    youtube

    #Start session Youtube
    #Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Search"]

    #Click Element    //android.widget.ImageView[@content-desc="Search"]

    #Input Text Into Current Element    Teste de Software

    #Wait Until Page Contains Element    //*[contains(@text, "Videos")]
    #Click Element    //*[contains(@text, "Videos")]

    #Click Element    //android.view.ViewGroup[@content-desc="Entenda os 7 princípios do Teste de Software que todo engenheiro de software deve saber - 12 minutes, 31 seconds - Go to channel - pessonizando - 27K views - 4 years ago - play video"]/android.widget.ImageView[2]
    