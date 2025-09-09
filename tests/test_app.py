import os
from fastapi.testclient import TestClient
from application import app

os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code in (200)