import math
import time
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union


class ExecutionMode(Enum):
    """Modos de execução paralela disponíveis."""

    THREADS = 'threads'
    PROCESSES = 'processes'


class ParallelExecutor:
    """
    Executor paralelo que divide uma lista em partes e executa uma função sobre cada parte.

    Características:
    - Suporte a threads e processos
    - Divisão equilibrada da lista
    - Tratamento de exceções robusto
    - Progresso opcional com barra visual
    - Logging integrado
    - Resultados ordenados pela ordem original
    """

    def __init__(
        self,
        func: Callable,
        num_parts: int = 10,
        max_workers: Optional[int] = None,
        mode: ExecutionMode = ExecutionMode.THREADS,
        show_progress: bool = True,
        logger: Optional[Callable[[str], None]] = None,
    ):
        """
        Inicializa o executor paralelo.

        Args:
            func: Função a ser executada em paralelo sobre cada parte da lista
            num_parts: Número de partes em que dividir a lista
            max_workers: Número máximo de workers (padrão: min(num_parts, 4))
            mode: Modo de execução (THREADS ou PROCESSES)
            show_progress: Se deve mostrar barra de progresso
            logger: Função de logging opcional (recebe string como parâmetro)
        """
        if num_parts < 1:
            raise ValueError('num_parts deve ser pelo menos 1')
        if max_workers is not None and max_workers < 1:
            raise ValueError('max_workers deve ser pelo menos 1')

        self.func = func
        self.num_parts = num_parts
        self.max_workers = max_workers or min(num_parts, 4)
        self.mode = mode
        self.show_progress = show_progress
        self.logger = logger or print

    def _split_list(self, data: List[Any]) -> List[List[Any]]:
        """
        Divide uma lista em partes equilibradas.

        Args:
            data: Lista a ser dividida

        Returns:
            Lista de sublistas (partes)
        """
        if not data:
            return []

        chunk_size = math.ceil(len(data) / self.num_parts)
        return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

    def _create_executor(self):
        """Cria o executor apropriado baseado no modo."""
        if self.mode == ExecutionMode.THREADS:
            return ThreadPoolExecutor(max_workers=self.max_workers)
        elif self.mode == ExecutionMode.PROCESSES:
            return ProcessPoolExecutor(max_workers=self.max_workers)
        else:
            raise ValueError(f'Modo não suportado: {self.mode}')

    def _execute_with_progress(self, futures: List[Future], total_parts: int) -> List[Any]:
        """
        Executa futures com acompanhamento de progresso.

        Args:
            futures: Lista de futures a aguardar
            total_parts: Número total de partes

        Returns:
            Lista de resultados na ordem original
        """
        results = [None] * total_parts
        completed = 0

        if self.show_progress:
            self.logger(f'Iniciando execução paralela: {total_parts} partes, {self.max_workers} {self.mode.value}')

        start_time = time.time()

        for future in as_completed(futures):
            # Encontrar o índice original da future
            for i, f in enumerate(futures):
                if f == future:
                    index = i
                    break

            try:
                result = future.result()
                results[index] = result
                completed += 1

                if self.show_progress:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    eta = (total_parts - completed) / rate if rate > 0 else 0
                    progress = f'[{completed}/{total_parts}] Concluída parte {index + 1}'
                    if eta > 0:
                        progress += f' (ETA: {eta:.1f}s)'
                    self.logger(progress)

            except Exception as e:
                self.logger(f'Erro na parte {index + 1}: {e}')
                results[index] = e  # Armazenar a exceção para o usuário decidir como lidar
                completed += 1

        if self.show_progress:
            total_time = time.time() - start_time
            self.logger(f'Execução concluída em {total_time:.2f}s')

        return results

    def run(self, data: List[Any]) -> List[Any]:
        """
        Executa a função em paralelo sobre as partes da lista.

        Args:
            data: Lista de dados a processar

        Returns:
            Lista de resultados na ordem original das partes.
            Se ocorrer erro em alguma parte, a exceção será retornada no lugar do resultado.
        """
        if not isinstance(data, list):
            raise TypeError('data deve ser uma lista')

        parts = self._split_list(data)
        if not parts:
            return []

        with self._create_executor() as executor:
            futures = [executor.submit(self.func, part) for part in parts]
            return self._execute_with_progress(futures, len(parts))

    def run_flatten(self, data: List[Any]) -> List[Any]:
        """
        Executa e achata os resultados (útil quando cada parte retorna uma lista).

        Args:
            data: Lista de dados a processar

        Returns:
            Lista achatada de todos os resultados
        """
        results = self.run(data)
        flattened = []

        for result in results:
            if isinstance(result, Exception):
                raise result  # Re-raise exceptions
            if isinstance(result, list):
                flattened.extend(result)
            else:
                flattened.append(result)

        return flattened

    def run_with_timeout(self, data: List[Any], timeout: float) -> List[Any]:
        """
        Executa com timeout global.

        Args:
            data: Lista de dados a processar
            timeout: Timeout em segundos

        Returns:
            Lista de resultados

        Raises:
            TimeoutError: Se o timeout for excedido
        """
        parts = self._split_list(data)
        if not parts:
            return []

        with self._create_executor() as executor:
            futures = [executor.submit(self.func, part) for part in parts]

            try:
                # Aguardar todas as futures com timeout
                completed_futures = []
                for future in as_completed(futures, timeout=timeout):
                    completed_futures.append(future)

                # Processar resultados
                results = [None] * len(parts)
                for future in completed_futures:
                    for i, f in enumerate(futures):
                        if f == future:
                            try:
                                results[i] = future.result()
                            except Exception as e:
                                results[i] = e
                            break

                return results

            except TimeoutError:
                self.logger(f'Timeout de {timeout}s excedido')
                raise
