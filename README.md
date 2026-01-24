# Social Media App

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-pytest-ED8B00?style=for-the-badge&logo=pytest&logoColor=white)
[![License](https://img.shields.io/badge/License-MIT-999999?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)



A modern social media application built with **FastAPI**, using **async**, **Pydantic**, **databases**, and **JWT-based authorization**.

This project is based on code from [PacktPublishing/Mastering-REST-APIs-with-FastAPI](https://github.com/PacktPublishing/Mastering-REST-APIs-with-FastAPI) (MIT License) and course Mastering REST APIs with FastAPI by PacktPublishing

All modifications and additional features are made by Gossu386.

See license details in the [LICENSE](LICENSE) file.
---

## Features

- User registration, login, and authentication
- CRUD operations for posts and comments
- Async database interactions for high performance
- Pydantic models for strict data validation
- Unit and integration tests using **pytest**
- JWT-based authentication and role-based authorization
- Modular and scalable FastAPI architecture

---

## Tech Stack

| Component | Description |
|-----------|-------------|
| **FastAPI** | Web framework for building APIs |
| **Uvicorn** | ASGI server for running FastAPI apps |
| **SQLAlchemy** | ORM for database interactions |
| **Databases (aiosqlite)** | Async database access layer |
| **Pydantic / pydantic-settings** | Data validation and app configuration |
| **python-dotenv** | Load environment variables from `.env` files |
| **python-jose** | JWT token creation and verification |
| **passlib[bcrypt] / bcrypt** | Password hashing and verification |
| **python-multipart** | Handle file uploads |
| **rich** | Pretty console output and logging |
| **asgi-correlation-id** | Track requests via correlation IDs |
| **python-json-logger** | JSON-formatted logging |
| **logtail-python** | Optional log shipping |

### Development / Testing

| Component | Description |
|-----------|-------------|
| **pytest** | Testing framework |
| **pytest-mock** | Mocking for tests |
| **httpx** | Async HTTP client for testing endpoints |
| **anyio** | Async concurrency backend for tests |
| **black** | Code formatting |
| **isort** | Sort imports |
| **ruff** | Linting |



