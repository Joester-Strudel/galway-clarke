# Third-Party Imports
from ninja import Router
from pydantic import BaseModel

# First-Party Imports
from gc_core.api_auth import GlobalAuth


router = Router(tags=["Health"], auth=GlobalAuth())
router.__doc__ = "Health check routes for the GC Users API."


class PingOutSchema(BaseModel):
    message: str


@router.get(
    "/ping/",
    response={200: PingOutSchema},
    operation_id="ping",
)
def ping(request):
    """Simple liveness check that returns a pong message."""
    return {"message": "pong"}
