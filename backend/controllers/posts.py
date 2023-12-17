from sqlalchemy.orm import Session
from schema.posts import PostsSchema
from models.posts import PostsModel
from models.users import UsersModel
from utils.error import raise_exception

from services.posts import create_edit_post_service, get_posts_service, get_posts_detail_service, delete_post_service


def create_post(post: PostsSchema, db: Session, user: UsersModel):
    pm = PostsModel()
    pm.title = post.title
    pm.body = post.body
    pm.rating = post.rating
    pm.user_id = user.id

    res = create_edit_post_service(pm, db)
    return res


def get_posts(limit: int, skip: int, db: Session, user: UsersModel):
    return get_posts_service(limit, skip, db, user)


def update_posts(id: int, post: PostsSchema, db: Session, user: UsersModel):
    pm = get_posts_detail_service(id, db, user)
    if pm is None:
        return raise_exception("Post not found", status_code=400)
    pm.title = post.title
    pm.rating = post.rating
    pm.user_id = user.id

    res = create_edit_post_service(pm, db)
    return res


def delete_post(id: int, db: Session, user: UsersModel):
    pm = get_posts_detail_service(id, db, user)
    if pm is None:
        return raise_exception("Post not found", status_code=400)

    delete_post_service(pm, db)

    return {
        "message": "Successfully deleted",
        "post_id": id
    }
