from sqlalchemy.orm import Session

from . import models


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comments).offset(skip).limit(limit).all()


def get_comment_by_user(db: Session, user_id: str):
    return db.query(models.Comments).filter(models.Comments.user_id == user_id).first()
