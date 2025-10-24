*** Settings ***
Library    AppiumLibrary
Library    ../src/robotframework_appium_extensions/keywords/SwipeElement.py

*** Variables ***
${rgb_elemento_xpath}    xpath=//android.widget.SeekBar[@resource-id="henry.rgb.color.picker:id/red_seekbar"]
${rgb_elemento_id}   id=henry.rgb.color.picker:id/green_seekbar
${timer_elemento_id}   id=com.digitalchemy.timerplus:id/second_picker

*** Keywords ***
Start session Rgb
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=henry.rgb.color.picker
    ...    appActivity=.MainActivity
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