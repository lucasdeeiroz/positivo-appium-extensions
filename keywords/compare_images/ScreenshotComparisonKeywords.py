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
        Compara duas imagens já salvas e valida se são iguais ou diferenstes.

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

        # Avalia conforme esperado
        if expected == "Equal" and difference_percent > (tolerance * 100):
            raise AssertionError(f"❌ Imagens diferentes! Diferença: {difference_percent:.2f}%")
        elif expected == "Different" and difference_percent <= (tolerance * 100):
            raise AssertionError(f"❌ Imagens muito parecidas! Diferença: {difference_percent:.2f}%")
        else:
            print(f"✅ Comparação bem-sucedida! Diferença: {difference_percent:.2f}%")
