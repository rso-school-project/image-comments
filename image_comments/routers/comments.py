import uuid

# import logging

from fastapi import APIRouter
from image_comments import settings

# import json_log_formatter

#
# formatter = json_log_formatter.JSONFormatter()
# json_handler = logging.StreamHandler()
# json_handler.setFormatter(formatter)
# logger = logging.getLogger('uvicorn')
# logger.addHandler(json_handler)
# logger.setLevel(logging.INFO)


router = APIRouter()


@router.get('/settings')
async def test_configs():
    return {"Config for X:": f"{settings.config_x}", "Config for Y:": f"{settings.config_y}"}


def comment_generator():
    return [{'id': index, 'author_id': uuid.uuid1(), 'text': 'Test comment ' + str(index)} for index in range(1, 6)]


# ordering of decorators is very important
@router.get('/')
def list_comments():
    # logger.info('function1 has executed',
    #         extra={
    #             'job_category': 'test_function',
    #             'logger.name': 'my_json',
    #         }
    #     )
    #     logger = logging.getLogger("uvicorn")
    #     print(logger.__dict__)
    #     print([name for name in logging.root.manager.loggerDict])
    # import time
    #
    # time.sleep(2)
    #
    # logger = logging.getLogger("router")
    # logger.info("THIS IS A INFO LOG", extra={'a': 1})

    return comment_generator()
