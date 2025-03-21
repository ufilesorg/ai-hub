from apps.ai.routes import router as ai_router
from fastapi_mongo_base.core import app_factory

from . import config

app = app_factory.create_app(settings=config.Settings(), original_host_middleware=True)
app.include_router(ai_router, prefix=f"{config.Settings.base_path}")
