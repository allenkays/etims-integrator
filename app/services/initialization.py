"""Service layer for the initialization process.

The service converts the validated API request model into the payload required
by the upstream VSCU client and returns the response unchanged to the caller.
"""

from app.clients.vscu_client import VSCUClient
from app.models.initialization import (
    InitInfoRequest,
    InitInfoResponse,
)


class InitializationService:
    """Business logic for initialization requests."""

    def __init__(self, vscu_client: VSCUClient):
        """Create the initialization service with a configured VSCU client.

        Args:
            vscu_client: Client used to send initialization requests upstream.
        """
        self.vscu_client = vscu_client

    async def initialize(self, request: InitInfoRequest) -> InitInfoResponse:
        """Run initialization using the request model provided by the API.

        Args:
            request: Validated initialization request payload.

        Returns:
            The JSON response returned from the VSCU initialization endpoint.
        """
        payload = request.model_dump()

        response = await self.vscu_client.initialize(
            payload
        )

        return response
