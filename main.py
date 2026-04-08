import click

from src.pipeline.etl_extract import extract
from src.pipeline.etl_load import load
from src.pipeline.etl_transform import transform
from src.utils.env_config import ConfigLoader
from src.utils.logger import Logger


@click.command()
@click.option('--env-file', default='.env', show_default=True, help='Arquivo .env a ser carregado.')
@click.option('--log-file', default='etl.log', show_default=True, help='Arquivo de log de execução.')
@click.option('--group', default='PROCAPI', show_default=True, help='Prefixo do grupo de variáveis de ambiente.')
@click.option('--dry-run', is_flag=True, help='Executa o pipeline sem executar a carga final.')
def main(env_file: str, log_file: str, group: str, dry_run: bool):
    logger = Logger(log_file)
    logger.info('Iniciando pipeline ETL')

    loader = ConfigLoader(env_file)

    # Valida se o arquivo .env existe
    if not loader.validate_env_file():
        logger.warning(f'Arquivo {env_file} não encontrado. Usando apenas variáveis de ambiente.')

    try:
        config_group = loader.load_group(group)
        logger.info(f'Configurações {group} carregadas')
        logger.debug(f'{group} config: {config_group}')
    except ValueError as e:
        logger.error(f'Erro na configuração: {e}')
        raise click.Abort()

    data = extract()
    processed = transform(data)

    if dry_run:
        logger.info('Dry-run ativado: etapa de carga será simulada, sem persistência.')
        rows = len(processed)
    else:
        rows = load(processed)

    logger.info(f'Pipeline ETL concluído com {rows} registros processados')


if __name__ == '__main__':
    main()
