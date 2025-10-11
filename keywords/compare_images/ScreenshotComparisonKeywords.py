import cv2
import numpy as np
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn


class ScreenshotComparisonKeywords:

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword("Compare Screenshots")
    def compare_images(self, img1, img2, expected="Equal", tolerance=0.1):
        """
        Compares two saved images and validates if they are equal or different.

        Args:
            img1 (str): Full path to the first image.
            img2 (str): Full path to the second image.
            expected (str): "Equal" (expects images to be equal) or "Different" (expects images to be different).
            tolerance (float): Difference tolerance in percent (0.1 = 10%).
        """
        # Load images
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)

        if image1 is None:
            raise AssertionError(f"Could not open image: {img1}")
        if image2 is None:
            raise AssertionError(f"Could not open image: {img2}")

        # Resize if images have different sizes
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # Calculate absolute difference
        diff = cv2.absdiff(image1, image2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero = np.count_nonzero(gray)
        total_pixels = gray.size
        difference_percent = (non_zero / total_pixels) * 100

        # Set limit in %
        limit = tolerance * 100

        # Logging helper
        def log(msg, level="INFO"):
            self._builtin.log_to_console(msg)
            self._builtin.log(msg, level)

        # Evaluate as expected
        if expected == "Equal":
            if difference_percent > limit:
                log(f"❌ IMAGES ARE DIFFERENT. Difference: {difference_percent:.2f}% (limit {limit:.2f}%)", "ERROR")
                raise AssertionError(f"Images are different. Difference {difference_percent:.2f}% > limit {limit:.2f}%")
            else:
                log(f"✅ IMAGES ARE EQUAL. Difference: {difference_percent:.2f}% (<= {limit:.2f}%)")

        elif expected == "Different":
            if difference_percent <= limit:
                log(f"❌ IMAGES ARE TOO SIMILAR. Difference: {difference_percent:.2f}% (limit {limit:.2f}%)", "ERROR")
                raise AssertionError(f"Images are too similar. Difference {difference_percent:.2f}% <= limit {limit:.2f}%")
            else:
                log(f"✅ IMAGES ARE DIFFERENT. Difference: {difference_percent:.2f}% (> {limit:.2f}%)")
