from types import SimpleNamespace

from dotenv import dotenv_values


class ConfigLoader:
    def __init__(self, env_file='.env'):
        self.config = dotenv_values(env_file)

    def load_group(self, prefix: str):
        prefix = prefix.upper() + '_'

        filtered = {
            key.replace(prefix, '').lower(): value.strip()
            for key, value in self.config.items()
            if key.startswith(prefix)
        }

        return SimpleNamespace(**filtered)


loader = ConfigLoader()

acesso_procapi = loader.load_group('PROCAPI')
acesso_pje = loader.load_group('PJE')
acesso_solar = loader.load_group('SOLAR')
