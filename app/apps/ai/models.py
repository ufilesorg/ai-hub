from fastapi_mongo_base.models import BaseEntity
from pymongo import ASCENDING, TEXT, IndexModel

from .schemas import CategorySchema, ModelDetailSchema


class Category(CategorySchema, BaseEntity):
    class Settings:
        indexes = BaseEntity.Settings.indexes + [
            IndexModel([("slug", ASCENDING)], unique=True),
        ]


class Model(ModelDetailSchema, BaseEntity):

    class Settings:
        indexes = BaseEntity.Settings.indexes + [
            IndexModel([("name", ASCENDING)]),
            IndexModel(
                [
                    ("name", TEXT),
                    ("description", TEXT),
                    ("category", TEXT),
                    ("tags", TEXT),
                ],  # Text index for search
                name="text_search_index",
            ),
            IndexModel([("source_url", ASCENDING)], unique=True),
        ]
