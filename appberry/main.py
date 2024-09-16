from fastapi import Depends, FastAPI
from appberry.routers import irrigation, health, version
from appberry.security.auth import get_user

app = FastAPI()

# Public routes
app.include_router(
    health.router,
    prefix="/api/openfarm"
)

app.include_router(
    version.router,
    prefix="/api/openfarm"
)


# Secure routes
app.include_router(
    irrigation.router,
    prefix="/api/openfarm",
    dependencies=[Depends(get_user)],
)
