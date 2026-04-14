"""
Exemplo de pipeline ETL usando o template.

Este arquivo demonstra como implementar um pipeline ETL simples
que lê dados de um CSV, processa e salva em um banco PostgreSQL.
"""

import csv
import io
from typing import Any, Dict, List

from src.db.postgresdb_connection import PostgresConnection
from src.pipeline.default_extract import extract
from src.pipeline.default_load import load
from src.pipeline.default_transform import transform
from src.utils.env_config import ConfigLoader
from src.utils.logger import Logger


def extract_csv_data() -> List[Dict[str, Any]]:
    """Extrai dados de um CSV em memória (exemplo)."""
    # Dados de exemplo - em produção, ler de arquivo/API/banco
    csv_data = """id,nome,idade,cidade
1,João,25,São Paulo
2,Maria,30,Rio de Janeiro
3,José,35,Belo Horizonte"""

    reader = csv.DictReader(io.StringIO(csv_data))
    return list(reader)


def transform_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transforma os dados: converte idade para int, adiciona status."""
    transformed = []
    for row in data:
        transformed.append(
            {
                'id': int(row['id']),
                'nome': row['nome'].upper(),
                'idade': int(row['idade']),
                'cidade': row['cidade'],
                'status': 'ATIVO' if int(row['idade']) >= 18 else 'INATIVO',
            }
        )
    return transformed


def load_to_postgres(data: List[Dict[str, Any]]) -> int:
    """Carrega dados no PostgreSQL."""
    # Carrega configuração do banco
    loader = ConfigLoader()
    db_config = loader.load_group('POSTGRES', required_keys=['host', 'database', 'user', 'password'])

    conn_string = f'postgresql://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}'

    with PostgresConnection(conn_string) as conn:
        # Cria tabela se não existir
        conn.execute_modify(
            """
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(100),
                idade INTEGER,
                cidade VARCHAR(100),
                status VARCHAR(20)
            )
        """
        )

        # Insere dados
        for row in data:
            conn.execute_modify(
                """
                INSERT INTO pessoas (id, nome, idade, cidade, status)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    nome = EXCLUDED.nome,
                    idade = EXCLUDED.idade,
                    cidade = EXCLUDED.cidade,
                    status = EXCLUDED.status
            """,
                (row['id'], row['nome'], row['idade'], row['cidade'], row['status']),
            )

    return len(data)


def main():
    """Pipeline ETL completo."""
    logger = Logger('etl_pipeline', level='INFO')

    logger.info('Iniciando pipeline ETL de exemplo')

    try:
        # Extract
        logger.info('Fase EXTRACT: lendo dados CSV')
        data = extract_csv_data()
        logger.info(f'Dados extraídos: {len(data)} registros')

        # Transform
        logger.info('Fase TRANSFORM: processando dados')
        processed_data = transform_data(data)
        logger.info(f'Dados transformados: {len(processed_data)} registros')

        # Load
        logger.info('Fase LOAD: salvando no PostgreSQL')
        rows_loaded = load_to_postgres(processed_data)
        logger.info(f'Pipeline concluído: {rows_loaded} registros carregados')

    except Exception as e:
        logger.error(f'Erro no pipeline ETL: {e}')
        raise


if __name__ == '__main__':
    main()
