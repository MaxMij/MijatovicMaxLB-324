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
