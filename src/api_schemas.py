import datetime
import uuid

from pydantic import BaseModel


class NNModelCreateRequest(BaseModel):
    name: str
    description: str | None = None


class NNModelCreateResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    created_at: datetime.datetime
