from auth.endpoints.auth import api_router as auth_router
from auth.endpoints.health_check import api_router as application_health_router

list_of_routes = [application_health_router, auth_router]
