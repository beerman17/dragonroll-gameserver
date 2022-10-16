import pytest
from starlette.testclient import TestClient

from app.main import app
from app.database import Session


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='module')
def test_db_connection():
    db = Session()
    yield db
