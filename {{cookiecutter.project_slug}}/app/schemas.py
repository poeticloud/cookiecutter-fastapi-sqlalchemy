from uuid import UUID

import pydantic


class Schema(pydantic.BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class AnimalDetail(Schema):
    id: UUID
    name: str
