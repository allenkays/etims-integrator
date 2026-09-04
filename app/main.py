"""Application entry point for the eTIMS integrator service.

This module configures the FastAPI app and wires together the external VSCU
client and the initialization workflow used by the platform.
"""

from fastapi import FastAPI

from app.clients.vscu_client import VSCUClient
from app.config import VSCU_BASE_URL
from app.models.initialization import InitInfoRequest
from app.services.initialization import InitializationService


app = FastAPI(title="eTIMS Integrator")

vscu_client = VSCUClient(
    base_url=VSCU_BASE_URL
)

initialization_service = InitializationService(
    vscu_client=vscu_client
)


@app.post("/initialize")
async def initialize(request: InitInfoRequest):
    """Initialize a device registration request against the upstream VSCU API.

    Args:
        request: The initialization payload containing the device identifiers.

    Returns:
        The serialized response from the VSCU initialization endpoint.
    """
    return await initialization_service.initialize(request)
