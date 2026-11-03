"""Configurações da aplicação."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    app_name: str = "Genshin Impact API"
    app_version: str = "0.1.0"
    app_description: str = "API que retorna dados de personagens de Genshin Impact."
    app_version_api: str = "/api/v1"
    characters_data_path: Path = BASE_DIR / "data" / "characters.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()