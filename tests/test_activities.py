"""
Tests for the GET /activities endpoint.

Using AAA (Arrange-Act-Assert) pattern for clarity.
"""
import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client, mock_activities):
        """
        Test: GET /activities returns all activities in the database.
        
        Arrange: Client and mocked activities are provided by fixtures.
        Act: Send GET request to /activities endpoint.
        Assert: Response status is 200 and contains all activities.
        """
        # Arrange is implicit via fixtures

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_returns_correct_structure(self, client, mock_activities):
        """
        Test: Each activity has the required fields.
        
        Arrange: Client and mocked activities are provided by fixtures.
        Act: Send GET request to /activities endpoint.
        Assert: Each activity has description, schedule, max_participants, and participants.
        """
        # Arrange is implicit via fixtures

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)

    def test_get_activities_includes_participants(self, client, mock_activities):
        """
        Test: Activity details include current participants.
        
        Arrange: Client and mocked activities with known participants.
        Act: Send GET request to /activities endpoint.
        Assert: Activities show correct participant lists.
        """
        # Arrange is implicit via fixtures

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "emma@mergington.edu" in data["Programming Class"]["participants"]
        assert len(data["Gym Class"]["participants"]) == 0
