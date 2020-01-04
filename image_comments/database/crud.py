from sqlalchemy.orm import Session

from . import models, schemas


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comments).offset(skip).limit(limit).all()


def get_comments_by_image(db: Session, image_id: int):
    return db.query(models.Comments).filter(models.Comments.image_id == image_id).all()


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comments(text=comment.text, user_id=comment.user_id, image_id=comment.image_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment