*** Settings ***
Resource    VisibleElementsResource.robot

Suite Setup       Open Wikipedia App
Suite Teardown    Close Wikipedia App

*** Test Cases ***
# Rodar Keyword
#     Get Visible Elements On Screen    all    debug=True

Retornar todos os elementos visíveis
    [Documentation]    Deve retornar todos os elementos visíveis na tela
    [Tags]    smoke    visible    all 
    # a intenção do smoke teste é validar o fluxo mínimo da aplicação. nesse caso, aceitar um lista vazia pode mascarar algum problema
    # por isso, vamo usar o should not be empty pra garantir que o retorno nao vai ta vazio
    # caso seja possível que o app retorne uma tela sem nenhum elemento com rid, vale usar uma condicional pra não quebrar o pipeline
    ${elements}=    Get Visible Elements On Screen    all    debug=True 
    Should Not Be Empty    ${elements}

Retornar apenas os elementos clicáveis
    [Documentation]    Deve retornar apenas os elementos cujo atributo clickable seja true
    [Tags]    regression    filter    clickable
    ${elements}=    Get Visible Elements On Screen    clickable    debug=True
    FOR    ${el}    IN    @{elements}
        Should Be True    ${el['clickable']}
    END

Retorna apenas elementos com texto visível
    [Documentation]    Deve retornar apenas os elementos cujo atributo "text" não seja vazio
    [Tags]    regression    filter    text
    @{elements}=    Get Visible Elements On Screen    text    debug=True
    FOR    ${el}    IN    @{elements}
        Should Not Be Empty    ${el['text']} 
    END

Retorna apenas Buttons
    [Documentation]    Deve retornar apenas os elementos cuja classe contenha a substring "Button"
    [Tags]    regression    filter    button
    ${elements}=    Get Visible Elements On Screen    button    debug=True
    FOR    ${el}    IN    @{elements}
        Should Contain    ${el['class']}    Button
    END

Retorna apenas elementos de inputs de texto
    [Documentation]    Deve retornar apenas os elementos cuja classe contenha a substring "EditText"
    [Tags]    regression    filter    input
    ${elements}=    Get Visible Elements On Screen    input    debug=True
    FOR    ${el}    IN    @{elements}
        Should Contain    ${el['class']}    EditText
    END

Validação da estrutura do modo debug
    [Documentation]    Valida a estrutura JSON retornada no modo debug, usando o default de filter_type
    [Tags]    debug    exploratory
    ${result}=    Get Visible Elements On Screen    all    debug=True
    FOR    ${el}    IN    @{result}
        Dictionary Should Contain Key    ${el}    resource_id
        Dictionary Should Contain Key    ${el}    accessibility_id
        Dictionary Should Contain Key    ${el}    text
        Dictionary Should Contain Key    ${el}    class
        Dictionary Should Contain Key    ${el}    clickable
    END

Validação de erro gerado por filtro inválido
    [Documentation]    Ao passar um filtro inválido, a keyword deve falhar com mensagem clara
    [Tags]             negative    error    invalid_filter
    Run Keyword And Expect Error    Filter inválido*    
    ...    Get Visible Elements On Screen    foo