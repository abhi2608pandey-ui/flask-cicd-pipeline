import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_success(client):
    """Health endpoint should return HTTP 200."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["service"] == "student-registration"


@patch("app.mongo")
def test_home_page_success(mock_mongo, client):
    """Home page should successfully return student records."""
    mock_mongo.db.students.find.return_value = [
        {
            "_id": ObjectId(),
            "name": "Test Student",
            "email": "test@example.com",
            "course": "Python"
        }
    ]

    response = client.get("/")

    assert response.status_code == 200


@patch("app.mongo")
def test_add_student_success(mock_mongo, client):
    """Adding a student should redirect to the home page."""
    response = client.post(
        "/add",
        data={
            "name": "John Doe",
            "email": "john@example.com",
            "course": "Python"
        }
    )

    assert response.status_code == 302
    mock_mongo.db.students.insert_one.assert_called_once()


@patch("app.mongo")
def test_update_student_success(mock_mongo, client):
    """Updating a student should redirect to the home page."""
    student_id = str(ObjectId())

    mock_mongo.db.students.find_one.return_value = {
        "_id": ObjectId(student_id),
        "name": "John Doe",
        "email": "john@example.com",
        "course": "Python"
    }

    response = client.post(
        f"/update/{student_id}",
        data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "course": "DevOps"
        }
    )

    assert response.status_code == 302
    mock_mongo.db.students.update_one.assert_called_once()


@patch("app.mongo")
def test_delete_student_success(mock_mongo, client):
    """Deleting an existing student should redirect."""
    student_id = str(ObjectId())

    mock_result = MagicMock()
    mock_result.deleted_count = 1

    mock_mongo.db.students.delete_one.return_value = mock_result

    response = client.get(f"/delete/{student_id}")

    assert response.status_code == 302
    mock_mongo.db.students.delete_one.assert_called_once()


def test_update_invalid_student_id(client):
    """Invalid student IDs should return 404."""
    response = client.get("/update/not-a-valid-id")

    assert response.status_code == 404


def test_delete_invalid_student_id(client):
    """Invalid student IDs should return 404."""
    response = client.get("/delete/not-a-valid-id")

    assert response.status_code == 404