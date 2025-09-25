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
    def compare_images(self, img1, img2, expected="Equal", tolerance=0.01):
        """
        Compare two saved images and validate if they are equal or different.

        Args:
            img1 (str): Full path to the first image.
            img2 (str): Full path to the second image.
            expected (str): "Equal" (expect equal) or "Different" (expect different).
            tolerance (float): Difference tolerance in percent (0.1 = 10%).

        Usage example:
            Compare Screenshots    path/to/img1.png    path/to/img2.png    Equal    0.02
        """
        # Carregar as imagens
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)

        if image1 is None:
            raise AssertionError(f"Could not open image: {img1}")
        if image2 is None:
            raise AssertionError(f"Could not open image: {img2}")

        # Redimensiona se forem de tamanhos diferentes
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # Calcula diferença absoluta
        diff = cv2.absdiff(image1, image2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero = np.count_nonzero(gray)
        total_pixels = gray.size
        difference_percent = (non_zero / total_pixels) * 100

        # Avalia conforme esperado
        if expected == "Equal" and difference_percent > (tolerance * 100):
            raise AssertionError(f"❌ Images are different! Difference: {difference_percent:.2f}%")
        elif expected == "Different" and difference_percent <= (tolerance * 100):
            raise AssertionError(f"❌ Images are too similar! Difference: {difference_percent:.2f}%")
        else:
            print(f"✅ Comparison successful! Difference: {difference_percent:.2f}%")
