"""
Pytest configuration and shared fixtures for API tests.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for making requests to the API.
    
    Each test gets a fresh client instance.
    """
    return TestClient(app)


@pytest.fixture
def mock_activities(monkeypatch):
    """
    Fixture: Provides a fresh, isolated activities data for each test.
    
    Patches the app.activities with a clean copy to prevent test pollution.
    """
    from src import app as app_module
    
    fresh_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }
    
    # Patch the app's activities dict with our fresh copy
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    return fresh_activities


@pytest.fixture
def test_email():
    """Fixture: Provides a test email for signup operations."""
    return "newstudent@mergington.edu"


@pytest.fixture
def test_activity_name():
    """Fixture: Provides a test activity name."""
    return "Programming Class"
