from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError


class MongoDBConnection:
    """Conexão MongoDB com PyMongo para operações seguras."""

    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_name: str = 'dbprocapi',
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        """Inicializa a conexão com MongoDB.

        Args:
            connection_string: String de conexão completa (tem prioridade)
            db_name: Nome do banco de dados
            host: Host do MongoDB
            port: Porta do MongoDB
            username: Nome de usuário
            password: Senha
            **kwargs: Outros parâmetros para MongoClient
        """
        self.db_name = db_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None

        if connection_string:
            self.connection_string = connection_string
        else:
            # Constrói string de conexão a partir dos parâmetros
            auth_part = ''
            if username and password:
                auth_part = f'{username}:{password}@'

            self.connection_string = f'mongodb://{auth_part}{host}:{port}/{db_name}'

        # Parâmetros adicionais para MongoClient
        self.client_kwargs = kwargs

    def __enter__(self) -> Database:
        """Context manager entry - retorna o banco de dados."""
        try:
            self.client = MongoClient(self.connection_string, **self.client_kwargs)
            self.db = self.client[self.db_name]
            return self.db
        except PyMongoError as e:
            raise PyMongoError(f'Erro ao conectar ao MongoDB: {self.connection_string}') from e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.client:
            self.client.close()

    def test_connection(self) -> bool:
        """Testa se a conexão com o banco está funcionando.

        Returns:
            True se a conexão for bem-sucedida
        """
        try:
            with self as db:
                db.command('ping')
            return True
        except PyMongoError:
            return False

    def get_database(self) -> Database:
        """Retorna o objeto Database (deve ser usado dentro de context manager).

        Returns:
            Objeto Database do PyMongo

        Raises:
            RuntimeError: Se chamado fora do context manager
        """
        if not self.db:
            raise RuntimeError("Banco de dados não disponível. Use com 'with' ou chame dentro do contexto.")
        return self.db

    @classmethod
    def from_config(cls, config: Any) -> 'MongoDBConnection':
        """Cria uma conexão MongoDB a partir de um objeto de configuração.

        Args:
            config: Objeto com atributos host, port, username, password, db_name, etc.

        Returns:
            Instância de MongoDBConnection
        """
        return cls(
            host=getattr(config, 'host', 'localhost'),
            port=getattr(config, 'port', 27017),
            username=getattr(config, 'username', None),
            password=getattr(config, 'password', None),
            db_name=getattr(config, 'db_name', 'dbprocapi'),
        )
