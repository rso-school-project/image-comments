import time

from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from func_timeout import func_set_timeout
from sqlalchemy.orm import Session


from image_comments import settings
from image_comments.utils import fallback
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


@router.get('/comments/', response_model=List[schemas.Comment])
def read_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # NOTE: this is importat for logging.
    #       we get unique_log_id as a header in request object.
    #       unique_log_id = request.header.get('unique_log_id')
    #       Use this log id, when calling another microservice from here.
    users = crud.get_comments(db, skip=skip, limit=limit)
    return users


@router.get('/settings')
async def test_configs(request: Request):
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}


def test_fallback():
    return {'Detail': 'This is fallback function. Request timed-out'}


@router.get('/timeout/{seconds}')
@fallback(fallback_function=test_fallback)
@func_set_timeout(3)
def test_timeout_feature(seconds: str):
    time.sleep(float(seconds))
    return {'Timeout': seconds, 'Detail': 'Request did not time-out.'}
