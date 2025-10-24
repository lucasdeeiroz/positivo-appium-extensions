*** Settings ***
Library    AppiumLibrary
Library    ../src/robotframework_appium_extensions/keywords/ScrollInside.py

*** Variables ***
${playStore_elemento_xpath}    xpath=//androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]
${timer_elemento_id}   id=com.digitalchemy.timerplus:id/second_picker

*** Keywords ***
Start session Play Store
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.android.vending
    ...    appActivity=com.android.vending.AssetBrowserActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true 

Start session Timer
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.digitalchemy.timerplus
    ...    appActivity=com.digitalchemy.timerplus.ui.main.MainActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true