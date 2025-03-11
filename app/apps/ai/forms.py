from enum import Enum

from pydantic import BaseModel


class FieldType(str, Enum):
    text = "text"
    number = "number"
    email = "email"
    password = "password"
    textarea = "textarea"
    select = "select"
    multi_select = "multi_select"
    radio = "radio"
    checkbox = "checkbox"
    date = "date"
    time = "time"
    datetime = "datetime"
    file = "file"
    image = "image"
    audio = "audio"
    video = "video"
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
