import pytest

from app import app, entries
import app as app_module


@pytest.fixture()
def anonymous_client(monkeypatch):
    monkeypatch.setitem(app.config, "TESTING", True)
    monkeypatch.setitem(app.config, "SECRET_KEY", "isolated-test-key")
    monkeypatch.setitem(app.config, "PASSWORD", "test-password")
    monkeypatch.setitem(app.config, "SESSION_COOKIE_SECURE", False)
    entries.clear()
    with app.test_client() as test_client:
        yield test_client
    entries.clear()


@pytest.fixture()
def client(anonymous_client):
    response = anonymous_client.post("/login", data={"password": "test-password"})
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    return anonymous_client


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

    # Entries are stored in the prototype's in-memory list.
    entry = entries[0]
    assert entry is not None
    assert entry.content == "Test Entry Content"
    assert entry.happiness == "😃"


def test_anonymous_user_cannot_add_entry(anonymous_client):
    response = anonymous_client.post(
        "/add_entry", data={"content": "Unbefugter Eintrag", "happiness": "😃"}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"
    assert entries == []


@pytest.mark.parametrize("password", ["incorrect", ""])
def test_wrong_password_does_not_authenticate(anonymous_client, password):
    response = anonymous_client.post("/login", data={"password": password})
    assert "Falsches Passwort" in response.get_data(as_text=True)
    with anonymous_client.session_transaction() as login_session:
        assert not login_session.get("logged_in")


@pytest.mark.parametrize("configured_password", [None, ""])
def test_missing_configuration_cannot_authenticate(
    anonymous_client, monkeypatch, configured_password
):
    monkeypatch.setitem(app.config, "PASSWORD", configured_password)
    anonymous_client.post("/login", data={})
    with anonymous_client.session_transaction() as login_session:
        assert not login_session.get("logged_in")


def test_unicode_password(client, monkeypatch):
    monkeypatch.setitem(app.config, "PASSWORD", "Grüezi😃")
    client.post("/logout")
    response = client.post("/login", data={"password": "Grüezi😃"})
    assert response.headers["Location"] == "/"
    with client.session_transaction() as login_session:
        assert login_session["logged_in"] is True


def test_logout_removes_write_access(client):
    assert client.post("/logout").headers["Location"] == "/"
    response = client.post("/add_entry", data={"content": "Nach Abmeldung"})
    assert response.headers["Location"] == "/login"
    assert entries == []


@pytest.mark.parametrize("content", ["", "   \n ", "x" * 5001])
def test_invalid_content_is_rejected(client, content):
    response = client.post("/add_entry", data={"content": content})
    assert response.headers["Location"] == "/"
    assert entries == []


@pytest.mark.parametrize("character", ["x", "😃"])
def test_maximum_length_entry_is_accepted(client, character):
    client.post("/add_entry", data={"content": character * 5000})
    assert len(entries[0].content) == 5000


def test_invalid_happiness_is_rejected(client):
    client.post("/add_entry", data={"content": "Test", "happiness": "invalid"})
    assert entries == []


@pytest.mark.parametrize("happiness", ["😃", "😐", "😞"])
def test_happiness_is_rendered(client, happiness):
    client.post("/add_entry", data={"content": "Mein Tag", "happiness": happiness})
    html = client.get("/").get_data(as_text=True)
    assert "Mein Tag" in html
    assert happiness in html
    assert entries[0].timestamp is not None


def test_entry_text_is_escaped_and_hidden_after_logout(client):
    client.post("/add_entry", data={"content": "<script>alert('x')</script>"})
    html = client.get("/").get_data(as_text=True)
    assert "&lt;script&gt;" in html
    assert "<script>" not in html
    client.post("/logout")
    html = client.get("/").get_data(as_text=True)
    assert "alert" not in html
    assert "Bitte anmelden" in html


def test_http_methods_and_request_limit(client):
    assert client.get("/add_entry").status_code == 405
    assert client.get("/logout").status_code == 405
    assert client.post("/add_entry", data={"content": "x" * 70000}).status_code == 413


def test_health_reports_revision_without_revealing_entries(
    anonymous_client, monkeypatch
):
    monkeypatch.setattr(app_module, "BUILD_REVISION", "tested-commit")
    response = anonymous_client.get("/healthz")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "revision": "tested-commit"}
