from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    posts: Mapped[List["Post"]] = relationship(back_populates="author")

    followers: Mapped[List["Follows"]] = relationship(back_populates="user_from")
    following: Mapped[List["Follows"]] = relationship(back_populates="user_to")

    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_type: Mapped[str] = mapped_column(String(120), nullable=False)
    caption: Mapped[str] = mapped_column(String(120), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship(back_populates="posts")

    post_comment: Mapped[List["Comment"]] = relationship(back_populates="comment_post")

    def serialize(self):
        return{
            "id": self.id,
            "type": self.post_type,
            "caption": self.caption,
        }
    
class Follows(db.Model):
    __tablename__ = "follows"
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, )
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    state: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user_from: Mapped["User"] = relationship(back_populates="followers")
    user_to: Mapped["User"] = relationship(back_populates="following")

    def serialize(self):
        return{
            "fromId": self.user_from_id,
            "toId": self.user_to_id,
        }
    
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(150), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    author: Mapped["User"] = relationship(back_populates="comments")

    comment_post: Mapped["Post"] = relationship(back_populates="post_comment")

    def serialize(self):
        return{
            "id": self.id,
            "comment": self.comment_text,
            "author": self.author_id,
            "postId": self.post_id
        }
    
