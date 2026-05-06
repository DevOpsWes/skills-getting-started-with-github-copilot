"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Using AAA (Arrange-Act-Assert) pattern for clarity.
"""
import pytest


class TestSignup:
    """Test suite for activity signup."""

    def test_signup_success(self, client, mock_activities, test_email, test_activity_name):
        """
        Test: Student successfully signs up for an activity.
        
        Arrange: Client, mocked activities, and test email are provided by fixtures.
        Act: POST request to signup endpoint with valid activity and email.
        Assert: Response status is 200 and participant is added to activity.
        """
        # Arrange is implicit via fixtures

        # Act
        response = client.post(
            f"/activities/{test_activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        assert test_email in mock_activities[test_activity_name]["participants"]
        data = response.json()
        assert "Signed up" in data["message"]
        assert test_email in data["message"]

    def test_signup_nonexistent_activity(self, client, mock_activities, test_email):
        """
        Test: Signup fails when activity does not exist.
        
        Arrange: Client, mocked activities, and test email are provided by fixtures.
        Act: POST request to signup endpoint with nonexistent activity name.
        Assert: Response status is 404 and error detail is clear.
        """
        # Arrange is implicit via fixtures
        nonexistent_activity = "Nonexistent Club"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email_fails(self, client, mock_activities, test_activity_name):
        """
        Test: Student cannot sign up twice for the same activity.
        
        Arrange: Client, mocked activities, and test activity with existing participant.
        Act: Try to POST signup with an email already in the activity's participants.
        Assert: Response status is 400 and error detail indicates duplicate signup.
        """
        # Arrange
        existing_email = mock_activities[test_activity_name]["participants"][0]

        # Act
        response = client.post(
            f"/activities/{test_activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_multiple_students(self, client, mock_activities, test_activity_name):
        """
        Test: Multiple different students can sign up for the same activity.
        
        Arrange: Client and mocked activities.
        Act: Sign up two different students for the same activity.
        Assert: Both students are in the participants list.
        """
        # Arrange
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{test_activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{test_activity_name}/signup",
            params={"email": email2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in mock_activities[test_activity_name]["participants"]
        assert email2 in mock_activities[test_activity_name]["participants"]
