"""Application entry point for the eTIMS integrator service.

This module configures the FastAPI app and wires together the external VSCU
client and the initialization workflow used by the platform.
"""

from fastapi import FastAPI

from app.clients.vscu_client import VSCUClient
from app.config import VSCU_BASE_URL
from app.models.code import CodeRequest
from app.models.initialization import InitInfoRequest
from app.models.item_classification import (
    ItemClassificationRequest,
)
from app.services.code import CodeService
from app.services.initialization import InitializationService
from app.services.item_classification import (
    ItemClassificationService,
)


app = FastAPI(title="eTIMS Integrator")

vscu_client = VSCUClient(
    base_url=VSCU_BASE_URL
)

initialization_service = InitializationService(
    vscu_client=vscu_client
)

code_service = CodeService(
    vscu_client=vscu_client
)

item_classification_service = ItemClassificationService(
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


@app.post("/codes")
async def get_codes(request: CodeRequest):
    """Fetch code data from the upstream VSCU API.

    Args:
        request: The code request payload containing the request parameters.
    Returns:
        The serialized response from the VSCU code endpoint.
    """
    return await code_service.get_codes(request)


@app.post("/item-classifications")
async def get_item_classifications(
    request: ItemClassificationRequest
):
    """Fetch item classification data from the upstream VSCU API.

    Args:
        request: The item classification request payload containing the request
        parameters.

    Returns:
        The serialized response from the VSCU item classification endpoint.
    """
    return await item_classification_service.get_item_classifications(
        request
    )
