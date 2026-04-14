"""Testes para conexões de banco de dados."""
from unittest.mock import Mock, patch

import pytest

from src.db.mongodb_connection import MongoDBConnection
from src.db.postgresdb_connection import PostgresConnection


class TestPostgresConnection:
    """Testes para PostgresConnection."""

    def test_initialization(self):
        """Testa inicialização da conexão PostgreSQL."""
        conn_string = 'postgresql://user:pass@localhost:5432/testdb'
        conn = PostgresConnection(conn_string)

        assert conn.connection_string == conn_string
        assert conn.engine is not None

    @patch('src.db.postgresdb_connection.create_engine')
    def test_test_connection_success(self, mock_create_engine):
        """Testa teste de conexão bem-sucedido."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine

        conn = PostgresConnection('postgresql://test')
        result = conn.test_connection()

        assert result is True
        mock_engine.begin.assert_called_once()

    @patch('src.db.postgresdb_connection.create_engine')
    def test_test_connection_failure(self, mock_create_engine):
        """Testa teste de conexão com falha."""
        from sqlalchemy.exc import SQLAlchemyError

        mock_engine = Mock()
        mock_engine.begin.side_effect = SQLAlchemyError('Connection failed')
        mock_create_engine.return_value = mock_engine

        conn = PostgresConnection('postgresql://test')
        result = conn.test_connection()

        assert result is False


class TestMongoDBConnection:
    """Testes para MongoDBConnection."""

    def test_initialization_with_connection_string(self):
        """Testa inicialização com string de conexão."""
        conn_string = 'mongodb://user:pass@localhost:27017/testdb'
        conn = MongoDBConnection(connection_string=conn_string, db_name='testdb')

        assert conn.connection_string == conn_string
        assert conn.db_name == 'testdb'

    def test_initialization_with_parameters(self):
        """Testa inicialização com parâmetros individuais."""
        conn = MongoDBConnection(host='localhost', port=27017, username='user', password='pass', db_name='testdb')

        expected_conn_string = 'mongodb://user:pass@localhost:27017/testdb'
        assert conn.connection_string == expected_conn_string

    def test_from_config_classmethod(self):
        """Testa método from_config."""
        config = Mock()
        config.host = 'testhost'
        config.port = 27018
        config.username = 'testuser'
        config.password = 'testpass'
        config.db_name = 'testdb'

        conn = MongoDBConnection.from_config(config)

        assert conn.connection_string == 'mongodb://testuser:testpass@testhost:27018/testdb'

    @patch('src.db.mongodb_connection.MongoClient')
    def test_test_connection_success(self, mock_mongo_client):
        """Testa teste de conexão bem-sucedido."""
        mock_client = Mock()
        mock_db = Mock()
        mock_client.__getitem__.return_value = mock_db
        mock_db.command.return_value = {'ok': 1}
        mock_mongo_client.return_value = mock_client

        conn = MongoDBConnection('mongodb://test')
        result = conn.test_connection()

        assert result is True

    @patch('src.db.mongodb_connection.MongoClient')
    def test_test_connection_failure(self, mock_mongo_client):
        """Testa teste de conexão com falha."""
        from pymongo.errors import PyMongoError

        mock_client = Mock()
        mock_client.__enter__.side_effect = PyMongoError('Connection failed')
        mock_mongo_client.return_value = mock_client

        conn = MongoDBConnection('mongodb://test')
        result = conn.test_connection()

        assert result is False
