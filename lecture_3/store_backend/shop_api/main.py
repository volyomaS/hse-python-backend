from fastapi import FastAPI

from store_backend.shop_api.routes import router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Shop API")

app.include_router(router)

Instrumentator().instrument(app).expose(app)
