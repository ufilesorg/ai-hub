from fastapi_mongo_base.routes import AbstractBaseRouter

from .models import AIModel
from .schemas import AIModelSchema


class AIModelRouter(AbstractBaseRouter):
    def __init__(self):
        super().__init__(
            model=AIModel,
            schema=AIModelSchema,
            user_dependency=None,
            tags=["AIModel"],
        )

    def config_routes(self, **kwargs):
        super().config_routes(
            create_route=False,
            update_route=False,
            delete_route=False,
        )



router = AIModelRouter().router
