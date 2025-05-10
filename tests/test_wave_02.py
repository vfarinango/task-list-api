import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "task": {
                "id": 2,
                "title": "Answer forgotten email 📧",
                "description": "",
                "is_complete": False}
        },
        {
            "task": {
                "id": 3,
                "title": "Pay my outstanding tickets 😭",
                "description": "",
                "is_complete": False}
        },
        {
            "task": {
                "id": 1,
                "title": "Water the garden 🌷",
                "description": "",
                "is_complete": False}
        }
    ]


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "task": {
                "description": "",
                "id": 1,
                "is_complete": False,
                "title": "Water the garden 🌷"}
        },
        {
            "task": {
                "description": "",
                "id": 3,
                "is_complete": False,
                "title": "Pay my outstanding tickets 😭"}
        },
        {
            "task": {
                "description": "",
                "id": 2,
                "is_complete": False,
                "title": "Answer forgotten email 📧"}
        }
    ]
