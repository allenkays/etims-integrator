# KRA eTIMS VSCU Integrator

A Python/FastAPI system-to-system integration service for connecting a taxpayer's business application or ERP system to the Kenya Revenue Authority (KRA) Electronic Tax Invoice Management System (eTIMS) through the Virtual Sales Control Unit (VSCU).

## Overview

The eTIMS Integrator acts as the integration layer between a taxpayer's internal business system and the KRA eTIMS VSCU application.

The application is responsible for:

- Receiving transaction and master-data information from a business system
- Validating and transforming data into the format expected by VSCU
- Communicating with the locally deployed KRA VSCU service
- Processing VSCU responses
- Persisting relevant eTIMS information
- Managing transaction states, errors, retries, and reconciliation

The project is being developed against the KRA eTIMS VSCU technical specifications and is intended for sandbox development and testing before production certification.

## Architecture

The intended integration architecture is:

```text
┌───────────────────────────────┐
│       Business System         │
│       / ERP / POS             │
└───────────────┬───────────────┘
                │
                │ HTTP / JSON
                ▼
┌───────────────────────────────┐
│      eTIMS Integrator         │
│                               │
│      Python / FastAPI         │
│      localhost:8000           │
└───────────────┬───────────────┘
                │
                │ HTTP / JSON
                ▼
┌───────────────────────────────┐
│          KRA VSCU             │
│                               │
│       Java application        │
│       localhost:8088          │
└───────────────┬───────────────┘
                │
                │ HTTPS
                ▼
┌───────────────────────────────┐
│          KRA eTIMS            │
│        Sandbox / API          │
└───────────────────────────────┘
```

The VSCU application is deployed locally by the taxpayer, while this project provides the integration layer that communicates with it.

## Technology Stack

- Python 3.10+
- FastAPI
- Pydantic
- HTTPX
- Uvicorn
- pytest
- pytest-asyncio
- pytest-cov
- Flake8
- uv

## Project Structure

```text
etims-integrator/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── clients/
│   │   └── vscu_client.py
│   ├── models/
│   │   └── initialization.py
│   ├── services/
│   │   └── initialization.py
│   ├── config.py
│   └── main.py
├── docs/
├── tests/
├── .env
├── .gitignore
├── CONTRIBUTING.md
├── README.md
├── pyproject.toml
└── uv.lock
```

The project structure will grow as additional eTIMS functionality is implemented.

## Current Implementation

The current implementation establishes the foundation for communicating with VSCU.

### Device Initialization

The first implemented VSCU operation is device initialization.

The integrator exposes:

```text
POST /initialize
```

The request contains:

```json
{
  "tin": "A123456789Z",
  "bhfId": "00",
  "dvcSrlNo": "dvcv1130"
}
```

The integrator forwards the request to the VSCU initialization endpoint:

```text
POST /initializer/selectInitInfo
```

The VSCU response is validated using Pydantic models before being returned by the integrator.

## VSCU Operations

The integration will progressively implement the major VSCU operations defined by the KRA technical specification.

Planned areas include:

1. Device initialization
2. Code data
3. Item classification
4. Branch information
5. Customer information
6. Notices
7. Item information
8. Imported items
9. Sales transactions and invoices
10. Purchase transactions
11. Stock management
12. Error handling and retry mechanisms
13. Transaction reconciliation

## Transaction Processing

eTIMS transactions require more than simply sending an HTTP request.

The integrator will distinguish between transport-level success and eTIMS business-level success.

For example:

```text
HTTP 200
   │
   ▼
VSCU response received
   │
   ▼
Check resultCd
   │
   ├── 000 → Successful eTIMS operation
   │
   └── Other → eTIMS/business error
```

Transactions will eventually be tracked through explicit states such as:

```text
PENDING
   ↓
SENT
   ↓
KRA_ACCEPTED
   ↓
RECEIPT_GENERATED
   ↓
COMPLETED
```

