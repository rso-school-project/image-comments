import os
import etcd3

from fastapi import FastAPI


app = FastAPI()
etcd_client = etcd3.client(host='etcd', port='2379')

# on initial setup populate enviroment variables from config server.
for value, metadata in etcd_client.get_range(range_start="/image_comments/", range_end="/image_comments0"):
    key, value = metadata.key.decode('utf-8'), value.decode('utf-8')
    config_var_name = os.path.basename(key)
    os.environ[config_var_name] = value


# this import must be after we set enviroment variables
from image_comments import settings


def etcd_watch_callback(event):
    key, value = event.key.decode('utf-8'), event.value.decode('utf-8')
    # zamiži na eno oko in pojdi naprej.
    settings.__dict__[os.path.basename(key)] = value


etcd_client.add_watch_callback(key="/image_comments/", range_end="/image_comments0", callback=etcd_watch_callback)


@app.get("/")
async def root():
    return {"message": f"Hello world...  {settings.test_x} {__name__}"}
