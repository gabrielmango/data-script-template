"""Exemplo de pipeline ETL baseado em classes abstratas."""

import csv
import io
from typing import Any, Dict, List

from src.pipeline import DefaultETLPipeline, DefaultExtractStep, DefaultLoadStep, DefaultTransformStep
from src.utils.logger import Logger


class CsvExtractStep(DefaultExtractStep):
    """Extração de dados a partir de CSV em memória."""

    def extract(self) -> List[Dict[str, Any]]:
        csv_data = """id,nome,idade,cidade
1,João,25,São Paulo
2,Maria,30,Rio de Janeiro
3,José,35,Belo Horizonte"""
        reader = csv.DictReader(io.StringIO(csv_data))
        return [dict(row) for row in reader]


class UppercaseTransformStep(DefaultTransformStep):
    """Transforma dados para padrão de texto uppercase."""

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                'id': int(row['id']),
                'nome': row['nome'].strip().upper(),
                'idade': int(row['idade']),
                'cidade': row['cidade'].strip().title(),
                'status': 'ATIVO' if int(row['idade']) >= 18 else 'INATIVO',
            }
            for row in data
        ]


class PrintLoadStep(DefaultLoadStep):
    """Carga de dados simulada que imprime o resultado."""

    def load(self, data: List[Dict[str, Any]]) -> int:
        for row in data:
            print(row)
        return len(data)


class ClassBasedETLPipeline(DefaultETLPipeline):
    """Pipeline ETL concreto com passos customizados."""

    def __init__(self):
        super().__init__()
        self.extract_step = CsvExtractStep()
        self.transform_step = UppercaseTransformStep()
        self.load_step = PrintLoadStep()

    def get_name(self) -> str:
        return 'class_based_example'


def main() -> None:
    logger = Logger('class_based_etl_example.log', level='INFO')
    logger.info('Executando pipeline ETL baseado em classes abstratas')

    pipeline = ClassBasedETLPipeline()
    record_count = pipeline.run(dry_run=False)

    logger.info(f'Pipeline concluído com {record_count} registros processados.')


if __name__ == '__main__':
    main()
