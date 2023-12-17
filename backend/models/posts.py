from db.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class PostsModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UsersModel", back_populates="posts")
