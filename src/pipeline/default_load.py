from typing import Any, List

from src.pipeline.base import LoadStep


class DefaultLoadStep(LoadStep):
    """Implementação padrão de carga de dados."""

    def load(self, data: List[Any]) -> int:
        """Carga de dados - implemente a lógica de gravação aqui."""
        return len(data)
