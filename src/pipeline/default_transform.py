from typing import Any, List

from src.pipeline.base import TransformStep


class DefaultTransformStep(TransformStep):
    """Implementação padrão de transformação de dados."""

    def transform(self, data: List[Any]) -> List[Any]:
        """Transformação de dados - implemente a lógica de tratamento aqui."""
        return data
