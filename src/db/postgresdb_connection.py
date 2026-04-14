from typing import Any, Dict, List, Optional, Union

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


class PostgresConnection:
    """Conexão PostgreSQL com SQLAlchemy para operações seguras e parametrizadas."""

    def __init__(self, connection_string: str, echo: bool = False):
        """Inicializa a conexão com PostgreSQL.

        Args:
            connection_string: String de conexão PostgreSQL
            echo: Se deve logar queries SQL (útil para debug)
        """
        self.connection_string = connection_string
        self.engine: Engine = create_engine(connection_string, echo=echo)
        self._connection = None

    def __enter__(self):
        """Context manager entry."""
        self._connection = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._connection:
            self._connection.close()

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executa uma query SELECT e retorna os resultados.

        Args:
            query: Query SQL parametrizada
            params: Parâmetros da query

        Returns:
            Lista de dicionários com os resultados

        Raises:
            SQLAlchemyError: Se houver erro na execução da query
        """
        if not self._connection:
            raise RuntimeError("Conexão não estabelecida. Use com 'with' ou chame connect() primeiro.")

        try:
            result = self._connection.execute(text(query), params or {})
            columns = list(result.keys())
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            return data
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f'Erro ao executar query: {query}') from e

    def execute_modify(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """Executa uma query de modificação (INSERT, UPDATE, DELETE).

        Args:
            query: Query SQL parametrizada
            params: Parâmetros da query

        Returns:
            Número de linhas afetadas

        Raises:
            SQLAlchemyError: Se houver erro na execução da query
        """
        try:
            with self.engine.begin() as connection:
                result = connection.execute(text(query), params or {})
                return result.rowcount
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f'Erro ao executar modificação: {query}') from e

    def execute_scalar(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Executa uma query que retorna um único valor.

        Args:
            query: Query SQL parametrizada
            params: Parâmetros da query

        Returns:
            Valor único ou None

        Raises:
            SQLAlchemyError: Se houver erro na execução da query
        """
        if not self._connection:
            raise RuntimeError("Conexão não estabelecida. Use com 'with' ou chame connect() primeiro.")

        try:
            result = self._connection.execute(text(query), params or {})
            row = result.fetchone()
            return row[0] if row else None
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f'Erro ao executar query escalar: {query}') from e

    def test_connection(self) -> bool:
        """Testa se a conexão com o banco está funcionando.

        Returns:
            True se a conexão for bem-sucedida
        """
        try:
            with self.engine.begin() as connection:
                connection.execute(text('SELECT 1'))
            return True
        except SQLAlchemyError:
            return False
