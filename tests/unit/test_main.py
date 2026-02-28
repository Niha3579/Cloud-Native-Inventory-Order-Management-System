from fastapi.testclient import TestClient
from src.app import app

# Create a TestClient instance using your FastAPI app
client = TestClient(app)

def test_read_main():
    """
    Test the root endpoint to ensure the API is up and running.
    """
    response = client.get("/")
    
    # Assert that the HTTP status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the JSON response matches what we expect
    assert response.json() == {"message": "Inventory System Running"}