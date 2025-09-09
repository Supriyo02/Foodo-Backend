import os
from fastapi.testclient import TestClient
from application import app

os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_db")

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/health")
    assert response.status_code == 200