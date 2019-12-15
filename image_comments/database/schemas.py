from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    user_id: int
    image_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    image_id: int

    class Config:
        orm_mode = True
