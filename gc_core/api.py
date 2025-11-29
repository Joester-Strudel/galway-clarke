# Python Imports
import logging

# Django Imports
from django.contrib.admin.views.decorators import staff_member_required

# Third-Party Imports
from ninja import NinjaAPI

# First-Party Imports
from gc_core.api_auth import GlobalAuth
from gc_users.api import gc_users_router


logger = logging.getLogger(__name__)

# Global API Object
api = NinjaAPI(
    title="Galway Clarke API",
    description="The official Galway Clarke API documentation.",
    version="1.0.0",
    urls_namespace="galway-api",
    docs_decorator=staff_member_required,
    auth=GlobalAuth(),
)

# Router Registrations
routers = {
    "gc-users": gc_users_router,
}

for path, router in routers.items():
    api.add_router(f"/{path}", router)


__all__ = ["api"]
