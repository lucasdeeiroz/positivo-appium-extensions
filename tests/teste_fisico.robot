*** Settings ***

Resource     ../resources/base_fisico.resource
*** Variables ***

${SCREENSHOT_FOLDER}    ./screenshots
${DURATION}      500
*** Test Cases ***

Deve executar pinch no Google Maps
    [Tags]    pinch
    Start session Google Maps
    Sleep    10

    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    # --- Pinch ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    Perform Pinch Gesture    scale=0.5    duration=500     locator=id=com.google.android.apps.maps:id/mainmap_container    #direction=horizontal
    # ------------
    Sleep    5
    Close Application

Deve dar zoom no Google Maps 1.5
    [Tags]    maps2
    Start session Google Maps
    Sleep    10

    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Sleep    2
    # --- Pinch ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    #Perform Pinch Gesture    scale=0.5    duration=500     locator=id=com.google.android.apps.maps:id/mainmap_container    #direction=horizontal
    # ------------

    # --- Zoom com estratégia de direção vertical e horizontal ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    #Perform Zoom_2    id=com.google.android.apps.maps:id/mainmap_container    scale=1.5    duration=${DURATION}
    #--------------------------------------------------------------


    # --- Zoom com estratégia de pertubação de movimento ---   
    # Observação: Pertubação obtém resultados consistentes para a mesma configuração
    #             Resultados mais consistentes e fator de scale responsivo.              
    Perform Zoom_4    id=com.google.android.apps.maps:id/mainmap_container    scale=1.5    duration=${DURATION}    steps=50    direction=horizontal
    #------------------------------------------------------- 
    
    # --- Zoom com estratégia de offset ---
    #Zoom in_2   locator=id=com.google.android.apps.maps:id/mainmap_container     initial_offset=50    final_offset=400    pause_s=1    duration_ms=1000   
    #Observação:  Dependência de duração para execução (semelhante estratégia com scale). 
    #             Resultados inconsistentes para a mesma configuração
    #--------------------------------------

    Sleep    5
    
    # Obtém timestamp seguro para nome de arquivo
    ${timestamp}=    Get Time    epoch
    ${safe_name}=    Set Variable    pert_scale1.5_after_zoom_${timestamp}
    
    # Garante que o diretório existe
    Create Directory    ${OUTPUT_DIR}${/}screenshots${/}maps${/}pert_scale1.5
    
    # Captura o screenshot com caminho absoluto
    Capture Page Screenshot    ${OUTPUT_DIR}${/}screenshots${/}maps${/}pert_scale1.5${/}${safe_name}.png
    
    Close Application

Deve dar zoom no Google Maps 1.7
    [Tags]    maps2
    Start session Google Maps
    Sleep    10

    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Sleep    2
    # --- Pinch ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    #Perform Pinch Gesture    scale=0.7    duration=500     locator=id=com.google.android.apps.maps:id/mainmap_container    #direction=horizontal
    # ------------

    # --- Zoom com estratégia de direção vertical e horizontal ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    #Perform Zoom_2    id=com.google.android.apps.maps:id/mainmap_container    scale=1.7    duration=${DURATION}
    #--------------------------------------------------------------


    # --- Zoom com estratégia de pertubação de movimento ---   
    # Observação: Pertubação obtém resultados consistentes para a mesma configuração
    #             Resultados mais consistentes e fator de scale responsivo.              
    Perform Zoom_4    id=com.google.android.apps.maps:id/mainmap_container    scale=1.7    duration=${DURATION}    steps=50     direction=horizontal 
    #------------------------------------------------------- 
    
    # --- Zoom com estratégia de offset ---
    #Zoom in_2   locator=id=com.google.android.apps.maps:id/mainmap_container     initial_offset=50    final_offset=400    pause_s=1    duration_ms=1000   
    #Observação:  Dependência de duração para execução (semelhante estratégia com scale). 
    #             Resultados inconsistentes para a mesma configuração
    #--------------------------------------

    Sleep    5
    
    # Obtém timestamp seguro para nome de arquivo
    ${timestamp}=    Get Time    epoch
    ${safe_name}=    Set Variable    pert_scale1.7_after_zoom_${timestamp}
    
    # Garante que o diretório existe
    Create Directory    ${OUTPUT_DIR}${/}screenshots${/}maps${/}pert_scale1.7
    
    # Captura o screenshot com caminho absoluto
    Capture Page Screenshot    ${OUTPUT_DIR}${/}screenshots${/}maps${/}pert_scale1.7${/}${safe_name}.png
    
    Close Application

