from fastapi_mongo_base.routes import AbstractBaseRouter

from .models import Model
from .schemas import ModelSchema


class ModelRouter(AbstractBaseRouter):
    def __init__(self):
        super().__init__(
            model=Model,
            schema=ModelSchema,
            user_dependency=None,
            tags=["Model"],
        )

    def config_routes(self, **kwargs):
        super().config_routes(
            create_route=False,
            update_route=False,
            delete_route=False,
        )


router = ModelRouter().router
