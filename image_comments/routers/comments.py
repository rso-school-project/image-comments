import uuid
import time
# import logging

from typing import List
from fastapi import APIRouter
from func_timeout import func_set_timeout


from image_comments import settings
from image_comments.utils import fallback

# import json_log_formatter

#
# formatter = json_log_formatter.JSONFormatter()
# json_handler = logging.StreamHandler()
# json_handler.setFormatter(formatter)
# logger = logging.getLogger('uvicorn')
# logger.addHandler(json_handler)
# logger.setLevel(logging.INFO)

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from image_comments.database import crud, models, schemas
from image_comments.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine, checkfirst=True)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get('/settings')
async def test_configs():
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}


@router.get('/comments/', response_model=List[schemas.Comment])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_comments(db, skip=skip, limit=limit)
    return users


# def comment_generator():
#     return [{'id': index, 'author_id': uuid.uuid1(), 'text': 'Test comment ' + str(index)} for index in range(1, 6)]
# # ordering of decorators is very important
# @router.get('/comments')
# def list_comments():
#     # logger.info('function1 has executed',
#     #         extra={
#     #             'job_category': 'test_function',
#     #             'logger.name': 'my_json',
#     #         }
#     #     )
#     #     logger = logging.getLogger("uvicorn")
#     #     print(logger.__dict__)
#     #     print([name for name in logging.root.manager.loggerDict])
#     # import time
#     #
#     # time.sleep(2)
#     #
#     # logger = logging.getLogger("router")
#     # logger.info("THIS IS A INFO LOG", extra={'a': 1})
#
#     return comment_generator()


def test_fallback():
    return {'Detail': 'This is fallback function. Request timed-out'}


@router.get('/timeout/{seconds}')
@fallback(fallback_function=test_fallback)
@func_set_timeout(3)
def test_timeout_feature(seconds: str):
    time.sleep(float(seconds))
    return {'Timeout': seconds, 'Detail': 'Request did not time-out.'}