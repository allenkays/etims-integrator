"""HTTP client for communicating with the VSCU service.

This client encapsulates the details of the initialization endpoint used by
the integrator when registering or initializing a device.
"""

import httpx
from app.models.initialization import InitInfoResponse


class VSCUClient:
    """Thin async wrapper around the VSCU REST API."""

    def __init__(self, base_url: str):
        """Create a VSCU client bound to a specific base URL.

        Args:
            base_url: The root URL of the VSCU service.
        """
        self.base_url = base_url.rstrip("/")

    async def initialize(self, payload: dict) -> InitInfoResponse:
        """Send initialization data to the VSCU selectInitInfo endpoint.

        Args:
            payload: JSON payload containing the initialization request data.

        Returns:
            The decoded JSON response returned by the upstream API.

        Raises:
            httpx.HTTPStatusError: If the remote service responds with an
            error.
        """
        url = f"{self.base_url}/initializer/selectInitInfo"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload
            )

        response.raise_for_status()

        return InitInfoResponse.model_validate(
            response.json()
        )
