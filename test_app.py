import pytest

from app import app, entries


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    entries.clear()
    with app.test_client() as test_client:
        yield test_client
    entries.clear()


def test_add_entry(client):
    response = client.post("/add_entry", data={"content": "Test Entry Content"})

    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    entry = entries[0]
    assert entry is not None
    assert entry.content == "Test Entry Content"


def test_add_entry_with_happiness(client):
    # Test adding an entry with happiness
    response = client.post(
        "/add_entry", data={"content": "Test Entry Content", "happiness": "😃"}
    )

    # Check if the response is a redirect to the index page
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    # Check if the entry was added to the database with the correct happiness
    entry = entries[0]
    assert entry is not None
    assert entry.content == "Test Entry Content"
    assert entry.happiness == "😃"
