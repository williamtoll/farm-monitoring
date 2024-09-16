from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from appberry.security.api_key import check_api_key

api_key_header = APIKeyHeader(name="X-API-Key")

def get_user(api_key_header: str = Security(api_key_header)):
    if check_api_key(api_key_header):
        return "Authenticated"
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )

