from src.pipeline.etl_extract import extract
from src.pipeline.etl_load import load
from src.pipeline.etl_transform import transform
from src.utils.env_config import ConfigLoader
from src.utils.logger import Logger


def main():
    logger = Logger('etl.log')
    logger.info('Iniciando pipeline ETL')

    loader = ConfigLoader()
    acesso_procapi = loader.load_group('PROCAPI')

    logger.info('Configurações PROCAPI carregadas')
    logger.debug(f'PROCAPI config: {acesso_procapi}')

    data = extract()
    processed = transform(data)
    rows = load(processed)

    logger.info(f'Pipeline ETL concluído com {rows} registros processados')


if __name__ == '__main__':
    main()
