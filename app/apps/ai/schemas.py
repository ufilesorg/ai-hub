from fastapi_mongo_base.schemas import BaseEntitySchema
from pydantic import BaseModel
from .forms import FieldSchema

class Category(BaseModel):
    name: str
    slug: str
    description: str | None = None
    name_fa: str | None = None
    description_fa: str | None = None
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



class AIModelSchema(BaseEntitySchema):
    name: str
    description: str | None = None
    name_fa: str | None = None
    description_fa: str | None = None
    logo: str | None = None
    tags: list[str] = []
    category: Category | None = None

    inputs: list[FieldSchema] = []
    outputs: list[FieldSchema] = []

    score: float | None = None
    stars: float | None = None
    reviews: int | None = None

    source_url: str
    api_available: bool = False

    pixy_available: bool = False
    pixy_url: str | None = None
    pixy_pricing: str | None = None
