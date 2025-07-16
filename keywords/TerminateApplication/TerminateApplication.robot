*** Settings ***
Documentation     Executa o app YouTube e o termina após 5 segundos.
Library           AppiumLibrary
Resource          ./base.resource

*** Test Cases ***
Testar Encerramento do YouTube
    Conectar Ao Emulador
    Abrir Aplicativo YouTube
    Esperar 5 Segundos
    Encerrar Aplicativo
    Fechar Sessao
