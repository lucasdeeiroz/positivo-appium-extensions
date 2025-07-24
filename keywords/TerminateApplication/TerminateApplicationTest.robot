*** Settings ***
Documentation     Executa o app YouTube e o encerra após um timeout definido.
Library           AppiumLibrary
Resource          ./base.resource

*** Test Cases ***
Testar Encerramento do YouTube
    [Tags]    YouTube
    [Documentation]    Testa o encerramento do aplicativo YouTube Utilizando a keyword personalizada TerminateApplicationExtension
    ...                após a sessão de videos curtos "Shorts" e execução de varios swipes .
    [Teardown]    Close Application
    Start Session Youtube
    #Click Text    text=Shorts
    Swipe Loop    10
    ${app_id}=    Get Current App Id
    Log    Encerrando o aplicativo com ID: ${app_id}
    Terminate Application Extension        ${app_id}


Testar Encerramento do TikTok
    [Tags]    TikTok
    [Documentation]    Testa o encerramento do aplicativo TikTok Utilizando a keyword personalizada TerminateApplicationExtension
    ...                após a execução de varios swipes.
    [Teardown]    Close Application
    Start Session TikTok
    Swipe Loop    10
    ${app_id}=    Get Current App Id
    Log    Encerrando o aplicativo com ID: ${app_id}
    Terminate Application Extension        ${app_id}