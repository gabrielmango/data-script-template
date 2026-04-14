from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

DataType = List[Any]


class ExtractStep(ABC):
    """Base abstrata para uma etapa de extração de dados."""

    @abstractmethod
    def extract(self) -> DataType:
        """Extrai dados da fonte de origem."""
        raise NotImplementedError


class TransformStep(ABC):
    """Base abstrata para uma etapa de transformação de dados."""

    @abstractmethod
    def transform(self, data: DataType) -> DataType:
        """Transforma os dados extraídos."""
        raise NotImplementedError


class LoadStep(ABC):
    """Base abstrata para uma etapa de carga de dados."""

    @abstractmethod
    def load(self, data: DataType) -> int:
        """Carrega os dados transformados e retorna o número de registros processados."""
        raise NotImplementedError


class ETLPipeline(ABC):
    """Base abstrata para um pipeline ETL completo."""

    def __init__(self, extract_step: ExtractStep, transform_step: TransformStep, load_step: LoadStep):
        self.extract_step = extract_step
        self.transform_step = transform_step
        self.load_step = load_step

    @abstractmethod
    def run(self, dry_run: bool = False) -> int:
        """Executa o pipeline ETL e retorna a quantidade de registros processados."""
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome do pipeline."""
        raise NotImplementedError
