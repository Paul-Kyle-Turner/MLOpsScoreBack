from pydantic import AliasChoices, BaseModel, Field


class PaginateRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        validation_alias=AliasChoices(
            'page_size', 'size', 'limit', 'pageSize'
        )
    )
