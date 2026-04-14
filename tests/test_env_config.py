"""Testes para o módulo de configuração de ambiente."""
import os
import tempfile
from pathlib import Path

import pytest

from src.utils.env_config import ConfigLoader


class TestConfigLoader:
    """Testes para ConfigLoader."""

    def test_load_config_without_env_file(self):
        """Testa carregamento sem arquivo .env."""
        loader = ConfigLoader()
        config = loader._load_config()
        assert isinstance(config, dict)

    def test_load_config_with_env_file(self):
        """Testa carregamento com arquivo .env."""
        # Cria arquivo .env temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write('TEST_KEY=test_value\n')
            f.write('TEST_NUMBER=42\n')
            env_file = f.name

        try:
            loader = ConfigLoader(env_file)
            config = loader._load_config()

            assert config['TEST_KEY'] == 'test_value'
            assert config['TEST_NUMBER'] == '42'
        finally:
            Path(env_file).unlink()

    def test_load_group_basic(self):
        """Testa carregamento de grupo básico."""
        # Simula variáveis de ambiente
        os.environ['TEST_PREFIX_KEY1'] = 'value1'
        os.environ['TEST_PREFIX_KEY2'] = 'value2'
        os.environ['OTHER_KEY'] = 'ignored'

        try:
            loader = ConfigLoader()
            group = loader.load_group('TEST_PREFIX')

            assert hasattr(group, 'key1')
            assert hasattr(group, 'key2')
            assert not hasattr(group, 'other_key')

            assert group.key1 == 'value1'
            assert group.key2 == 'value2'
        finally:
            # Limpa variáveis de ambiente
            del os.environ['TEST_PREFIX_KEY1']
            del os.environ['TEST_PREFIX_KEY2']
            del os.environ['OTHER_KEY']

    def test_load_group_with_required_keys(self):
        """Testa carregamento de grupo com chaves obrigatórias."""
        os.environ['REQUIRED_KEY1'] = 'value1'

        try:
            loader = ConfigLoader()
            # Deve funcionar com chave obrigatória presente
            group = loader.load_group('REQUIRED', required_keys=['key1'])
            assert group.key1 == 'value1'

            # Deve falhar com chave obrigatória ausente
            with pytest.raises(ValueError, match='Configurações obrigatórias faltando'):
                loader.load_group('REQUIRED', required_keys=['key1', 'key2'])
        finally:
            del os.environ['REQUIRED_KEY1']

    def test_get_method(self):
        """Testa método get."""
        os.environ['GET_TEST_KEY'] = 'get_value'

        try:
            loader = ConfigLoader()
            assert loader.get('GET_TEST_KEY') == 'get_value'
            assert loader.get('NON_EXISTENT_KEY') is None
            assert loader.get('NON_EXISTENT_KEY', 'default') == 'default'
        finally:
            del os.environ['GET_TEST_KEY']

    def test_validate_env_file(self):
        """Testa validação de arquivo .env."""
        loader = ConfigLoader('.env')
        assert loader.validate_env_file()  # Arquivo .env existe no projeto

        loader_nonexistent = ConfigLoader('nonexistent.env')
        assert not loader_nonexistent.validate_env_file()
