from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from typing import List

from schema.posts import PostsDisplaySchema, PostsSchema
from controllers import posts as post_controllers
from services.auth import get_current_user, oauth_schema
from models.users import UsersModel

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.post("/")
def create_post_routes(pm: PostsSchema, db: Session = Depends(get_db), user: UsersModel = Depends(get_current_user)):
    return post_controllers.create_post(pm, db, user)


@router.get("/", response_model=List[PostsDisplaySchema])
def get_post_routes(limit: int = 10, skip: int = 0, db: Session = Depends(get_db),
                    user: UsersModel = Depends(get_current_user)):
    return post_controllers.get_posts(limit, skip, db, user)


@router.put("/{id}")
def update_post_routes(id: int, pm: PostsSchema, db: Session = Depends(get_db),
                       user: UsersModel = Depends(get_current_user)):
    return post_controllers.update_posts(id, pm, db, user)


@router.delete("/")
def delete_post_routes(id: int, db: Session = Depends(get_db), user: UsersModel = Depends(get_current_user)):
    return post_controllers.delete_post(id, db, user)
