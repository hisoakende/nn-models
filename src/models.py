import datetime
import enum
import functools
import uuid

import pytz as pytz
from pydantic import BaseModel, Field

from src import config


class NNModelStatus(enum.Enum):
    CREATED = 'created'
    UPLOADED = 'uploaded'
    READY = 'ready'


class Requirement(BaseModel):
    package_name: str
    version: str
    is_install: bool


class NNModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: str | None
    status: NNModelStatus
    requirements: list[Requirement]
    created_at: datetime.datetime = Field(
        default_factory=functools.partial(
            datetime.datetime.now,
            pytz.timezone(config.TIMEZONE)
        )
    )
