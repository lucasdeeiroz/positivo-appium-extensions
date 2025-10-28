*** Settings ***

Resource    ../../resources/base_change_theme.resource

*** Test Cases ***
Change Theme to Dark via ADB
    [Documentation]    Test change device theme from light to dark using ADB
    [Tags]    theme    dark_theme    adb    fast
    [Setup]    Setup Test Environment
    [Teardown]    Teardown Test Environment
    
   
    ${initial_theme}=    Get Current Theme
    Log    Initial Theme: ${initial_theme}

    Change To Dark Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    
    Verify Theme Change    dark
    
 
    Capture Page Screenshot    dark_theme_applied.png

Change Theme to Light via ADB
    [Documentation]    Test changing device theme from dark to light using ADB
    [Tags]    theme    light_theme    adb    fast
    [Setup]    Setup Test Environment
    [Teardown]    Teardown Test Environment
    
   
    Change To Dark Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    
    ${initial_theme}=    Get Current Theme
    Log    Tema inicial: ${initial_theme}
    
    
    Change To Light Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
 
    Verify Theme Change    light
    
   
    Capture Page Screenshot    light_theme_applied.png

Change Theme to Auto via ADB
    [Documentation]    Tests automatic theme toggling
    [Tags]    theme    toggle    adb    fast
    [Setup]    Setup Test Environment
    [Teardown]    Teardown Test Environment
    
    
    ${initial_theme}=    Get Current Theme
    Log    Initial Theme: ${initial_theme}
    
    
    Toggle Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
  
    ${new_theme}=    Get Current Theme
    Should Not Be Equal As Strings    ${initial_theme}    ${new_theme}
    Log    Change theme from ${initial_theme} for ${new_theme}
    
   
    Toggle Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    
    ${final_theme}=    Get Current Theme
    Should Be Equal As Strings    ${initial_theme}    ${final_theme}
    Log    Theme reverted to initial state: ${final_theme}

Complete Theme Change Test
    [Documentation]    Complete test that verifies all theme functionalities
    [Tags]    theme    complete    adb    regression
    [Setup]    Setup Test Environment
    [Teardown]    Reset Theme To Auto
    
  
    ${initial_theme}=    Get Current Theme
    Log    Initial Theme: ${initial_theme}
    
    
    Change To Dark Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    Verify Theme Change    dark
    Capture Page Screenshot    step2_dark_theme.png
    
    
    Change To Light Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    Verify Theme Change    light
    Capture Page Screenshot    step3_light_theme.png
    
   
    Toggle Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    Verify Theme Change    dark
    Capture Page Screenshot    step4_toggled_to_dark.png
    
   
    Reset Theme To Auto
    Sleep    ${THEME_CHANGE_DELAY}s
    ${final_theme}=    Get Current Theme
    Should Be Equal As Strings    ${final_theme}    auto
    Log    Theme reset to auto
    Capture Page Screenshot    step5_auto_theme.png



   
    
