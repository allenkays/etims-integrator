from app.clients.vscu_client import VSCUClient
from app.models.item_classification import (
    ItemClassificationRequest,
    ItemClassificationResponse,
)


class ItemClassificationService:
    """
    A service for interacting with the item classification endpoint.
    """

    def __init__(self, vscu_client: VSCUClient):
        """
        Initialize the item classification service.

        Args:
            vscu_client: An instance of the VSCU client.
        """
        self.vscu_client = vscu_client

    async def get_item_classifications(
        self,
        request: ItemClassificationRequest
    ) -> ItemClassificationResponse:
        """
        Get item classifications based on the provided request.

        Args:
            request: The request model containing the item classification
            criteria.

        Returns:
            The response model containing the item classifications.
        """
        payload = request.model_dump()

        response = await self.vscu_client.get_item_classifications(
            payload
        )

        return response
