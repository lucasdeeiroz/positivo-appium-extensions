*** Settings ***

Resource     ../resources/base.resource

*** Test Cases ***

Deve marcar as techs que usam Appium
    Start session
    Get Started
    Navigate to     Check e Radio
    Go to item     Checkbox    Marque as techs que usam Appium
    
    @{techs}    Create List    Ruby    Python    Java    Javascript    C#    Robot Framework
    
    FOR    ${tech}    IN    @{techs}    
        Click Element    xpath=//android.widget.CheckBox[contains(@text, "${tech}")] 
        Sleep    1
    END
    

    Close session