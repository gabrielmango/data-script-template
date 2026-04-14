# data-script-template

Template para scripts Python focados em manipulação de dados. Este repositório é um modelo leve para construir tarefas ETL, com suporte básico a configuração de ambiente, logging e conexões a bancos.

## Estrutura do projeto

- `main.py` — ponto de entrada para executar o pipeline ETL
- `src/utils/env_config.py` — carregamento de variáveis de ambiente via `.env`
- `src/utils/logger.py` — logger simples que grava em arquivo
- `src/db/postgresdb_connection.py` — conexão PostgreSQL com SQLAlchemy (queries parametrizadas, tratamento de erros)
- `src/db/mongodb_connection.py` — conexão MongoDB com PyMongo (suporte a credenciais via config)
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

## Exemplos

Veja `examples/etl_pipeline_example.py` para um pipeline ETL completo que demonstra:
- Extração de dados CSV
- Transformação de dados
- Carregamento em PostgreSQL
- Tratamento de erros e logging

Para executar o exemplo:
```powershell
python examples/etl_pipeline_example.py
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
