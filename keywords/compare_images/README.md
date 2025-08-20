# Screenshot Comparison — AppiumLibrary Extension

`Capturar Screenshot Inicial Como` and `Comparar Screenshot Final Com` are custom keywords designed to capture and compare screenshots during automated tests with Appium and Robot Framework.
They use OpenCV and SSIM (Structural Similarity Index) to detect visual differences between a reference image and the current app screen.

## Purpose
- Capture a baseline screenshot for later comparison.
- Compare the current screen against a reference image to detect UI changes.
- Quantify differences using the SSIM metric.
- Automatically generate a visual diff image highlighting changes.
- Fail tests when differences exceed an allowed tolerance.

## How It Works
### 1️⃣ Capturar Screenshot Inicial Como
Saves the current device screen as the reference screenshot.
- Creates the screenshot folder if it doesn’t exist.
- File is saved in the specified path with the given filename.

### 2️⃣ Comparar Screenshot Final Com
Captures the current screen as the final screenshot.
- Loads both the reference image and the final image.
- Converts them to grayscale and calculates SSIM similarity.
- Generates and saves a diff image showing pixel differences.
- If the percentage difference exceeds the tolerance, the test fails.

## Parameters
| Keyword                        | Parameter           | Description                                 |
|--------------------------------|---------------------|---------------------------------------------|
| Capturar Screenshot Inicial Como | nome_arquivo        | Filename for the reference screenshot.      |
|                                | caminho (optional)  | Folder path (default: screenshots).         |
| Comparar Screenshot Final Com   | arquivo_referencia  | Path to the reference screenshot.           |
|                                | tolerancia (optional)| Max allowed difference (default: 0.01 = 1%).|
|                                | caminho (optional)  | Folder for saving screenshots and diff image.|

## Tolerance & SSIM
- SSIM ranges from 0 (completely different) to 1 (identical).
- `percentual_diferenca = 1 - score` is used to calculate the visual difference.
- If `percentual_diferenca > tolerancia`, the keyword raises an AssertionError.

**Example:**
- If similarity is 0.9750, then `percentual_diferenca = 0.025` → 2.5% difference.
- If tolerance is 1%, the comparison fails.

## How To Execute
Example in `.robot`:
```robotframework
*** Settings ***
Library    AppiumLibrary
Library    ScreenshotComparisonKeywords.py

*** Test Cases ***
Capture And Compare Screens
		Open Application    http://localhost:4723/wd/hub    platformName=Android    deviceName=emulator-5554    appPackage=com.example    appActivity=.MainActivity
    
		# Capture reference
		Capturar Screenshot Inicial Como    baseline.png
    
		# Perform some UI action...
    
		# Compare with tolerance of 2%
		Comparar Screenshot Final Com    screenshots/baseline.png    tolerancia=0.02
```

Run with:
```shell
robot ScreenshotComparison.robot
```

## Technical Details
- Uses cv2 (OpenCV) for image processing.
- Uses skimage.metrics.ssim for structural similarity measurement.
- Automatically creates directories for saving screenshots.
- Saves a visual diff file (`diff.png`) for debugging.
- Validates:
	- File existence
	- Successful image loading
	- Matching image dimensions

## Test Structure
- **Mocked Tests**
	- Compare identical images → pass.
	- Compare slightly different images within tolerance → pass.
	- Compare different-sized images → fail.
	- Compare different images beyond tolerance → fail.
- **Emulator Tests**
	- Capture baseline after app load.
	- Compare after UI changes (e.g., zoom, scroll).
	- Validate detection of small layout changes.
- **Physical Device Tests (Pending)**
	- Not yet validated on real devices, but works with any Appium-supported platform.

---

If you want, I can also make a visual report template for this keyword showing:

- Reference image
- Final image
- Diff image side by side
