from typing import Any, List

from src.pipeline.base import ExtractStep


class DefaultExtractStep(ExtractStep):
    """Implementação padrão de extração de dados."""

    def extract(self) -> List[Any]:
        """Extração de dados - implemente a lógica de extração aqui."""
        return []
