*** Settings ***

Resource    base.resource

*** Test Cases ***
Deve logar com sucesso
    Start session
    Navigate to   Formulários
    Go to Iten    Login    Olá Padawan, vamos testar o login?

    Input Text        id=com.qaxperience.yodapp:id/etEmail        yoda@qax.com
    Input Text        id=com.qaxperience.yodapp:id/etPassword     jedi
    Click Element     id=com.qaxperience.yodapp:id/btnSubmit

    Wait Until Page Contains Element    Boas vindas, logado você está.

    Close session
    