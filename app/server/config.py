"""FastAPI server configuration."""

import dataclasses
import os
from pathlib import Path

import dotenv
from fastapi_mongo_base.core import config

dotenv.load_dotenv()


@dataclasses.dataclass
class Settings(config.Settings):
    """Server config settings."""

    base_dir: Path = Path(__file__).resolve().parent.parent
    base_path: str = "/v1/apps/hub"
    update_time: int = 10

    UFILES_API_KEY: str = os.getenv("UFILES_API_KEY")
    UFILES_BASE_URL: str = os.getenv("UFILES_URL")
    UFAAS_BASE_URL: str = os.getenv("UFAAS_BASE_URL")
    USSO_BASE_URL: str = os.getenv("USSO_URL")
    UFAAS_RESOURCE_VARIANT: str = os.getenv(
        "UFAAS_RESOURCE_VARIANT", default="hub"
    )
