"""Implementação padrão do pipeline ETL."""

from src.pipeline.base import ETLPipeline
from src.pipeline.default_extract import DefaultExtractStep
from src.pipeline.default_load import DefaultLoadStep
from src.pipeline.default_transform import DefaultTransformStep


class DefaultETLPipeline(ETLPipeline):
    """Pipeline ETL padrão que pode ser estendido por herança."""

    def __init__(self):
        super().__init__(DefaultExtractStep(), DefaultTransformStep(), DefaultLoadStep())

    def run(self, dry_run: bool = False) -> int:
        data = self.extract_step.extract()
        transformed = self.transform_step.transform(data)

        if dry_run:
            return len(transformed)

        return self.load_step.load(transformed)

    def get_name(self) -> str:
        return 'default'
