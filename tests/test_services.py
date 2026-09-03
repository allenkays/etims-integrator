"""Tests for the initialization service."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.initialization import InitializationService
from app.clients.vscu_client import VSCUClient
from app.models.initialization import (
    InitInfoRequest,
    InitInfoResponse,
    InitTaxpayer,
    InitBranch,
    InitDevice,
)


@pytest.fixture
def mock_vscu_client():
    """Create a mock VSCUClient for testing."""
    return MagicMock(spec=VSCUClient)


@pytest.fixture
def initialization_service(mock_vscu_client):
    """Create an InitializationService with a mocked client."""
    return InitializationService(vscu_client=mock_vscu_client)


class TestInitializationServiceInit:
    """Tests for InitializationService initialization."""

    def test_service_creation(self, mock_vscu_client):
        """Test creating an InitializationService."""
        service = InitializationService(vscu_client=mock_vscu_client)
        assert service.vscu_client == mock_vscu_client

    def test_service_requires_vscu_client(self):
        """Test that service requires a VSCU client."""
        with pytest.raises(TypeError):
            InitializationService()


@pytest.mark.asyncio
class TestInitializationServiceInitialize:
    """Tests for the InitializationService.initialize method."""

    async def test_successful_initialization(self, initialization_service, mock_vscu_client):
        """Test successful initialization."""
        request = InitInfoRequest(
            tin="123456789",
            bhfId="BRN001",
            dvcSrlNo="DEVICE001"
        )

        # Create a mock response
        mock_response = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "info": {
                    "taxpayer": {
                        "tin": "123456789",
                        "taxprNm": "Example Company",
                        "bsnsActv": "Manufacturing"
                    },
                    "branch": {
                        "bhfId": "BRN001",
                        "bhfNm": "Main Branch",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Gasabo",
                        "sctrNm": "Gacuriro",
                        "locDesc": "Main office location",
                        "hqYn": "Y",
                        "mgrNm": "John Doe",
                        "mgrTelNo": "250788123456",
                        "mgrEmail": "john@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE001",
                        "lastSaleInvcNo": 100
                    }
                }
            }
        )

        mock_vscu_client.initialize = AsyncMock(return_value=mock_response)

        response = await initialization_service.initialize(request)

        assert isinstance(response, InitInfoResponse)
        assert response.resultCd == "00"
        assert response.data.info.taxpayer.tin == "123456789"
        assert response.data.info.device.dvcId == "DEVICE001"
        mock_vscu_client.initialize.assert_called_once()

    async def test_request_payload_conversion(self, initialization_service, mock_vscu_client):
        """Test that request is correctly converted to payload."""
        request = InitInfoRequest(
            tin="123456789",
            bhfId="BRN001",
            dvcSrlNo="DEVICE001"
        )

        mock_response = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "info": {
                    "taxpayer": {
                        "tin": "123456789",
                        "taxprNm": "Example Company",
                        "bsnsActv": "Manufacturing"
                    },
                    "branch": {
                        "bhfId": "BRN001",
                        "bhfNm": "Main Branch",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Gasabo",
                        "sctrNm": "Gacuriro",
                        "locDesc": "Main office location",
                        "hqYn": "Y",
                        "mgrNm": "John Doe",
                        "mgrTelNo": "250788123456",
                        "mgrEmail": "john@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE001"
                    }
                }
            }
        )

        mock_vscu_client.initialize = AsyncMock(return_value=mock_response)

        await initialization_service.initialize(request)

        # Verify that the client was called with a dictionary payload
        call_args = mock_vscu_client.initialize.call_args
        payload = call_args[0][0]

        assert isinstance(payload, dict)
        assert payload["tin"] == "123456789"
        assert payload["bhfId"] == "BRN001"
        assert payload["dvcSrlNo"] == "DEVICE001"

    async def test_response_returned_unchanged(self, initialization_service, mock_vscu_client):
        """Test that service returns client response unchanged."""
        request = InitInfoRequest(
            tin="123456789",
            bhfId="BRN001",
            dvcSrlNo="DEVICE001"
        )

        mock_response = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "info": {
                    "taxpayer": {
                        "tin": "123456789",
                        "taxprNm": "Example Company",
                        "bsnsActv": "Manufacturing"
                    },
                    "branch": {
                        "bhfId": "BRN001",
                        "bhfNm": "Main Branch",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Gasabo",
                        "sctrNm": "Gacuriro",
                        "locDesc": "Main office location",
                        "hqYn": "Y",
                        "mgrNm": "John Doe",
                        "mgrTelNo": "250788123456",
                        "mgrEmail": "john@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE001",
                        "lastSaleInvcNo": 100,
                        "lastPchsInvcNo": 50
                    }
                }
            }
        )

        mock_vscu_client.initialize = AsyncMock(return_value=mock_response)

        response = await initialization_service.initialize(request)

        # Verify response is the same object
        assert response == mock_response
        assert response.data.info.device.lastPchsInvcNo == 50

    async def test_different_request_payloads(self, initialization_service, mock_vscu_client):
        """Test service with different request payloads."""
        test_cases = [
            {
                "tin": "111111111",
                "bhfId": "BRN001",
                "dvcSrlNo": "DEVICE001"
            },
            {
                "tin": "222222222",
                "bhfId": "BRN002",
                "dvcSrlNo": "DEVICE002"
            },
        ]

        mock_response = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "info": {
                    "taxpayer": {
                        "tin": "123456789",
                        "taxprNm": "Example Company",
                        "bsnsActv": "Manufacturing"
                    },
                    "branch": {
                        "bhfId": "BRN001",
                        "bhfNm": "Main Branch",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Gasabo",
                        "sctrNm": "Gacuriro",
                        "locDesc": "Main office location",
                        "hqYn": "Y",
                        "mgrNm": "John Doe",
                        "mgrTelNo": "250788123456",
                        "mgrEmail": "john@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE001"
                    }
                }
            }
        )

        mock_vscu_client.initialize = AsyncMock(return_value=mock_response)

        for test_case in test_cases:
            request = InitInfoRequest(**test_case)
            await initialization_service.initialize(request)

        # Verify client was called twice
        assert mock_vscu_client.initialize.call_count == 2
