from enum import Enum
from typing import Literal

from fastapi_mongo_base.schemas import BaseEntitySchema
from pydantic import BaseModel


class FieldType(str, Enum):
    text = "text"
    number = "number"
    email = "email"
    password = "password"
    textarea = "textarea"
    select = "select"
    radio = "radio"
    checkbox = "checkbox"
    date = "date"
    time = "time"
    datetime = "datetime"
    file = "file"
    image = "image"
    color = "color"
    range = "range"
    url = "url"
    tel = "tel"
    hidden = "hidden"


class FieldSchema(BaseModel):
    name: str
    label: str
    placeholder: str | None = None
    description: str | None = None
    
    type: FieldType = FieldType.text
    
    options: list[str] | None = None
    required: bool = False
    validation: str | None = None  # regex
    
    value: str | None = None