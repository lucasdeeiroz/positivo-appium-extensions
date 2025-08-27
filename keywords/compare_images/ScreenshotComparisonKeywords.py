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
        Compara duas imagens já salvas e valida se são iguais ou diferentes.

        Args:
            img1 (str): Caminho completo da primeira imagem.
            img2 (str): Caminho completo da segunda imagem.
            expected (str): "Equal" (espera iguais) ou "Different" (espera diferentes).
            tolerance (float): Tolerância de diferença em percentual (0.1 = 10%).
        """
        # Carregar as imagens
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)

        if image1 is None:
            raise AssertionError(f"Não foi possível abrir a imagem: {img1}")
        if image2 is None:
            raise AssertionError(f"Não foi possível abrir a imagem: {img2}")

        # Redimensiona se forem de tamanhos diferentes
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # Calcula diferença absoluta
        diff = cv2.absdiff(image1, image2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero = np.count_nonzero(gray)
        total_pixels = gray.size
        difference_percent = (non_zero / total_pixels) * 100

        # Define limite em %
        limit = tolerance * 100

        # Logging helper
        def log(msg, level="INFO"):
            self._builtin.log_to_console(msg)
            self._builtin.log(msg, level)

        # Avalia conforme esperado
        if expected == "Equal":
            if difference_percent > limit:
                log(f"❌ Imagens DIFERENTES. Diferença: {difference_percent:.2f}% (limite {limit:.2f}%)", "ERROR")
                raise AssertionError(f"Imagens diferentes. Diferença {difference_percent:.2f}% > limite {limit:.2f}%")
            else:
                log(f"✅ Imagens IGUAIS. Diferença: {difference_percent:.2f}% (<= {limit:.2f}%)")

        elif expected == "Different":
            if difference_percent <= limit:
                log(f"❌ Imagens MUITO PARECIDAS. Diferença: {difference_percent:.2f}% (limite {limit:.2f}%)", "ERROR")
                raise AssertionError(f"Imagens muito parecidas. Diferença {difference_percent:.2f}% <= limite {limit:.2f}%")
            else:
                log(f"✅ Imagens DIFERENTES. Diferença: {difference_percent:.2f}% (> {limit:.2f}%)")
