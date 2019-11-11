from fastapi import APIRouter
from image_comments import settings

router = APIRouter()


@router.get("/comments/")
async def get_all_comments():
    return {"message": f"Hello world...  {settings.test_x}"}
