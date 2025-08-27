""" Environment variable manager. """

import sys
from typing import Optional

from src.core import log
from .models import AppConfig, DatabaseConfig, ApiBrasilDevices, ApiBrasilCredentials
from .exceptions import ConfigValidationError
from .validators import (
    EnvValidator,
    FileValidator,
    RequiredKeysValidator,
    TypeConversionValidator,
    RequiredSystem
)


FALLBACK_TIMER: int = 2
DEACTIVATED_INTERVAL: float = 60
DATABASE_REQUIRED_KEYS: list = ["HOSTNAME", "DATABASE", "PASSWORD", "USER"]
IGNORED_KEYS: list = ["STILL_ON"]
CREDENTIAL_REQUIRED_KEYS: list = [
    "API_BRASIL_DEVICE_TOKEN_CPF",
    "API_BRASIL_DEVICE_TOKEN_CNPJ",
    "API_BRASIL_DEVICE_TOKEN_PLACA",
    "API_BRASIL_BEARER_TOKEN"
]

class RealTimeEnvManager:
    def __init__(self, env_file: str = '.env') -> None:
        self.env_file = env_file
        
        self._app_validators: list[EnvValidator] = [
            FileValidator(self.env_file),
            RequiredKeysValidator(["TIMER", "STILL_ON"]),
            TypeConversionValidator("TIMER", int)
        ]
    
    def load_app_config(self) -> AppConfig:
        env_data = self._read_env_file()
        self._validate(env_data, self._app_validators)
        
        return AppConfig(
            still_on=bool(env_data.get("STILL_ON", False)),
            timer=int(env_data.get("TIMER", FALLBACK_TIMER)),
            deactivated_interval=float(env_data.get("DEACTIVATED_INTERVAL", DEACTIVATED_INTERVAL))
        )
    
    def _read_env_file(self) -> dict[str, str]:
        try:
            with open(self.env_file, 'r', encoding='utf-8') as file:
                return self._parse_env(file)
        except Exception as e:
            log.dev.error(f"Erro inesperado: {e}")
            raise ConfigValidationError("Falha na leitura do ambiente") from e
    
    def _validate(self, env_data: dict[str, str], validators: list) -> None:
        for validator in validators:
            validator.validate(env_data)
    
    def _parse_env(self, file) -> dict[str, str]:
        env_vars: dict = {}
        for line in file:
            line = line.strip()
            
            if self.__skip_line(line):
                continue
            
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip()
        return env_vars
    
    def __skip_line(self, line) -> bool:
        """ Skips the line if it have some invalid thing. """
        if line.startswith('#'): # Ignore the comment lines.
            return True
        
        elif not '=' in line:
            return True
        
        return False


class AppConfigManager(RealTimeEnvManager):
    def __init__(self) -> None:
        super().__init__()
        self._db_config: Optional[DatabaseConfig] = None
        self.verify_off_command()
    
    def load_database_config(self) -> DatabaseConfig:
        """ Loads and validates the configurations. """
        if self._db_config is None: # Cache
            env_data = self._read_env_file()
            RequiredSystem(
                keys=DATABASE_REQUIRED_KEYS,
                ignore_keys=IGNORED_KEYS
            ).validate(env_data)
            
            self._db_config = DatabaseConfig(
                hostname=env_data["HOSTNAME"],
                database=env_data["DATABASE"],
                password=env_data["PASSWORD"],
                user=env_data["USER"],
                port=int(env_data.get("PORT", "5432"))
            )
        
        return self._db_config
    
    @property
    def database_url(self) -> str:
        """ Create connection URL. """
        db = self.load_database_config()
        return f"postgresql+psycopg2://{db.user}:{db.password}@{db.hostname}:{db.port}/{db.database}"
    
    def verify_off_command(self) -> None:
        """ If STILL_ON == False. Auto turn off the program """
        if not self.load_app_config().still_on:
            log.user.info(f'Arquivo .env: Comando STILL_ON ordem "desligar".\n\nSe deseja ligar o bot, preencha STILL_ON no arquivo .env -> Ex.: STILL_ON=ON\n')
            sys.exit()
