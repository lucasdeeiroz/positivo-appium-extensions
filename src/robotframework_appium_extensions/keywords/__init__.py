import os
import importlib
import inspect
from typing import List, Type


def get_all_keyword_classes() -> List[Type]:
    """
    Descobre e retorna dinamicamente uma lista de todas as classes de keyword
    presentes neste diretório.
    """
    keyword_classes = []
    package_dir = os.path.dirname(__file__)

    for filename in os.listdir(package_dir):
        if filename.endswith(".py") and not filename.startswith("__init__"):
            module_name = filename[:-3]
            module = importlib.import_module(f".{module_name}", package=__name__)

            # Assumindo que o nome da classe da keyword é o mesmo que o nome do módulo.
            if hasattr(module, module_name):
                keyword_class = getattr(module, module_name)
                if inspect.isclass(keyword_class):
                    keyword_classes.append(keyword_class)
    return keyword_classes
