from app.clients.vscu_client import VSCUClient
from app.models.code import CodeRequest, CodeResponse


class CodeService:
    def __init__(self, vscu_client: VSCUClient):
        self.vscu_client = vscu_client

    async def get_codes(self, request: CodeRequest) -> CodeResponse:
        """Fetch code data from the VSCU service.

        Args:
            request: A CodeRequest object containing the request parameters.
            lastReqDt: The last request date in 'YYYY-MM-DD' format.

        Returns:
            A CodeResponse object containing the code data.

        Raises:
            httpx.HTTPStatusError: If the remote service responds with an
            error.
        """
        payload = request.model_dump()
        response = await self.vscu_client.get_codes(payload)
        return response
