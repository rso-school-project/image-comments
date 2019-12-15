from sqlalchemy import Column, Integer, String

from image_comments.database import Base


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    image_id = Column(Integer)
    text = Column(String)

