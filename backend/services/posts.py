from models.posts import PostsModel
from models.users import UsersModel
from sqlalchemy.orm import Session


def create_edit_post_service(pm, db: Session):
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return pm


def get_posts_service(limit: int, skip: int, db: Session, user: UsersModel):
    return db.query(PostsModel).filter(PostsModel.user_id == user.id).offset(skip).limit(limit).all()


def get_posts_detail_service(id: int, db: Session, user: UsersModel):
    return db.query(PostsModel).filter(PostsModel.user_id == user.id).filter(PostsModel.id == id).first()


def delete_post_service(post: PostsModel, db: Session):
    db.delete(post)
    db.commit()
    return True
