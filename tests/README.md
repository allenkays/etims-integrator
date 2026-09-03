# Test Suite for eTIMS Integrator

This directory contains comprehensive tests for the eTIMS integrator application.

## Test Files

### `test_models.py`
Tests for Pydantic data models:
- **TestInitInfoRequest**: Tests for initialization request model validation
- **TestInitTaxpayer**: Tests for taxpayer model validation
- **TestInitBranch**: Tests for branch model validation
- **TestInitDevice**: Tests for device model validation
- **TestInitInfoResponse**: Tests for initialization response model validation

Includes tests for:
- Valid model creation
- Required field validation
- Optional field defaults
- Model serialization and deserialization

### `test_vscu_client.py`
Tests for the VSCU HTTP client:
- **TestVSCUClientInitialization**: Tests for client initialization
  - URL handling (trailing slash removal)
  - Base URL configuration
- **TestVSCUClientInitialize**: Tests for the initialize method
  - Successful HTTP requests
  - Error handling for HTTP errors
  - Correct URL construction
  - Payload passing

Includes async tests with mocked HTTP responses using `AsyncMock`.

### `test_services.py`
Tests for the initialization service layer:
- **TestInitializationServiceInit**: Tests for service initialization
- **TestInitializationServiceInitialize**: Tests for the initialize method
  - Request payload conversion to dictionary
  - Response pass-through behavior
  - Correct service orchestration
  - Multiple request handling

Includes async tests with mocked VSCU client.

### `test_api.py`
Tests for FastAPI endpoints:
- **TestInitializeEndpoint**: Tests for the /initialize POST endpoint
  - Successful initialization requests
  - Validation error handling for missing fields
  - Malformed JSON handling
  - Response serialization
  - Special characters handling
  - HTTP method validation
- **TestAppMetadata**: Tests for FastAPI app metadata
  - App title verification
  - Route availability

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install pytest pytest-asyncio httpx
```

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_models.py
pytest tests/test_vscu_client.py
pytest tests/test_services.py
pytest tests/test_api.py
```

### Run Specific Test Class
```bash
pytest tests/test_models.py::TestInitInfoRequest
pytest tests/test_vscu_client.py::TestVSCUClientInitialize
```

### Run Specific Test
```bash
pytest tests/test_models.py::TestInitInfoRequest::test_valid_request
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run with Coverage Report
```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

### Run Only Async Tests
```bash
pytest tests/ -k "asyncio"
```

## Test Coverage

The test suite provides coverage for:

1. **Models (app/models/initialization.py)**
   - InitInfoRequest validation
   - InitTaxpayer validation
   - InitBranch validation
   - InitDevice validation (required and optional fields)
   - InitInfoResponse validation and deserialization

2. **Client (app/clients/vscu_client.py)**
   - HTTP request construction and URL building
   - Payload handling
   - Response parsing
   - Error handling

3. **Services (app/services/initialization.py)**
   - Request-to-payload conversion
   - Service orchestration
   - Response handling

4. **API Endpoints (app/main.py)**
   - Request validation
   - Response serialization
   - HTTP method enforcement
   - Route availability

## Key Testing Patterns

### Async Testing
Tests using async functions are marked with `@pytest.mark.asyncio` decorator:
```python
@pytest.mark.asyncio
async def test_async_operation():
    ...
```

### Mocking
- HTTP requests are mocked using `unittest.mock.AsyncMock` and `patch`
- Service dependencies are mocked to isolate unit tests
- FastAPI's `TestClient` is used for endpoint testing

### Fixtures
- `client`: Provides a FastAPI TestClient for endpoint testing
- `vscu_client`: Provides a VSCUClient instance
- `mock_vscu_client`: Provides a mocked VSCUClient
- `initialization_service`: Provides an InitializationService with mocked dependencies
- `sample_init_response`: Provides sample response data

## Future Improvements

Potential enhancements to the test suite:
- [ ] Integration tests with actual VSCU API (with test server)
- [ ] Performance/load testing
- [ ] Test data factories for more complex scenarios
- [ ] Parameterized tests for edge cases
- [ ] Contract testing with API documentation
