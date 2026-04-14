# Contributing

Guia para contribuições ao data-script-template.

## Configuração do ambiente

1. Clone o repositório
2. Crie e ative um ambiente virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Instale em modo desenvolvimento:
   ```powershell
   pip install -e ".[dev]"
   ```

4. Instale os hooks de pre-commit:
   ```powershell
   pre-commit install
   ```

## Workflow

### Criar uma feature

1. Crie uma branch:
   ```powershell
   git checkout -b feature/minha-feature
   ```

2. Implemente a feature

3. Escreva testes em `tests/`

4. Execute testes e linting:
   ```powershell
   task test
   task lint
   ```

5. Formate o código:
   ```powershell
   task format
   ```

6. Commit com mensagem descritiva:
   ```powershell
   task commit "feat: descrição da feature"
   ```

### Depois de fazer changes

Sempre execute antes de commitar:

```powershell
task pre_commit
```

Isso vai:
- Formatação com black/isort
- Atualizar requirements.txt
- Configurar git
- Mostrar status

## Padrões de código

- **Formatação**: black (120 caracteres)
- **Import sort**: isort (perfil black, 120 caracteres)
- **Linting**: flake8
- **Type hints**: use quando apropriado
- **Docstrings**: use para funções/classes públicas

## Exemplo de commit bom

```
feat: adicionar suporte a cache no ConfigLoader

- Implementar cache em memória para configurações
- Adicionar método clear_cache()
- Adicionar testes para cache
- Atualizar documentação
```

## Testes

- Sempre escreva testes para features novas
- Use mocks para evitar dependências externas
- Mantenha cobertura > 80%

```powershell
# Ver cobertura
task test-cov

# Resultado em htmlcov/index.html
```

## Pull Requests

- Uma PR por feature
- Descrição clara do que foi feito
- Reference issues quando aplicável
- Todos os testes devem passar

## Changelog

Para mudanças significativas, adicione ao `CHANGELOG.md` (se existir).

Padrão:
- `[Unreleased]` para features não lançadas
- `[X.Y.Z]` para versões lançadas com data