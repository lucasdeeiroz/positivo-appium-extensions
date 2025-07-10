from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import cv2
import numpy as np
import os

class ScreenshotComparisonKeywords:

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword("Capturar Screenshot Inicial Como")
    def capturar_screenshot_inicial(self, nome_arquivo):
        self.driver.save_screenshot(nome_arquivo)
        print(f"📸 Screenshot inicial salvo como {nome_arquivo}")

    @keyword("Comparar Screenshot Final Com")
    def comparar_screenshot_final(self, arquivo_referencia, tolerancia=0.01):
        imagem_final = "screenshot_final.png"
        self.driver.save_screenshot(imagem_final)

        imagem1 = cv2.imread(arquivo_referencia)
        imagem2 = cv2.imread(imagem_final)

        if imagem1.shape != imagem2.shape:
            raise AssertionError("❌ As imagens têm tamanhos diferentes.")

        diff = cv2.absdiff(imagem1, imagem2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        total_pixels = gray.size
        diff_pixels = cv2.countNonZero(thresh)
        percentual_diferenca = diff_pixels / total_pixels

        print(f"🔍 Diferença detectada: {percentual_diferenca*100:.2f}%")

        if percentual_diferenca > tolerancia:
            raise AssertionError(f"❌ Diferença visual maior que o tolerado: {percentual_diferenca:.2%}")
        print("✅ As telas são visualmente semelhantes.")


