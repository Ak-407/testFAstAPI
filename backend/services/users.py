from sqlalchemy.orm import Session
from models.users import UsersModel


def create_user_service(um, db: Session):
    db.add(um)
    db.commit()
    db.refresh(um)
    return um


def get_user_service(um, db: Session):
    user = db.query(UsersModel).filter(UsersModel.email == um.email)
    return user.first()
