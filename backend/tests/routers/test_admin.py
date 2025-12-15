from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app
from backend.dependencies import get_current_user

# Mock auth dependency to bypass check
app.dependency_overrides[get_current_user] = lambda: MagicMock(id="test-user")

client = TestClient(app)

@patch("backend.routers.admin.ScraperService")
@patch("backend.routers.admin.IngestionService")
def test_scrape_endpoint(mock_ingest, mock_scraper):
    # Setup mocks
    mock_scraper_instance = mock_scraper.return_value
    mock_scraper_instance.scrape_url.return_value = [{"title": "Test", "content": "Content"}]
    
    mock_ingest_instance = mock_ingest.return_value
    mock_ingest_instance.process_and_store.return_value = {"status": "success", "chunks": 5}

    # Test
    response = client.post(
        "/api/admin/scrape",
        json={"url": "https://www.himolde.no/test"}
    )
    
    # Verify
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Scraping and ingestion triggered", "details": {"status": "success", "chunks": 5}}

@patch("backend.routers.admin.settings")
def test_scrape_endpoint_invalid_url(mock_settings):
    response = client.post(
        "/api/admin/scrape",
        json={"url": "https://google.com"} # Not himolde.no
    )
    assert "himolde.no" in str(response.json()["detail"])

# Need to mock Supabase for GET /urls if we are querying DB
@patch("backend.routers.admin.create_client")
def test_get_urls(mock_create_client):
    # Mock Supabase response
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    
    mock_response = MagicMock()
    mock_response.data = [
        {"url": "https://www.himolde.no/1", "title": "Page 1", "metadata": {"scraped_at": "2025-01-01"}},
        {"url": "https://www.himolde.no/2", "title": "Page 2", "metadata": {"scraped_at": "2025-01-02"}}
    ]
    
    # Chain: table().select().order().execute()
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = mock_response

    response = client.get("/api/admin/urls")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["url"] == "https://www.himolde.no/1"

# User Management Tests
@patch("backend.routers.admin.create_client")
def test_list_users(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    
    # Mock user as a simple object or dict that mimics the structure
    # Since we just return the list, a dict is safest for JSON serialization in tests
    mock_user = {"id": "123", "email": "test@example.com", "created_at": "2023-01-01T00:00:00Z"}
    
    # Mock response object
    mock_response = MagicMock()
    mock_response.users = [mock_user]
    mock_supabase.auth.admin.list_users.return_value = mock_response

    response = client.get("/api/admin/users")
    assert response.status_code == 200
    assert response.json()[0]["email"] == "test@example.com"

@patch("backend.routers.admin.create_client")
def test_create_user(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    
    mock_user_inner = MagicMock()
    mock_user_inner.id = "new-id"
    mock_user_inner.email = "new@example.com"
    
    mock_response = MagicMock()
    mock_response.user = mock_user_inner
    
    mock_supabase.auth.admin.create_user.return_value = mock_response
    
    response = client.post(
        "/api/admin/users",
        json={"email": "new@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == "new-id"

@patch("backend.routers.admin.create_client")
def test_delete_user(mock_create_client):
    mock_supabase = MagicMock()
    mock_create_client.return_value = mock_supabase
    
    response = client.delete("/api/admin/users/123")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_supabase.auth.admin.delete_user.assert_called_with("123")
