from fastapi_mongo_base.models import BaseEntity
from pymongo import ASCENDING, TEXT, IndexModel

from .schemas import AIModelSchema


class AIModel(AIModelSchema, BaseEntity):

    class Settings:
        indexes = BaseEntity.Settings.indexes + [
            IndexModel([("name", ASCENDING)]),
            IndexModel(
                [
                    ("name", TEXT),
                    ("description", TEXT),
                    ("name_fa", TEXT),
                    ("description_fa", TEXT),
                    ("category", TEXT),
                    ("tags", TEXT),
                ],  # Text index for search
                name="text_search_index",
            ),
        ]