Deve dar zoom no Google Maps 1.1
    [Tags]    maps2
    Start session Google Maps
    Sleep    10

    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Sleep    2
    # --- Pinch ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    #Perform Pinch Gesture    scale=0.1    duration=500     locator=id=com.google.android.apps.maps:id/mainmap_container    #direction=horizontal
    # ------------

    # --- Zoom com estratégia de direção vertical e horizontal ---
    # Observação: Problemas com o scale e dependência de duração para execução. 
    #             Resultados inconsistentes para a mesma configuração

    #Perform Zoom_2    id=com.google.android.apps.maps:id/mainmap_container    scale=1.1    duration=${DURATION}
    #--------------------------------------------------------------


    # --- Zoom com estratégia de pertubação de movimento ---   
    # Observação: Pertubação obtém resultados consistentes para a mesma configuração
    #             Resultados mais consistentes e fator de scale responsivo.              
    Perform Zoom_4    id=com.google.android.apps.maps:id/mainmap_container    scale=1.1    duration=100    steps=20      direction=horizontal
    #------------------------------------------------------- 
    
    # --- Zoom com estratégia de offset ---
    #Zoom in_2   locator=id=com.google.android.apps.maps:id/mainmap_container     initial_offset=50    final_offset=400    pause_s=1    duration_ms=1000   
    #Observação:  Dependência de duração para execução (semelhante estratégia com scale). 
    #             Resultados inconsistentes para a mesma configuração
    #--------------------------------------

    Sleep    5
    
    # Obtém timestamp seguro para nome de arquivo
    ${timestamp}=    Get Time    epoch
    ${safe_name}=    Set Variable    pert_scale1.1_after_zoom_${timestamp}
    
    # Garante que o diretório existe
    Create Directory    ${OUTPUT_DIR}${/}screenshots${/}maps${/}pert_scale1.1
    
    # Captura o screenshot com caminho absoluto
    Capture Page Screenshot    ${OUTPUT_DIR}${/}screenshots${/}maps${/}pert_scale1.1${/}${safe_name}.png
    
    Close Application


#--------------------------------------------------------------------------------------------------------------


Deve realizar um Zoom no Google Fotos 1.5
    [Tags]    fotos2

    Start session Google Photos
    Wait Until Page Contains Element      //*[contains(@text, "Use o backup do Google Fotos")]
    Click Element     //android.widget.Switch[@resource-id="com.google.android.apps.photos:id/onboarding_toggle"]

    Wait Until Page Contains Element   //*[contains(@text, "Continuar sem fazer backup")]
    Click Element    //*[contains(@text, "Continuar sem fazer backup")]

    Wait Until Page Contains Element      //android.widget.ImageView[@content-desc="Item Foto criado em 21 de set. de 2024 11:04"]        timeout=200
    Click Element    //android.widget.ImageView[@content-desc="Item Foto criado em 21 de set. de 2024 11:04"]

    Sleep    10
    #Perform Zoom_4    id=com.google.android.apps.photos:id/photos_photofragment_components_background_photo_view    scale=1.5
    Perform Zoom_2    id=com.google.android.apps.photos:id/photos_photofragment_components_background_photo_view    scale=1.5    

    # Obtém timestamp seguro para nome de arquivo
    ${timestamp}=    Get Time    epoch
    ${safe_name}=    Set Variable    pert_scale1.5_after_zoom_${timestamp}
    
    # Garante que o diretório existe
    Create Directory    ${OUTPUT_DIR}${/}screenshots${/}fotos${/}pert_scale1.5
    
    # Captura o screenshot com caminho absoluto
    Capture Page Screenshot    ${OUTPUT_DIR}${/}screenshots${/}fotos${/}pert_scale1.5${/}${safe_name}.png
    
    
    Sleep     5

    Close Application

