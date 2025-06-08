from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_post():
    response = client.post("/convert", files={"file": ("dummy.step", b"solid content")})
    assert response.status_code == 200
