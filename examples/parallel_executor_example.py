"""Exemplo de uso do ParallelExecutor."""

from src.utils import ExecutionMode, ParallelExecutor


def process_chunk(chunk):
    """Função de exemplo que processa um chunk de dados."""
    # Simula processamento (soma os números do chunk)
    return sum(chunk) if chunk else 0


def main():
    # Criar dados de teste
    data = list(range(1, 101))  # [1, 2, 3, ..., 100]

    print('Dados originais:', data[:10], '...', data[-10:])

    # Criar executor paralelo
    executor = ParallelExecutor(
        func=process_chunk, num_parts=10, max_workers=4, mode=ExecutionMode.THREADS, show_progress=True
    )

    # Executar processamento paralelo
    results = executor.run(data)

    print('\nResultados por parte:')
    for i, result in enumerate(results):
        print(f'Parte {i+1}: {result}')

    total = sum(results)
    print(f'\nSoma total: {total}')
    print(f'Verificação: {sum(data)}')


if __name__ == '__main__':
    main()
