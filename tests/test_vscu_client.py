"""Tests for the VSCU HTTP client."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from app.clients.vscu_client import VSCUClient
from app.models.initialization import InitInfoResponse


@pytest.fixture
def vscu_client():
    """Create a VSCUClient instance for testing."""
    return VSCUClient(base_url="http://localhost:8088")


class TestVSCUClientInitialization:
    """Tests for VSCUClient initialization."""

    def test_client_creation(self):
        """Test creating a VSCUClient."""
        client = VSCUClient(base_url="http://localhost:8088")
        assert client.base_url == "http://localhost:8088"

    def test_client_strips_trailing_slash(self):
        """Test that client strips trailing slashes from base URL."""
        client = VSCUClient(base_url="http://localhost:8088/")
        assert client.base_url == "http://localhost:8088"

    def test_client_with_multiple_trailing_slashes(self):
        """Test that client strips multiple trailing slashes."""
        client = VSCUClient(base_url="http://localhost:8088///")
        assert client.base_url == "http://localhost:8088"


@pytest.mark.asyncio
class TestVSCUClientInitialize:
    """Tests for the VSCUClient.initialize method."""

    async def test_successful_initialization(self, vscu_client):
        """Test successful initialization request."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        mock_response_data = {
            "resultCd": "00",
            "resultMsg": "Success",
            "resultDt": "2024-01-01T12:00:00Z",
            "data": {
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
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client
                )

            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_client.post = AsyncMock(return_value=mock_response)

            response = await vscu_client.initialize(payload)

            assert isinstance(response, InitInfoResponse)
            assert response.resultCd == "00"
            assert response.data.info.taxpayer.tin == "123456789"
            assert response.data.info.device.dvcId == "DEVICE001"
            mock_client.post.assert_called_once()

    async def test_initialization_error_handling(self, vscu_client):
        """Test error handling when VSCU returns an error status."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client
                )

            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "500 Server Error",
                request=MagicMock(),
                response=mock_response
            )
            mock_client.post = AsyncMock(return_value=mock_response)

            with pytest.raises(httpx.HTTPStatusError):
                await vscu_client.initialize(payload)

    async def test_correct_url_construction(self, vscu_client):
        """Test that the correct URL is constructed."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        mock_response_data = {
            "resultCd": "00",
            "resultMsg": "Success",
            "resultDt": "2024-01-01T12:00:00Z",
            "data": {
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
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client
                )

            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_client.post = AsyncMock(return_value=mock_response)

            await vscu_client.initialize(payload)

            expected_url = "http://localhost:8088/initializer/selectInitInfo"
            mock_client.post.assert_called_once_with(
                expected_url,
                json=payload
            )

    async def test_payload_passed_correctly(self, vscu_client):
        """Test that payload is passed correctly to the request."""
        payload = {
            "tin": "987654321",
            "bhfId": "BRN002",
            "dvcSrlNo": "DEVICE002"
        }

        mock_response_data = {
            "resultCd": "00",
            "resultMsg": "Success",
            "resultDt": "2024-01-01T12:00:00Z",
            "data": {
                "info": {
                    "taxpayer": {
                        "tin": "987654321",
                        "taxprNm": "Another Company",
                        "bsnsActv": "Services"
                    },
                    "branch": {
                        "bhfId": "BRN002",
                        "bhfNm": "Branch 2",
                        "bhfOpenDt": "2021-01-01",
                        "prvncNm": "Kigali",
                        "dstrtNm": "Kicukiro",
                        "sctrNm": "Gisozi",
                        "locDesc": "Secondary office",
                        "hqYn": "N",
                        "mgrNm": "Jane Doe",
                        "mgrTelNo": "250788654321",
                        "mgrEmail": "jane@example.com"
                    },
                    "device": {
                        "dvcId": "DEVICE002"
                    }
                }
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client
                )

            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_client.post = AsyncMock(return_value=mock_response)

            await vscu_client.initialize(payload)

            call_args = mock_client.post.call_args
            assert call_args.kwargs["json"] == payload
