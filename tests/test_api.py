"""Tests for the FastAPI application endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models.code import CodeResponse
from app.models.initialization import InitInfoResponse
from app.models.item_classification import (
    ItemClassificationData,
    ItemClassificationResponse,
)


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

        with patch(
            "app.main.initialization_service.initialize",
            new_callable=AsyncMock
        ) as mock_init:
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

        # Bad request or validation error
        assert response.status_code in [400, 422]

    def test_response_serialization(self, client, sample_init_response):
        """Test that response is properly serialized."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "dvcSrlNo": "DEVICE001"
        }

        with patch(
            "app.main.initialization_service.initialize",
            new_callable=AsyncMock
        ) as mock_init:
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
            assert (
                data["data"]["info"]["taxpayer"]["taxprNm"]
                ) == "Example Company"

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

            with patch(
                "app.main.initialization_service.initialize",
                new_callable=AsyncMock
            ) as mock_init:
                mock_init.return_value = response_data

                response = client.post("/initialize", json=payload)

                assert response.status_code == 200
                data = response.json()
                assert data["data"]["info"]["taxpayer"]["tin"] == (
                    payload["tin"]
                )

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

        with patch(
            "app.main.initialization_service.initialize",
            new_callable=AsyncMock
        ) as mock_init:
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
        with patch(
            "app.main.initialization_service.initialize",
            new_callable=AsyncMock
        ) as mock_init:
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


@pytest.fixture
def sample_code_response():
    """Create a sample CodeResponse for testing."""
    return CodeResponse(
        resultCd="000",
        resultMsg="Successful",
        resultDt="2024-01-01T12:00:00Z",
        data={
            "clsList": [
                {
                    "cdCls": "04",
                    "cdClsNm": "Tax Type",
                    "useYn": "Y",
                    "dtlList": [
                        {
                            "cd": "A",
                            "cdNm": "AEX",
                            "srtOrd": 1,
                            "useYn": "Y"
                        }
                    ]
                }
            ]
        }
    )


class TestCodesEndpoint:
    """Tests for the /codes endpoint."""

    def test_successful_code_sync(
        self,
        client,
        sample_code_response
    ):
        """Test successful code synchronization."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001",
            "lastReqDt": "20240101120000"
        }

        with patch(
            "app.main.code_service.get_codes",
            new_callable=AsyncMock
        ) as mock_codes:
            mock_codes.return_value = sample_code_response

            response = client.post("/codes", json=payload)

            assert response.status_code == 200

            data = response.json()

            assert data["resultCd"] == "000"
            assert data["resultMsg"] == "Successful"
            assert data["data"]["clsList"][0]["cdCls"] == "04"
            assert (
                data["data"]["clsList"][0]["dtlList"][0]["cd"]
                == "A"
            )

    def test_missing_tin(self, client):
        """Test Code API with missing tin."""
        payload = {
            "bhfId": "BRN001",
            "lastReqDt": "20240101120000"
        }

        response = client.post("/codes", json=payload)

        assert response.status_code == 422

    def test_missing_bhfid(self, client):
        """Test Code API with missing bhfId."""
        payload = {
            "tin": "123456789",
            "lastReqDt": "20240101120000"
        }

        response = client.post("/codes", json=payload)

        assert response.status_code == 422

    def test_missing_last_request_date(self, client):
        """Test Code API with missing lastReqDt."""
        payload = {
            "tin": "123456789",
            "bhfId": "BRN001"
        }

        response = client.post("/codes", json=payload)

        assert response.status_code == 422

    def test_codes_endpoint_method(self, client):
        """Test that /codes only accepts POST."""
        response = client.get("/codes")

        assert response.status_code == 405

    def test_codes_endpoint_exists(self, client):
        """Test that /codes endpoint exists."""
        response = client.post("/codes", json={})

        assert response.status_code == 422


@pytest.fixture
def sample_item_classification_response():
    """Create a sample ItemClassificationResponse for testing."""
    return ItemClassificationResponse(
        resultCd="000",
        resultMsg="Successful",
        resultDt="20260915190000",
        data=ItemClassificationData(itemClsList=[])
    )


class TestItemClassificationEndpoint:
    def test_get_item_classifications(
        self, client,
        sample_item_classification_response,
    ):
        """Test successful item classification request."""
        with patch(
            "app.main.item_classification_service"
            ".get_item_classifications",
            new_callable=AsyncMock,
        ) as mock_service:

            mock_service.return_value = (
                sample_item_classification_response
            )

            response = client.post(
                "/item-classifications",
                json={
                    "tin": "A123456789Z",
                    "bhfId": "00",
                    "lastReqDt": "20180523000000",
                },
            )

        assert response.status_code == 200
        assert response.json()["resultCd"] == "000"
        assert response.json()["resultMsg"] == "Successful"

    def test_missing_tin(self, client):
        """Test item classification request with missing tin."""
        response = client.post(
            "/item-classifications",
            json={
                "bhfId": "00",
                "lastReqDt": "20180523000000",
            },
        )

        assert response.status_code == 422

    def test_missing_bhf_id(self, client):
        """Test item classification request with missing bhfId."""
        response = client.post(
            "/item-classifications",
            json={
                "tin": "A123456789Z",
                "lastReqDt": "20180523000000",
            },
        )

        assert response.status_code == 422

    def test_missing_last_request_date(self, client):
        """Test item classification request with missing lastReqDt."""
        response = client.post(
            "/item-classifications",
            json={
                "tin": "A123456789Z",
                "bhfId": "00",
            },
        )

        assert response.status_code == 422

    def test_get_method_not_allowed(self, client):
        """Test that GET method is not allowed for item classifications."""
        response = client.get("/item-classifications")

        assert response.status_code == 405
