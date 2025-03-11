import uuid
from datetime import datetime
from typing import Literal

from fastapi_mongo_base.schemas import BaseEntitySchema, MultiLanguageString
from pydantic import BaseModel


class CategorySchema(BaseModel):
    slug: str
    name: MultiLanguageString
    description: MultiLanguageString | None = None
    ancestors: list[str] = []
    level: int = 0
    is_active: bool = True

    @property
    def full_name(self) -> str:
        return " > ".join(self.ancestors + [self.name])

    @property
    def full_name_fa(self) -> str:
        return " > ".join(self.ancestors + [self.name_fa])

    @property
    def parent_name(self) -> str:
        return self.ancestors[-1] if self.ancestors else ""


class VersionSchema(BaseModel):
    id: str
    created_at: datetime
    openapi_schema: dict | None = None


class ReviewSchema(BaseModel):
    user_id: uuid.UUID
    rating: int
    comment: str | None = None
    created_at: datetime


class ModelSchema(BaseEntitySchema):
    name: MultiLanguageString
    description: MultiLanguageString | None = None

    category: CategorySchema | None = None
    tags: list[str] = []
    logo: str | None = None
    cover_image: str | None = None

    chat_based: bool = False

    user_id: uuid.UUID | None = None

    run_count: int | None = None
    score: float | None = None
    stars: float | None = None

    api_available: bool = False

    pixy_available: bool = False
    pixy_url: str | None = None
    pixy_pricing: dict | None = None


class ModelDetailSchema(ModelSchema):
    user_id: uuid.UUID | None = None

    source: str = "replicate"
    owner: str | None = None
    visibility: Literal["public", "private"] = "public"
    versions: list[VersionSchema] = []

    default_example: dict | None = None

    source_url: str | None = None
    license_url: str | None = None
    github_url: str | None = None
    paper_url: str | None = None

    reviews: list[ReviewSchema] | None = None