with failure and retry states handled separately.

## Configuration

The VSCU base URL is configured through an environment variable.

Example `.env`:

```env
VSCU_BASE_URL=http://localhost:8088
```

The default development configuration assumes that the VSCU service is running locally on port `8088`.

Do not commit credentials, cryptographic keys, or other sensitive configuration to Git.

## Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/allenkays/etims-integrator.git
cd etims-integrator
```

### 2. Install uv

Install `uv` using the official installation method for your operating system.

### 3. Install project dependencies

```bash
uv sync
```

This creates/synchronizes the project's virtual environment using:

```text
pyproject.toml
uv.lock
```

### 4. Run tests

```bash
uv run pytest -q
```

### 5. Run linting

```bash
uv run flake8 app tests
```

### 6. Start the development server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Dependency Management

This project uses `uv` for dependency and virtual-environment management.

Runtime dependencies are defined in:

```text
pyproject.toml
```

The lock file is:

```text
uv.lock
```

Add a runtime dependency:

```bash
uv add package-name
```

Add a development dependency:

```bash
uv add --dev package-name
```

Synchronize the environment:

```bash
uv sync
```

Run project commands:

```bash
uv run <command>
```

## Testing and Continuous Integration

Tests and linting are executed through GitHub Actions.

The CI pipeline tests the project against:

```text
Python 3.10
Python 3.11
Python 3.12
```

The CI environment uses `uv` to install and synchronize dependencies.

The pipeline runs:

```bash
uv sync
uv run pytest -q
uv run flake8 app tests
```

Linting failures cause the CI job to fail.

## VSCU Environment

The production/sandbox integration requires the appropriate KRA VSCU software and environment.

The VSCU application is not included in this repository.

The official KRA VSCU package and sandbox access must be obtained through KRA's eTIMS integration/onboarding process.

This repository therefore contains the taxpayer-side integration application, not the KRA VSCU application itself.

## Security

The integrator will eventually handle sensitive eTIMS information and cryptographic material.

Security considerations include:

- Never commit credentials or cryptographic keys
- Store secrets outside source control
- Protect VSCU communication
- Validate incoming data
- Validate VSCU responses
- Log useful diagnostic information without exposing secrets
- Implement appropriate authentication for business-system clients
- Maintain audit information for eTIMS transactions

## Development Roadmap

### Phase 1 — Foundation

- [x] FastAPI application
- [x] VSCU HTTP client
- [x] Environment configuration
- [x] Pydantic request/response models
- [x] Device initialization
- [x] Automated tests
- [x] Flake8 compliance
- [x] uv dependency management
- [x] GitHub Actions CI

### Phase 2 — Master Data

- [ ] Code synchronization
- [ ] Item classification
- [ ] Branch information
- [ ] Customer information
- [ ] Notices
- [ ] Item registration

### Phase 3 — Transactions

- [ ] Sales transaction
- [ ] Sales invoice
- [ ] Purchase transactions
- [ ] Imported items

### Phase 4 — Inventory

- [ ] Stock master
- [ ] Stock in/out
- [ ] Stock inventory

### Phase 5 — Reliability

- [ ] Database persistence
- [ ] Transaction state management
- [ ] Idempotency
- [ ] Retry mechanism
- [ ] Error handling
- [ ] Reconciliation
- [ ] Structured logging
- [ ] Monitoring

### Phase 6 — Production Readiness

- [ ] Security hardening
- [ ] Containerization
- [ ] Deployment configuration
- [ ] Sandbox integration testing
- [ ] KRA certification preparation

## Related KRA Documentation

The implementation follows the KRA eTIMS system-to-system integration documentation and the applicable VSCU technical specification.

Refer to the official KRA eTIMS documentation for the current integration requirements, sandbox process, and certification requirements.

## License

This project is intended for development and integration work with the KRA eTIMS system. Licensing and distribution terms should be established before production or commercial distribution.