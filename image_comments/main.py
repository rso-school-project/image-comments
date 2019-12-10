from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

from .routers import comments
from .utils import check_liveness, check_readiness

VERSION = '1.1.0'
API_VERSION = 'v1'
PREFIX = f'/api/{API_VERSION}/comments'


app = FastAPI(
    title='image-comments',
    description='Microservice for handling image comments',
    version=VERSION,
    openapi_url=f'{PREFIX}/openapi.json',
)


app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics/', metrics)

app.include_router(
    comments.router, prefix=PREFIX, responses={404: {'description': 'Not found'}},
)

app.add_route('/health/live', check_liveness)
app.add_route('/health/ready', check_readiness)
