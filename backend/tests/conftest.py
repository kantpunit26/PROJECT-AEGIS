import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_db
from app.core.database import SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Initializes schema and seeds baseline dataset before running tests."""
    init_db()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
