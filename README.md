# data-script-template

Template para scripts Python focados em manipulação de dados. Este repositório é um modelo leve para construir tarefas ETL, com suporte básico a configuração de ambiente, logging e conexões a bancos.

## Estrutura do projeto

- `main.py` — ponto de entrada para executar o pipeline ETL
- `src/utils/env_config.py` — carregamento de variáveis de ambiente via `.env`
- `src/utils/logger.py` — logger simples que grava em arquivo
- `src/db/postgresdb_connection.py` — conexão PostgreSQL com SQLAlchemy (queries parametrizadas, tratamento de erros)
- `src/db/mongodb_connection.py` — conexão MongoDB com PyMongo (suporte a credenciais via config)
- `src/pipeline/pipeline.py` — classe abstrata `ETLPipeline` com `run()` abstrato
- `.env.example` — modelo de variáveis de ambiente
- `requirements.txt` — dependências do projeto
- `pyproject.toml` — metadados de projeto e configurações de ferramentas
- `create_project.ps1` / `start_project.ps1` — scripts PowerShell para setup

## Pré-requisitos

- Python 3.11+
- Windows PowerShell (para executar os scripts `.ps1`)
- `pyenv-win` é opcional, mas usado nos scripts de setup

## Instalação

1. Crie e ative o ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Copie o arquivo de exemplo e preencha as variáveis:

```powershell
copy .env.example .env
```

4. Edite `.env` com valores reais de conexão e credenciais.

## Como executar

- Execução direta:

```powershell
python main.py
```

- Execução via Taskipy:

```powershell
task run
```

### Opções de CLI

```powershell
python main.py --env-file .env --log-file etl.log --log-level INFO --group PROCAPI
```

- `--env-file` : arquivo de ambiente a ser carregado
- `--log-file` : arquivo de log de execução
- `--log-level` : nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--group` : prefixo do grupo de variáveis no `.env`
- `--dry-run` : roda o pipeline sem executar a carga final

## Uso básico

1. Ajuste `main.py` para implementar as etapas do seu pipeline ETL: `extract()`, `transform()` e `load()`.
2. Carregue as configurações com `ConfigLoader` em `src/utils/env_config.py`:
   - Suporte a `.env` e variáveis de ambiente (prioridade para variáveis de sistema)
   - Validação de chaves obrigatórias
   - Fallback seguro quando arquivo não existe
3. Use `Logger` em `src/utils/logger.py` para gravar eventos e erros.

## API Reference

Para documentação completa das classes, consulte [API.md](API.md).

### Importações simplificadas

```python
from src import extract, transform, load, Logger, ConfigLoader, PostgresConnection, MongoDBConnection
```

Todos os componentes principais estão exportados no nível do pacote `src` para importação conveniente.

## ETL orientado a classes

O template agora usa classes abstratas para manter o mesmo padrão em todas as implementações:

- `ExtractStep` — passo de extração
- `TransformStep` — passo de transformação
- `LoadStep` — passo de carga
- `ETLPipeline` — orquestração do pipeline

Use a implementação padrão ou crie seus próprios filhos:

```python
from src.pipeline import DefaultETLPipeline, DefaultExtractStep, DefaultTransformStep, DefaultLoadStep

class MyExtractStep(DefaultExtractStep):
    def extract(self):
        return [1, 2, 3]

class MyTransformStep(DefaultTransformStep):
    def transform(self, data):
        return [x * 2 for x in data]

class MyLoadStep(DefaultLoadStep):
    def load(self, data):
        print(data)
        return len(data)

class MyPipeline(DefaultETLPipeline):
    def __init__(self):
        super().__init__()
        self.extract_step = MyExtractStep()
        self.transform_step = MyTransformStep()
        self.load_step = MyLoadStep()

    def get_name(self):
        return 'my_pipeline'

pipeline = MyPipeline()
pipeline.run()
```

## Exemplos

Veja os exemplos em `examples/` que demonstram diferentes formas de usar o template:

- `examples/etl_pipeline_example.py` — pipeline ETL completo com funções e carga PostgreSQL
- `examples/class_based_etl_example.py` — pipeline ETL baseado em classes abstratas, mostrando como estender `DefaultETLPipeline` e criar passos customizados

Para executar o exemplo de classes:
```powershell
python examples/class_based_etl_example.py
```

## Scripts úteis

- `create_project.ps1` — cria ambiente virtual e gera `requirements.txt`
- `start_project.ps1` — cria/ativa ambiente e instala dependências já existentes

## Documentação

- [API.md](API.md) — Referência completa das classes e funções
- [CONTRIBUTING.md](CONTRIBUTING.md) — Guia para contribuições
- [CHANGELOG.md](CHANGELOG.md) — Histórico de mudanças

## Observações

### Instalação para desenvolvimento

```powershell
pip install -e ".[dev]"
```

### Executar testes

```powershell
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Via Taskipy
task test
task test-cov
```

### Pre-commit hooks

Instale os hooks de pre-commit para automatizar linting e formatação:

```powershell
pre-commit install
```

Execute manualmente em todos os arquivos:

```powershell
pre-commit run --all-files
```

### Linting e formatação

```powershell
# Formatação automática
task format

# Linting
task lint
```

### Testes implementados

- **ConfigLoader**: carregamento de variáveis de ambiente, validação de arquivos, grupos de configuração
- **Logger**: inicialização, níveis de log, rotação de arquivos, formatação
- **Conexões DB**: testes básicos de inicialização e validação (PostgreSQL e MongoDB)

Os testes usam mocks para evitar dependências externas e garantem isolamento.
