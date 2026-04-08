import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

from dotenv import dotenv_values


class ConfigLoader:
    """Carregador de configurações de ambiente com suporte a .env e variáveis de sistema."""

    def __init__(self, env_file: str = '.env'):
        self.env_file = Path(env_file)
        self._config: Optional[Dict[str, str]] = None

    def _load_config(self) -> Dict[str, str]:
        """Carrega configurações de .env e mescla com variáveis de ambiente."""
        if self._config is not None:
            return self._config

        config = {}

        # Carrega do .env se existir
        if self.env_file.exists():
            config.update(dotenv_values(self.env_file))

        # Mescla com variáveis de ambiente (elas têm prioridade)
        config.update(os.environ)

        self._config = config
        return config

    def load_group(self, prefix: str, required_keys: Optional[List[str]] = None) -> SimpleNamespace:
        """Carrega um grupo de configurações com prefixo específico.

        Args:
            prefix: Prefixo das variáveis (ex: 'PROCAPI')
            required_keys: Lista de chaves obrigatórias (sem prefixo)

        Returns:
            SimpleNamespace com as configurações

        Raises:
            ValueError: Se chaves obrigatórias estiverem faltando
        """
        config = self._load_config()
        prefix_upper = prefix.upper() + '_'

        filtered = {
            key.replace(prefix_upper, '').lower(): value.strip()
            for key, value in config.items()
            if key.startswith(prefix_upper) and value is not None
        }

        # Valida chaves obrigatórias
        if required_keys:
            missing = [key for key in required_keys if key.lower() not in filtered]
            if missing:
                raise ValueError(f'Configurações obrigatórias faltando para {prefix}: {missing}')

        return SimpleNamespace(**filtered)

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém uma configuração específica com fallback."""
        config = self._load_config()
        return config.get(key, default)

    def validate_env_file(self) -> bool:
        """Valida se o arquivo .env existe e é legível."""
        return self.env_file.exists() and self.env_file.is_file()