Deve realizar um Zoom no Google Fotos 1.7
    [Tags]    fotos

    Start session Google Photos
    Wait Until Page Contains Element      //*[contains(@text, "Use o backup do Google Fotos")]
    Click Element     //android.widget.Switch[@resource-id="com.google.android.apps.photos:id/onboarding_toggle"]

    Wait Until Page Contains Element   //*[contains(@text, "Continuar sem fazer backup")]
    Click Element    //*[contains(@text, "Continuar sem fazer backup")]

    Wait Until Page Contains Element      //android.widget.ImageView[@content-desc="Item Foto criado em 21 de set. de 2024 11:04"]        timeout=200
    Click Element    //android.widget.ImageView[@content-desc="Item Foto criado em 21 de set. de 2024 11:04"]

    Sleep    10
    Perform Zoom_4    id=com.google.android.apps.photos:id/photos_photofragment_components_background_photo_view    scale=1.7
    
    # Obtém timestamp seguro para nome de arquivo
    ${timestamp}=    Get Time    epoch
    ${safe_name}=    Set Variable    pert_scale1.7_after_zoom_${timestamp}
    
    # Garante que o diretório existe
    Create Directory    ${OUTPUT_DIR}${/}screenshots${/}fotos${/}pert_scale1.7
    
    # Captura o screenshot com caminho absoluto
    Capture Page Screenshot    ${OUTPUT_DIR}${/}screenshots${/}fotos${/}pert_scale1.7${/}${safe_name}.png
    
    
    Sleep     5

    Close Application

Deve realizar um Zoom no Google Fotos 1.1
    [Tags]    fotos

    Start session Google Photos
    Wait Until Page Contains Element      //*[contains(@text, "Use o backup do Google Fotos")]
    Click Element     //android.widget.Switch[@resource-id="com.google.android.apps.photos:id/onboarding_toggle"]

    Wait Until Page Contains Element   //*[contains(@text, "Continuar sem fazer backup")]
    Click Element    //*[contains(@text, "Continuar sem fazer backup")]

    Wait Until Page Contains Element      //android.widget.ImageView[@content-desc="Item Foto criado em 21 de set. de 2024 11:04"]        timeout=200
    Click Element    //android.widget.ImageView[@content-desc="Item Foto criado em 21 de set. de 2024 11:04"]

    Sleep    10
    Perform Zoom_4    id=com.google.android.apps.photos:id/photos_photofragment_components_background_photo_view    scale=1.1
    
    # Obtém timestamp seguro para nome de arquivo
    ${timestamp}=    Get Time    epoch
    ${safe_name}=    Set Variable    pert_scale1.1_after_zoom_${timestamp}
    
    # Garante que o diretório existe
    Create Directory    ${OUTPUT_DIR}${/}screenshots${/}fotos${/}pert_scale1.1
    
    # Captura o screenshot com caminho absoluto
    Capture Page Screenshot    ${OUTPUT_DIR}${/}screenshots${/}fotos${/}pert_scale1.1${/}${safe_name}.png
    
    
    Sleep     5

    Close Application

Deve realizar um Zoom e Pinch no Google Maps

    Start session Google Maps
    Sleep    10

    Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Sleep    2

    Perform Zoom_4    id=com.google.android.apps.maps:id/mainmap_container    scale=1.5    duration=${DURATION}    steps=50    direction=horizontal
    Sleep    5
    Perform Pinch_4   id=com.google.android.apps.maps:id/mainmap_container    scale=1.5    duration=${DURATION}    steps=50    direction=horizontal
    Sleep    5     