from pydantic import BaseModel


class PaginateRequest(BaseModel):
    page: int = 1
    page_size: int = 10
