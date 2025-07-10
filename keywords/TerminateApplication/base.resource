*** Settings ***

Library    AppiumLibrary

*** Variables ***
${START}    QAX


*** Keywords ***
 
Start session
    Open Application    http://localhost:4723
    ...                 platformName=Android
    ...                 deviceName=Android Emulator
    ...                 automationName=UIAutomator2
    ...                 app=${EXECDIR}/TerminateApplication/app/yodapp-beta.apk
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    
Get started
    Wait Until Page Contains    ${START}    100
    Click Text                  ${START}

Navigate to
    [Arguments]    ${item_text}
    ${hamburguer}    Set Variable    //android.widget.ImageButton[@content-desc="Open navigation drawer"]
    Wait Until Element Is Visible    ${hamburguer}    10
    Click Element    ${hamburguer}

    ${menu_item}    Set Variable    //*[@resource-id="com.qaxperience.yodapp:id/navView"]//*[@text="${item_text}"]
    Wait Until Element Is Visible    ${menu_item}    5
    Click Element    ${menu_item}

Go to Iten
    [Arguments]    ${item}    ${checkpoint}
    Wait Until Page Contains    ${item}    10
    Click Text                  ${item}
    Wait Until Page Contains    ${checkpoint}   5

Close session
    Terminate Application    app_id=com.qaxperience.yodapp
    Close Application