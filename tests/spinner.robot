*** Settings ***

Resource     ../resources/base.resource

*** Test Cases ***

Deve escolher o nível Jedi
    
    Start session
    Get Started
    
    Navigate to    Formulários
    Go to item    Cadastro    Crie sua conta.

    Select level    Jedi

    Close session

*** Keywords ***
Select level
    [Arguments]    ${level}
    
    Click Element    id=com.qaxperience.yodapp:id/spinnerJob
    Wait Until Element Is Visible    class=android.widget.ListView
    Click Text    ${level}