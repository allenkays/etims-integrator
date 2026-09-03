"""Tests for the FastAPI application endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from app.main import app
from app.models.initialization import InitInfoResponse


@pytest.fixture
def client():
    """Create a FastAPI TestClient."""
    return TestClient(app)


@pytest.fixture
def sample_init_response():
    """Create a sample InitInfoResponse for testing."""
    return InitInfoResponse(
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


class TestInitializeEndpoint:
    """Tests for the /initialize endpoint."""

    def test_successful_initialization(self, client, sample_init_response):
        """Test successful initialization request."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        with patch("app.main.initialization_service.initialize", new_callable=AsyncMock) as mock_init:
            mock_init.return_value = sample_init_response

            response = client.post("/initialize", json=payload)

            assert response.status_code == 200
            data = response.json()
            assert data["resultCd"] == "00"
            assert data["data"]["info"]["device"]["dvcId"] == "DEVICE001"

    def test_missing_required_field_tin(self, client):
        """Test initialization with missing tin field."""
        payload = {
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        response = client.post("/initialize", json=payload)

        assert response.status_code == 422  # Validation error

    def test_missing_required_field_bhfid(self, client):
        """Test initialization with missing bhfId field."""
        payload = {
            "tin": "123456789",
            "dvcSrlNo": "DEVICE001"
        }

        response = client.post("/initialize", json=payload)

        assert response.status_code == 422  # Validation error

    def test_missing_required_field_dvcsrlno(self, client):
        """Test initialization with missing dvcSrlNo field."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001"
        }

        response = client.post("/initialize", json=payload)

        assert response.status_code == 422  # Validation error

    def test_empty_payload(self, client):
        """Test initialization with empty payload."""
        response = client.post("/initialize", json={})

        assert response.status_code == 422  # Validation error

    def test_malformed_json(self, client):
        """Test initialization with malformed JSON."""
        response = client.post(
            "/initialize",
            content="not json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code in [400, 422]  # Bad request or validation error

    def test_response_serialization(self, client, sample_init_response):
        """Test that response is properly serialized."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        with patch("app.main.initialization_service.initialize", new_callable=AsyncMock) as mock_init:
            mock_init.return_value = sample_init_response

            response = client.post("/initialize", json=payload)

            assert response.status_code == 200
            data = response.json()

            # Verify structure
            assert "resultCd" in data
            assert "resultMsg" in data
            assert "resultDt" in data
            assert "data" in data

            # Verify result fields
            assert data["resultCd"] == "00"
            assert data["resultMsg"] == "Success"

            # Verify data structure
            assert "info" in data["data"]
            assert "taxpayer" in data["data"]["info"]
            assert "branch" in data["data"]["info"]
            assert "device" in data["data"]["info"]

            # Verify taxpayer data
            assert data["data"]["info"]["taxpayer"]["tin"] == "123456789"
            assert data["data"]["info"]["taxpayer"]["taxprNm"] == "Example Company"

            # Verify branch data
            assert data["data"]["info"]["branch"]["bhfId"] == "BRN001"
            assert data["data"]["info"]["branch"]["hqYn"] == "Y"

            # Verify device data
            assert data["data"]["info"]["device"]["dvcId"] == "DEVICE001"

    def test_different_request_data(self, client):
        """Test initialization with different request data."""
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

        for payload in test_cases:
            response_data = InitInfoResponse(
                resultCd="00",
                resultMsg="Success",
                resultDt="2024-01-01T12:00:00Z",
                data={
                    "info": {
                        "taxpayer": {
                            "tin": payload["tin"],
                            "taxprNm": "Test Company",
                            "bsnsActv": "Testing"
                        },
                        "branch": {
                            "bhfId": payload["bhfId"],
                            "bhfNm": "Test Branch",
                            "bhfOpenDt": "2020-01-01",
                            "prvncNm": "Test Province",
                            "dstrtNm": "Test District",
                            "sctrNm": "Test Sector",
                            "locDesc": "Test Location",
                            "hqYn": "Y",
                            "mgrNm": "Test Manager",
                            "mgrTelNo": "250700000000",
                            "mgrEmail": "test@example.com"
                        },
                        "device": {
                            "dvcId": payload["dvcSrlNo"]
                        }
                    }
                }
            )

            with patch("app.main.initialization_service.initialize", new_callable=AsyncMock) as mock_init:
                mock_init.return_value = response_data

                response = client.post("/initialize", json=payload)

                assert response.status_code == 200
                data = response.json()
                assert data["data"]["info"]["taxpayer"]["tin"] == payload["tin"]

    def test_special_characters_in_fields(self, client):
        """Test initialization with special characters in fields."""
        payload = {
            "tin": "123-456-789",
            "bhfId": "BRN/001",
            "dvcSrlNo": "DEVICE_001"
        }

        response_data = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z",
            data={
                "info": {
                    "taxpayer": {
                        "tin": payload["tin"],
                        "taxprNm": "Company & Co.",
                        "bsnsActv": "Manufacturing & Services"
                    },
                    "branch": {
                        "bhfId": payload["bhfId"],
                        "bhfNm": "Main Branch (HQ)",
                        "bhfOpenDt": "2020-01-01",
                        "prvncNm": "Kigali/City",
                        "dstrtNm": "Test District",
                        "sctrNm": "Test Sector",
                        "locDesc": "Location with \"quotes\"",
                        "hqYn": "Y",
                        "mgrNm": "John Doe-Smith",
                        "mgrTelNo": "250-788-123-456",
                        "mgrEmail": "john.doe@example.co.uk"
                    },
                    "device": {
                        "dvcId": payload["dvcSrlNo"]
                    }
                }
            }
        )

        with patch("app.main.initialization_service.initialize", new_callable=AsyncMock) as mock_init:
            mock_init.return_value = response_data

            response = client.post("/initialize", json=payload)

            assert response.status_code == 200

    def test_endpoint_method_is_post(self, client):
        """Test that endpoint only accepts POST requests."""
        # GET should not be allowed
        response = client.get("/initialize")
        assert response.status_code == 405  # Method not allowed

        # DELETE should not be allowed
        response = client.delete("/initialize")
        assert response.status_code == 405

    def test_endpoint_path_is_initialize(self, client):
        """Test that the endpoint is at /initialize."""
        # Mock the initialization service
        response_data = InitInfoResponse(
            resultCd="00",
            resultMsg="Success",
            resultDt="2024-01-01T12:00:00Z"
        )

        # Correct path
        with patch("app.main.initialization_service.initialize", new_callable=AsyncMock) as mock_init:
            mock_init.return_value = response_data

            response = client.post("/initialize", json={
                "tin": "123456789",
                "bhfId": "BRN001",
                "dvcSrlNo": "DEVICE001"
            })
            # Will succeed with mock
            assert response.status_code == 200

        # Wrong path
        response = client.post("/init", json={
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        })
        assert response.status_code == 404  # Not found


class TestAppMetadata:
    """Tests for FastAPI app metadata."""

    def test_app_title(self):
        """Test that app has the correct title."""
        assert app.title == "eTIMS Integrator"

    def test_app_has_routes(self):
        """Test that app has the expected routes."""
        routes = [route.path for route in app.routes]
        assert "/initialize" in routes
