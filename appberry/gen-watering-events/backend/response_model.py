from pydantic import BaseModel
from typing import Optional, Any

class APIResponse(BaseModel):
    status: str  # e.g., 'success' or 'error'
    message: str  # A short message about the operation
    result: Optional[Any] = None  # The actual data (if successful)
    error_reason: Optional[str] = None  # The reason for the failure (if any)
