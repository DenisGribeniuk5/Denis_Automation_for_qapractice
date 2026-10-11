from pydantic import BaseModel, ConfigDict, Field


class Book(BaseModel):
    model_config = ConfigDict(extra="forbid")

    isbn: str
    title: str
    subTitle: str
    author: str
    publish_date: str
    publisher: str
    pages: int
    description: str
    website: str


class BookList(BaseModel):
    books: list[Book]


class CreatedUser(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # The spec names this field userId, but the API sends userID.
    user_id: str = Field(alias="userID")
    username: str
    books: list[Book]


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(alias="userId")
    username: str
    books: list[Book]


class Token(BaseModel):
    token: str
    expires: str
    status: str
    result: str


class AddedBooks(BaseModel):
    books: list[dict[str, str]]


class ApiError(BaseModel):
    code: str
    message: str
