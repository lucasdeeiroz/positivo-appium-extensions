*** Settings ***

Resource    base_fisico.resource

*** Test Cases ***

Deve encontrar o elemento selecionado
    [Tags]    notes
    Start session Samsung Notes
    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Todas as notas"]
    Click Element    //android.widget.ImageView[@content-desc="Todas as notas"]
    Wait Until Page Contains Element    //android.widget.TextView[@text="Todas as notas"]
    Swipe Into Element    //android.widget.TextView[@resource-id="com.samsung.android.app.notes:id/title" and @text="‎Sol_Ingenieria_Mecanica_ESTATICA_R_C_Hib"]    
    ...    max_swipes=100    direction=up
    Sleep    5
    Swipe Into Element    container_locator=//android.widget.GridView[@resource-id="com.samsung.android.app.notes:id/noteslist_recyclerview"]
    ...    locator=//android.widget.TextView[@resource-id="com.samsung.android.app.notes:id/title" and @text="‎toaz.info-petroleo-e-seus-derivados-marco-antonio-"]
    ...    max_swipes=100    direction=down    swipe_distance_ratio=0.8


Deve encontrar o ano selecionado
    [Tags]    calendario

    Start session Calendario
    Wait Until Page Contains Element    //android.widget.RelativeLayout[@content-desc="Exibição anual, Botão"]
    Click Element    //android.widget.RelativeLayout[@content-desc="Exibição anual, Botão"]
    
    Swipe Into Element    container_locator=com.samsung.android.calendar:id/year_pager
    ...    locator=//android.widget.TextView[@content-desc="2029, Toque duas vezes para alterar o ano."]
    ...    max_swipes=10    direction=left    swipe_distance_ratio=0.8
    
    Swipe Into Element    container_locator=com.samsung.android.calendar:id/year_pager
    ...    locator=//android.widget.TextView[@content-desc="2025, Toque duas vezes para alterar o ano."]
    ...    max_swipes=5    direction=right    swipe_distance_ratio=0.8

