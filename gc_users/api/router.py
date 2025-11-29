# Third-Party Imports
from ninja import NinjaAPI

# First-Party Imports
from gc_users.api.ping import router as ping_router


api = NinjaAPI()

# Mount routes
api.add_router("", ping_router)

__all__ = ["api"]
