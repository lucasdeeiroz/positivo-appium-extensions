*** Settings ***
Documentation     Executa o app YouTube e o encerra após um timeout definido.
Library           AppiumLibrary
Resource          ./base.resource

*** Test Cases ***
Testar Encerramento do YouTube
    Start Session Youtube
    Waiting Time
    Encerrar Aplicativo
    Fechar Sessao
