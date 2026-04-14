# API Documentation

## Modules Overview

### src.pipeline
Pipeline ETL com funções de extração, transformação e carga.

#### Functions
- `extract()` → List[Any]
  - Extrai dados da fonte
  - Implementar com lógica específica
  
- `transform(data: List[Any])` → List[Any]
  - Transforma os dados extraídos
  - Implementar com lógica de negócio
  
- `load(data: List[Any])` → int
  - Carrega os dados processados
  - Retorna número de registros carregados

### src.utils
Utilitários para configuração e logging.

#### ConfigLoader
```python
from src.utils import ConfigLoader

loader = ConfigLoader('.env')

# Carregar grupo de configurações
db_config = loader.load_group('POSTGRES', required_keys=['host', 'user'])
print(db_config.host)
print(db_config.user)

# Obter valor individual
env = loader.get('ENVIRONMENT', default='development')

# Validar arquivo .env
if loader.validate_env_file():
    print(".env existe e é acessível")
```

#### Logger
```python
from src.utils import Logger, get_logger

# Inicializar logger
logger = Logger('meu_app', 'app.log', level='DEBUG')

# Ou usar função de conveniência
logger = get_logger('meu_app', 'app.log')

# Usar
logger.info('Iniciando aplicação')
logger.debug('Detalhado')
logger.warning('Aviso')
logger.error('Erro')
logger.critical('Crítico')
logger.exception('Erro com traceback')
```

### src.db
Conexões de banco de dados.

#### PostgresConnection
```python
from src.db import PostgresConnection

conn_string = "postgresql://user:pass@localhost/dbname"

with PostgresConnection(conn_string) as conn:
    # Consulta
    data = conn.execute_query("SELECT * FROM tabela WHERE id = %(id)s", {'id': 1})
    
    # Modificação
    rows_affected = conn.execute_modify(
        "INSERT INTO tabela (nome) VALUES (%(nome)s)",
        {'nome': 'João'}
    )
    
    # Valor único
    count = conn.execute_scalar("SELECT COUNT(*) FROM tabela")
    
    # Testar conexão
    if conn.test_connection():
        print("Conexão OK")
```

#### MongoDBConnection
```python
from src.db import MongoDBConnection

# Via string de conexão
conn = MongoDBConnection("mongodb://user:pass@localhost:27017/dbname")

# Ou via parâmetros
conn = MongoDBConnection(
    host='localhost',
    port=27017,
    username='user',
    password='pass',
    db_name='dbname'
)

# Ou via configuração
from src.utils import ConfigLoader
config = ConfigLoader().load_group('MONGODB')
conn = MongoDBConnection.from_config(config)

# Usar
with conn as db:
    collection = db['minha_colecao']
    collection.insert_one({'nome': 'João'})
    documento = collection.find_one({'nome': 'João'})

# Testar conexão
if conn.test_connection():
    print("Conexão OK")
```

## Main CLI

Execute o pipeline via CLI:

```bash
python main.py --env-file .env --log-level DEBUG --group PROCAPI --dry-run
```

### Opções
- `--env-file`: arquivo .env a usar (padrão: .env)
- `--log-file`: arquivo de log (padrão: etl.log)
- `--log-level`: DEBUG|INFO|WARNING|ERROR|CRITICAL (padrão: INFO)
- `--group`: prefixo de variáveis de ambiente (padrão: PROCAPI)
- `--dry-run`: simular sem persistência final

## Imports simplificados

```python
# Importar do pacote raiz
from src import extract, transform, load, Logger, ConfigLoader, PostgresConnection, MongoDBConnection
```