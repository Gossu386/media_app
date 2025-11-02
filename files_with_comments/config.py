from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[1] / ".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = (
        False  # the changes aren't written to database tak jak w testach
    )


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="TEST_")
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = (
        True  # the changes aren't written to database tak jak w testach
    )


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    if env_state not in configs:
        raise ValueError(
            f"Invalid ENV_STATE '{env_state}'. Must be one of {list(configs.keys())}"
        )
    return configs[env_state]()


print("Loaded ENV_STATE:", BaseConfig().ENV_STATE)
config = get_config(BaseConfig().ENV_STATE)




"""
This module defines configuration classes and a utility function for managing application settings
using the `pydantic-settings` library. It supports different environments (development, production,
and testing) by leveraging environment variables and prefixes.

Classes:
    BaseConfig:
        A base configuration class that loads settings from an `.env` file located one directory
        above the current file. It also allows ignoring extra environment variables.

    GlobalConfig:
        Inherits from `BaseConfig` and adds global settings such as `DATABASE_URL` and
        `DB_FORCE_ROLL_BACK`. These settings are shared across all environments.

    DevConfig:
        Inherits from `GlobalConfig` and applies the `DEV_` prefix to environment variables.

    ProdConfig:
        Inherits from `GlobalConfig` and applies the `PROD_` prefix to environment variables.

    TestConfig:
        Inherits from `GlobalConfig`, applies the `TEST_` prefix to environment variables, and
        overrides `DATABASE_URL` to use a SQLite test database. It also enables `DB_FORCE_ROLL_BACK`
        to ensure database changes are not persisted during tests.

Functions:
    get_config(env_state: str):
        A cached function that returns the appropriate configuration class instance based on the
        provided `env_state`. Supported values are "dev", "prod", and "test". Raises a `ValueError`
        if an invalid `env_state` is provided.

Environment Variables:
    - ENV_STATE: Determines the current environment (e.g., "dev", "prod", "test").
    - DEV_*: Environment variables prefixed with `DEV_` are used for development settings.
    - PROD_*: Environment variables prefixed with `PROD_` are used for production settings.
    - TEST_*: Environment variables prefixed with `TEST_` are used for testing settings.
    - DATABASE_URL: Specifies the database connection URL.
    - DB_FORCE_ROLL_BACK: A boolean flag indicating whether database changes should be rolled back
      (useful for testing environments).

Usage:
    The `get_config` function is used to retrieve the appropriate configuration instance based on
    the `ENV_STATE` environment variable. For example:
    
    ```python
    config = get_config("dev")
    print(config.DATABASE_URL)
    ```
"""
