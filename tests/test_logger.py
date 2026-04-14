"""Testes para o módulo de logging."""
import logging
import tempfile
from pathlib import Path

from src.utils.logger import Logger


class TestLogger:
    """Testes para Logger."""

    def test_logger_initialization(self):
        """Testa inicialização do logger."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / 'test.log'
            logger = Logger('test', str(log_file))

            assert logger.name == 'test'
            assert logger.log_file == log_file
            assert logger.level == logging.INFO
            assert log_file.parent.exists()

    def test_logger_levels(self):
        """Testa diferentes níveis de log."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / 'test.log'
            logger = Logger('test', str(log_file), level='DEBUG')

            assert logger.level == logging.DEBUG

            logger_debug = Logger('test', str(log_file), level='ERROR')
            assert logger_debug.level == logging.ERROR

    def test_logger_writing(self):
        """Testa escrita de logs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / 'test.log'
            logger = Logger('test', str(log_file))

            logger.info('Test message')
            logger.error('Error message')

            # Verifica se arquivo foi criado e contém mensagens
            assert log_file.exists()
            content = log_file.read_text()
            assert 'Test message' in content
            assert 'Error message' in content
            assert 'test' in content  # nome do logger

    def test_logger_rotation(self):
        """Testa rotação de arquivos de log."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / 'test.log'
            logger = Logger('test', str(log_file), max_bytes=100, backup_count=2)

            # Escreve mensagens grandes para forçar rotação
            for i in range(10):
                logger.info(f'Message {i}: ' + 'x' * 50)

            # Verifica se arquivos de backup foram criados
            backup_files = list(log_file.parent.glob('test.log.*'))
            assert len(backup_files) > 0

    def test_get_logger_function(self):
        """Testa função get_logger."""
        from src.utils.logger import get_logger

        logger = get_logger('test_func', 'func.log')
        assert isinstance(logger, Logger)
        assert logger.name == 'test_func'
