"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.

Using AAA (Arrange-Act-Assert) pattern for clarity.
"""
import pytest


class TestUnregister:
    """Test suite for activity unregistration/deletion."""

    def test_unregister_success(self, client, mock_activities, test_activity_name):
        """
        Test: Student successfully unregisters from an activity.
        
        Arrange: Client, mocked activities, and test activity with a known participant.
        Act: DELETE request to remove the known participant.
        Assert: Response status is 200 and participant is removed from activity.
        """
        # Arrange
        email_to_remove = mock_activities[test_activity_name]["participants"][0]
        initial_count = len(mock_activities[test_activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{test_activity_name}/signup",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        assert email_to_remove not in mock_activities[test_activity_name]["participants"]
        assert len(mock_activities[test_activity_name]["participants"]) == initial_count - 1
        data = response.json()
        assert "Removed" in data["message"]

    def test_unregister_nonexistent_activity(self, client, mock_activities, test_email):
        """
        Test: Unregister fails when activity does not exist.
        
        Arrange: Client, mocked activities, and test email.
        Act: DELETE request with nonexistent activity name.
        Assert: Response status is 404 and error detail is clear.
        """
        # Arrange
        nonexistent_activity = "Nonexistent Club"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_nonexistent_participant(self, client, mock_activities, test_activity_name, test_email):
        """
        Test: Unregister fails when participant is not in the activity.
        
        Arrange: Client, mocked activities, and test email not in any activity.
        Act: DELETE request with email not in the activity.
        Assert: Response status is 404 and error detail indicates participant not found.
        """
        # Arrange is implicit via fixtures

        # Act
        response = client.delete(
            f"/activities/{test_activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_unregister_keeps_other_participants(self, client, mock_activities):
        """
        Test: Unregistering one student doesn't affect other participants.
        
        Arrange: Client and mocked activities with multiple participants in Chess Club.
        Act: Sign up a second student, then remove the first participant.
        Assert: Second student remains in the activity.
        """
        # Arrange
        activity = "Chess Club"
        original_participant = mock_activities[activity]["participants"][0]
        new_email = "newparticipant@mergington.edu"
        
        # First, add a new participant
        client.post(
            f"/activities/{activity}/signup",
            params={"email": new_email}
        )
        
        # Act: Remove the original participant
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": original_participant}
        )

        # Assert
        assert response.status_code == 200
        assert original_participant not in mock_activities[activity]["participants"]
        assert new_email in mock_activities[activity]["participants"]
