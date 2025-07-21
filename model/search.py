from pydantic import AliasChoices, BaseModel, Field


class SearchRequest(BaseModel):
    search_query: str = Field(
        description="The query string to search for platforms by name",
        validation_alias=AliasChoices(
            "query", "search_query", "query_string", "search")
    )
    page: int = Field(1, ge=1, description="Page number for pagination")
    page_size: int = Field(
        10, ge=1, le=100, description="Number of results per page")
