import math
from typing import Any, Generic, List, Type, TypeVar

from fastapi import Query
from pydantic.generics import GenericModel

from app.core.config import settings
from app.schemas import Schema

DataT = TypeVar("DataT")


class PaginationResult(GenericModel, Generic[DataT]):
    total: int
    results: List[DataT]
    pages: int


class Pagination:
    def __init__(
        self,
        limit: int = Query(default=settings.default_limit, ge=1, le=settings.max_limit),
        offset: int = Query(default=0, ge=0),
    ):
        self.limit = limit
        self.offset = offset

    def apply(self, qs, schema: Type[Schema]):
        total, results = qs.count(), qs.limit(self.limit).offset(self.offset).all()
        pages = int(math.ceil(total / self.limit))

        return PaginationResult(total=total, results=[schema.from_orm(obj) for obj in results], pages=pages)
