# Compare Screenshots — AppiumLibrary Extension

`Compare Screenshots` is a custom keyword designed to compare two saved screenshots during automated tests with Appium and Robot Framework. It uses OpenCV to detect and quantify visual differences between two images based on pixel-by-pixel comparison.

## Purpose
- Compare two existing image files for visual differences
- Provide flexible comparison modes (equal or different)
- Support automatic image size adjustment
- Offer configurable tolerance levels
- Provide detailed feedback on comparison results

## How It Works
The keyword performs a comprehensive image comparison:

1. Input Validation
   - Verifies file paths exist and are accessible
   - Validates tolerance is between 0.0 and 1.0
   - Confirms expected mode is 'equal' or 'different'

2. Image Processing
   - Loads both images using OpenCV
   - Automatically resizes if dimensions differ
   - Converts to grayscale for comparison

3. Difference Analysis
   - Calculates pixel-by-pixel differences
   - Computes overall difference percentage
   - Compares against tolerance threshold

4. Result Determination
   - In 'equal' mode: passes if difference ≤ tolerance
   - In 'different' mode: passes if difference > tolerance
   - Provides detailed logging of results

## Parameters
| Parameter  | Type    | Required | Default | Description |
|------------|---------|----------|---------|-------------|
| img1       | string  | Yes      | -       | Full path to the first image file to compare |
| img2       | string  | Yes      | -       | Full path to the second image file to compare |
| expected   | string  | No       | "equal" | Comparison mode: "equal" or "different". In "equal" mode, passes if images are similar within tolerance. In "different" mode, passes if images differ more than tolerance |
| tolerance  | float   | No       | 0.1     | Maximum allowed difference ratio between images, from 0.0 to 1.0 (0% to 100%). Default 0.1 means 10% difference tolerance |

## Validation Modes

### Equal Mode (`expected="equal"`)
- PASS: difference ≤ tolerance
- FAIL: difference > tolerance

### Different Mode (`expected="different"`)
- PASS: difference > tolerance
- FAIL: difference ≤ tolerance

## Tolerance Explained
- Tolerance is a float between 0 and 1 (0% to 100%)
- Represents maximum allowed pixel difference ratio
- Default is 0.1 (10%)
- Example:
  - If tolerance = 0.05 (5%)
  - And difference = 3%
  - Then PASS in 'equal' mode, FAIL in 'different' mode

## How To Execute
Example in `.robot`:
```robotframework
*** Settings ***
Library    AppiumLibrary
Library    robotframework_appium_extensions.CompareScreenshots

*** Test Cases ***
Compare Two Screenshots
    # Compare two images expecting them to be equal (within 10% difference)
    Compare Screenshots    path/to/first.png    path/to/second.png    expected=equal    tolerance=0.1
    
    # Compare two images expecting them to be different (more than 20% difference)
    Compare Screenshots    path/to/first.png    path/to/modified.png    expected=different    tolerance=0.2
```

## Requirements
This keyword requires additional dependencies:
- `opencv-python-headless>=4.8.0`
- `numpy>=1.26.0`

Install them with pip:
```bash
pip install opencv-python-headless numpy
```

If these libraries are not installed, the image comparison keyword will not work and may raise an ImportError.

## Technical Details
- Uses OpenCV (cv2) for image processing and comparison
- Automatically resizes images if dimensions don't match
- Validates all inputs before processing:
  - File existence
  - Valid image formats
  - Numeric tolerance between 0 and 1
  - Valid 'expected' values ('equal' or 'different')
- Provides detailed error messages and logging
- Shows difference percentage in logs

## Error Handling
The keyword will raise:
- `ValueError` for:
  - Invalid file paths
  - Corrupt or invalid image formats
  - Invalid tolerance values
  - Invalid 'expected' values
- `AssertionError` when:
  - Images are too different (in 'equal' mode)
  - Images are too similar (in 'different' mode)

## Test Considerations
- Always use full paths to image files
- Consider image resolution and size
- Test with various tolerance levels
- Validate both equality and difference cases
- Check logs for exact difference percentages
