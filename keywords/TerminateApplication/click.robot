*** Settings ***

Resource    base.resource

*** Test Cases ***

# {
#   "platformName": "Android",
#   "appium:deviceName": "Android Emulator",
#   "appium:automationName": "UIAutomator2",
#   "appium:app": "C:\\Residencia36\\QAx\\projects\\yodaapp\\app\\yodapp-beta.apk",
#   "appium:udid": "emulator-5554",
#   "autoGrantPermissions": true
# }


Deve realizar um clique simples
    Start session
    Get started
    Navigate to    Clique em Botões
    Go to Iten    Clique simples    Botão clique simples

    Click Text    CLIQUE SIMPLES
    Wait Until Page Contains    Isso é um clique simples

    Close session

Deve realizar um clique longo
    [Tags]    long
    Start session
    Get started
    Navigate to    Clique em Botões
    Go to Iten    Clique longo    Botão clique longo
    
    ${locator}    Set Variable    id=com.qaxperience.yodapp:id/long_click

    ${positions}    Get Element Location    ${locator}

    Long Press    com.qaxperience.yodapp:id/long_click
    #Keyword Long Press Depreciada, não funciona mais.
    Tap With Positions            1000    ${${positions}[x], ${positions}[y]}
    Wait Until Page Contains      Isso é um clique longo

    Close session



