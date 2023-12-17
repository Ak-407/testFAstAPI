from pydantic import BaseModel
from typing import List


# PostsLists getting consumed by users schema
class PostsList(BaseModel):
    title: str
    body: str
    rating: int

    class Config:
        orm_mode = True


class RegisterUserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Bee Bee Wijaya",
                "email": "beebeewijaya@gmail.com",
                "password": "test-password"
            }
        }


class UserDisplaySchema(BaseModel):
    email: str
    username: str
    posts: List[PostsList] = []

    class Config:
        orm_mode = True
