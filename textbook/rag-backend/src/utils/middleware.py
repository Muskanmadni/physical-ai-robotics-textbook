from fastapi import Request
from fastapi.responses import Response

async def add_custom_headers(request: Request, call_next):
    """
    Middleware to add custom headers to responses
    """
    response = await call_next(request)
    response.headers["X-API-Version"] = "1.0.0"  # API version header
    response.headers["X-Content-Type-Options"] = "nosniff"  # Security header
    response.headers["X-Frame-Options"] = "DENY"  # Security header
    return response

# Additional middleware can be defined here as needed