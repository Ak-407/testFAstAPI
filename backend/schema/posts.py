from pydantic import BaseModel


class UserPost(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class PostsSchema(BaseModel):
    title: str
    body: str
    rating: int


class PostsDisplaySchema(BaseModel):
    id: int
    title: str
    body: str
    rating: int
    user: UserPost

    class Config:
        orm_mode = True
