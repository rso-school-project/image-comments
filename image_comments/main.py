import os
import etcd3

from fastapi import FastAPI
from .routers import comments


app_name = 'image_comments'

app = FastAPI(
    title='image-comments',
    description='Microservice for handling image comments',
    version='1.0.0',
    openapi_url='/api/v1/openapi.json')

etcd = etcd3.client(host='etcd', port='2379')

# on initial setup populate environment variables from config server.
for value, metadata in etcd.get_range(range_start=f'/{app_name}/', range_end=f'/{app_name}0'):
    key, value = metadata.key.decode('utf-8'), value.decode('utf-8')
    config_var_name = os.path.basename(key)
    os.environ[config_var_name] = value


# this import must be after we set environment variables
from image_comments import settings


def etcd_watch_callback(event):
    etcd_key, etcd_value = event.key.decode('utf-8'), event.value.decode('utf-8')
    # zamiži na eno oko in pojdi naprej.
    settings.__dict__[os.path.basename(etcd_key)] = etcd_value


etcd.add_watch_callback(key=f'/{app_name}/',
                        range_end=f'/{app_name}0',
                        callback=etcd_watch_callback)


app.include_router(
    comments.router,
    prefix='/api/v1',
    responses={404: {'description': 'Not found'}},
)


