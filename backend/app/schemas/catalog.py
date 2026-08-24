from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str


class BookResponse(BaseModel):
    id: int
    isbn: str
    title: str
    publisher: str | None
    publication_year: int | None
    description: str | None
    category: CategoryResponse
    authors: list[AuthorResponse]
    total_copies: int
    available_copies: int
