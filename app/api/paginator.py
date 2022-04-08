from __future__ import annotations

import math
from typing import Generic, Optional, Sequence, TypeVar

from fastapi import Request
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    count: int

    next_page: Optional[str] = None

    previous_page: Optional[str] = None

    results: Sequence[T]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_total_pages(cls, count: int, limit: int) -> int:
        try:
            return math.ceil(count / limit)
        except ZeroDivisionError:
            return 0

    @classmethod
    def get_next_page(cls, current_page: int, count: int, limit: int) -> Optional[str]:
        total_pages = cls.get_total_pages(count, limit)

        if current_page == total_pages or current_page > total_pages:
            return None

        return current_page + 1

    @classmethod
    def get_previous_page(
        cls, current_page: int, count: int, limit: int
    ) -> Optional[str]:
        total_pages = cls.get_total_pages(count, limit)

        if current_page == 1 or current_page > total_pages + 1:
            return None
        return current_page - 1

    @classmethod
    def get_next_page_url(
        cls, request: Request, name: str, current_page: int, count: int, limit: int
    ) -> Optional[str]:
        next_page = cls.get_next_page(current_page, count, limit)
        if next_page:
            return request.url_for(name=name, page=next_page)
        return None

    @classmethod
    def get_previous_page_url(
        cls, request: Request, name: str, current_page: int, count: int, limit: int
    ) -> Optional[str]:
        previous_page = cls.get_previous_page(current_page, count, limit)
        if previous_page:
            return request.url_for(name=name, page=previous_page)
        return None

    @classmethod
    def paginate(
        cls,
        request: Request,
        name: str,
        items: Sequence[T],
        count: int,
        current_page: int,
        limit: int,
    ) -> PaginatedResponse[T]:
        next_page = cls.get_next_page_url(request, name, current_page, count, limit)

        previous_page = cls.get_previous_page_url(
            request, name, current_page, count, limit
        )

        return cls(
            count=count, next_page=next_page, previous_page=previous_page, results=items
        )
