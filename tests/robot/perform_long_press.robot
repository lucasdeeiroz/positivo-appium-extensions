*** Settings ***

Library     AppiumLibrary

Resource    ../../resources/base_perform_long_press.resource



*** Test Cases ***
Long press test clicking an icon
    [Tags]        start
    
    Start session


    Perform Long Press        xpath=//android.widget.TextView[@content-desc="Gmail"]     8000
    Capture Page Screenshot


 
Long press test with calculator
        [Tags]    calculator

    Start session 1


    Perform Long Press     id=com.google.android.calculator:id/digit_8     8000
    Capture Page Screenshot


    Close session

Long press test
    [Tags]                      long

    Start session 2
    Get started
    Navigate to                 Button Clicks
    Go to item                  Long Click                               Long Click Button

    Perform Long Press                     id=com.qaxperience.yodapp:id/long_click    

    Wait Until Page Contains    This is a long click
    Capture Page Screenshot

    Close session
Non-existent button should not be present
    [Tags]    expected_error
    Start session 
    Element Should Be Visible    xpath=//android.widget.Button[@text="Non-existent"]
    Capture Page Screenshot

    Close session

YouTube app should not be present on home screen
    [Tags]        missing_element   
    Start session 
    Page Should Not Contain Element   xpath=//android.widget.TextView[@content-desc="YouTube"]
    Close session

    
Expected error when using LongP on missing element
    [Tags]    error1_expected    Start session 2

    ${error}=    Set Variable    No error

    TRY
        Perform Long Press    id=non_existent_button    8000
    EXCEPT    ${error}
        ${error_line}=    Evaluate    str($error).splitlines()[0]
        Log    ${error_line}
    END

    Capture Page Screenshot
    Close session



Expected error when using LongP with invalid locator
    [Tags]    error2_expected
    Start session 

    Run Keyword And Expect Error     Invalid locator syntax
    ...    Perform Long Press    invalid-locator    8000

    Capture Page Screenshot
    Close session

Expected error when using LongP without duration
    [Tags]    error3_expected
    Start session 

    Run Keyword And Expect Error     Missing required argument 'duration'
    ...    Perform Long Press    id=com.qaxperience.yodapp:id/long_click

    Capture Page Screenshot
    Close session

Expected error when using LongP on unsupported element
    [Tags]    error4_expected
    Start session 

    Run Keyword And Expect Error     Element does not support long press
    ...    Perform Long Press    id=com.qaxperience.yodapp:id/unsupported_element    8000

    Capture Page Screenshot
    Close session
