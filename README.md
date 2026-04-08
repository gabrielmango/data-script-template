# data-script-template

Template para scripts Python focados em manipulação de dados. Este repositório é um modelo leve para construir tarefas ETL, com suporte básico a configuração de ambiente, logging e conexões a bancos.

## Estrutura do projeto

- `main.py` — ponto de entrada para executar o pipeline ETL
- `src/utils/env_config.py` — carregamento de variáveis de ambiente via `.env`
- `src/utils/logger.py` — logger simples que grava em arquivo
- `src/db/postgresdb_connection.py` — conexão PostgreSQL com SQLAlchemy
- `src/db/mongodb_connection.py` — conexão MongoDB com pymongo
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
python main.py --env-file .env --log-file etl.log --group PROCAPI
```

- `--env-file` : arquivo de ambiente a ser carregado
- `--log-file` : arquivo de log de execução
- `--group` : prefixo do grupo de variáveis no `.env`
- `--dry-run` : roda o pipeline sem executar a carga final

## Uso básico

1. Ajuste `main.py` para implementar as etapas do seu pipeline ETL: `extract()`, `transform()` e `load()`.
2. Carregue as configurações com `ConfigLoader` em `src/utils/env_config.py`:
   - Suporte a `.env` e variáveis de ambiente (prioridade para variáveis de sistema)
   - Validação de chaves obrigatórias
   - Fallback seguro quando arquivo não existe
3. Use `Logger` em `src/utils/logger.py` para gravar eventos e erros.

## Scripts úteis

- `create_project.ps1` — cria ambiente virtual e gera `requirements.txt`
- `start_project.ps1` — cria/ativa ambiente e instala dependências já existentes

## Observações

- Não comite o arquivo `.env` com valores reais.
- O diretório `logs/` é ignorado pelo Git para evitar commit de arquivos de log.
- Se quiser suporte adicional a CLI, o template já inclui dependências como `click`.
