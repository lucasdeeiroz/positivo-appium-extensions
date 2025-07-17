*** Settings ***
Documentation     Executa o app YouTube e o encerra após um timeout definido.
Library           AppiumLibrary
Resource          ./base.resource

*** Test Cases ***
Testar Encerramento do YouTube
    [Documentation]    Testa o encerramento do aplicativo YouTube após a execução de um comando de término.
    [Teardown]    Close Application
    Start Session Youtube
    ${app_id}=    Get Current App Id
    Log    Encerrando o aplicativo com ID: ${app_id}
    Terminate Application Extension        ${app_id}