import os
from datetime import datetime


class Logger:
    """Classe simples para registro de logs em arquivo, com data e hora em cada mensagem."""

    def __init__(self, filepath: str, datetime_format: str = '%Y-%m-%d %H:%M:%S'):
        """Inicializa o logger."""
        self.filepath = 'logs/' + filepath
        self.datetime_format = datetime_format

        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def _write_log(self, level: str, message: str) -> None:
        """Escreve a mensagem com data/hora no arquivo."""
        now = datetime.now()
        timestamp = now.strftime(self.datetime_format)

        log_line = f'[{timestamp}] [{level}] {message}\n'
        try:
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except IOError as e:
            print(f'Erro ao escrever log: {e}')

    def info(self, message: str) -> None:
        self._write_log('INFO', message)

    def warning(self, message: str) -> None:
        self._write_log('WARNING', message)

    def error(self, message: str) -> None:
        self._write_log('ERROR', message)

    def debug(self, message: str) -> None:
        self._write_log('DEBUG', message)


if __name__ == '__main__':
    logger = Logger('meu_log_com_data.log')
    logger.info('Aplicação iniciada')
    logger.info('Usuário logou')
    logger.warning('Disco quase cheio')
    logger.error('Falha ao salvar arquivo')

    logger2 = Logger('log_hora.log', datetime_format='%H:%M:%S')
    logger2.info('Executando tarefa agendada')
