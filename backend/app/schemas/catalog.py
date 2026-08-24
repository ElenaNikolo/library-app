from pydantic import BaseModel, ConfigDict, Field


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


class AuthorCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=60)
    last_name: str = Field(min_length=1, max_length=60)


class BookCreate(BaseModel):
    isbn: str = Field(min_length=10, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    publisher: str | None = Field(default=None, max_length=120)
    publication_year: int | None = None
    description: str | None = None
    category_id: int
    author_ids: list[int]


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
