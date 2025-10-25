# Changelog

All notable changes to this project will be documented in this file.

---

## [0.1.0] - 2025-10-XX

### Overview

This release represents the **preview version** of the project, focused on refactoring deprecated Appium keywords within Robot Framework and introducing new functionalities to expand Android automation capabilities.

All keywords were validated on both **physical devices** and **Android emulators**, ensuring consistency, reliability, and performance stability.

---

### Added

####  System and Application Control

- **Change Theme** — Automates switching between light and dark modes on Android systems, enabling UI validation under different themes.  
- **Terminate Application Extension** — Gracefully terminates the target app, ensuring a clean environment for subsequent tests.

####  Interaction and Gestures

- **Click Elements** — Executes tap actions based on locators, improving flexibility in element interaction.  
- **Tap at Percentage** — Performs tap actions at specific screen coordinates defined as percentages, useful for dynamic layouts.  
- **Perform Long Press** — Simulates long-press gestures on elements or coordinates.  
- **Swipe Element** — Executes swipe gestures in any direction with configurable distance and duration.  
- **Scroll Inside** — Enables controlled vertical scrolling across the screen.  
- **Scroll to Element** — Scrolls until the specified element becomes visible.  
- **Perform Pinch** — Performs a two-finger pinch gesture for zoom-out interactions.  
- **Perform Zoom** — Executes a multi-touch zoom-in gesture for enlarging content.

####  Validation and State Inspection

- **Compare Screenshots** — Compares two screenshots pixel by pixel to verify visual consistency.  
- **Get Visible Elements on Screen** — Returns a list of all currently visible UI elements, assisting in coverage analysis.  
- **Get Readable Network Status** — Retrieves the active network state (Wi-Fi, mobile data, or offline mode).

####  Synchronization and Reliability

- **Wait Multiple Elements** — Waits for multiple elements to appear simultaneously, improving synchronization and reducing test delays.

---

### Documentation

- Added a complete **user guide** with syntax, arguments, and practical examples for each keyword.  
- Structured **repository layout** including scripts, resources, and automated test suites.  
- Added **contribution guidelines** to support open collaboration.  
- Included **CHANGELOG**, **README**, and **usage manual** following Robot Framework conventions.

---

### Validation

- All keywords were validated on **physical Android devices** and **emulators**.  
- Functional tests confirmed stability, performance, and full integration with Robot Framework’s Appium library.

---

[0.1.0]: https://github.com/restic36/robotframework-appium-extensions/releases/tag/v0.1.0
