import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class Logger:
    """Logger configurado com rotação de arquivos e níveis configuráveis."""

    def __init__(
        self,
        name: str = 'etl',
        log_file: str = 'etl.log',
        level: str = 'INFO',
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console: bool = True,
    ):
        """Inicializa o logger.

        Args:
            name: Nome do logger
            log_file: Nome do arquivo de log (será criado em logs/)
            level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_bytes: Tamanho máximo do arquivo antes da rotação
            backup_count: Número de arquivos de backup a manter
            console: Se deve logar também no console
        """
        self.name = name
        self.log_file = Path('logs') / log_file
        self.level = getattr(logging, level.upper(), logging.INFO)

        # Cria diretório logs se não existir
        self.log_file.parent.mkdir(exist_ok=True)

        # Configura o logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)

        # Remove handlers existentes para evitar duplicação
        self.logger.handlers.clear()

        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para arquivo com rotação
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Handler opcional para console
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        """Loga mensagem de debug."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Loga mensagem informativa."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Loga mensagem de aviso."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Loga mensagem de erro."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Loga mensagem crítica."""
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """Loga mensagem de erro com traceback."""
        self.logger.exception(message)


def get_logger(name: str = 'etl', log_file: str = 'etl.log', level: str = 'INFO') -> Logger:
    """Função de conveniência para obter um logger configurado."""
    return Logger(name=name, log_file=log_file, level=level)


if __name__ == '__main__':
    # Exemplo de uso
    logger = Logger('exemplo', 'exemplo.log', level='DEBUG')

    logger.info('Aplicação iniciada')
    logger.debug('Detalhes de debug')
    logger.warning('Aviso importante')
    logger.error('Erro ocorrido')

    # Teste de rotação (arquivo pequeno para demonstração)
    small_logger = Logger('teste_rotacao', 'teste.log', max_bytes=100, backup_count=3)
    for i in range(10):
        small_logger.info(f'Mensagem {i}: ' + 'x' * 50)

    print(f"Logs criados em: {Path('logs').absolute()}")
