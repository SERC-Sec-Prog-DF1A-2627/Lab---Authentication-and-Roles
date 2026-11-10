"""Run with: python -m pytest -q tests/test_auth.py"""
from app import app, get_db, ph, hash_password
from tests.helpers import get, post, login, PASSWORD

def test_registration_stores_argon2_and_assigns_student(client):
    response = post(client, "/register", {"username":"charlie", "password":PASSWORD, "role":"admin"})
    assert response.status_code == 302
    with app.app_context():
        row = get_db().execute("SELECT * FROM users WHERE username = ?", ("charlie",)).fetchone()
        assert row["role"] == "student"
        assert row["password_hash"].startswith("$argon2id$")
        assert row["password_hash"] != PASSWORD
        assert ph.verify(row["password_hash"], PASSWORD)

def test_same_password_uses_different_salts(client):
    assert hash_password(PASSWORD) != hash_password(PASSWORD)

def test_duplicate_username(client):
    assert post(client, "/register", {"username":"alice", "password":PASSWORD}).status_code == 409

def test_invalid_registration(client):
    assert post(client, "/register", {"username":"x", "password":"short"}).status_code == 400

def test_login_success(client):
    assert login(client).status_code == 302
    assert b"alice" in get(client, "/account").data

def test_login_failure_is_generic(client):
    wrong = login(client, "alice", "not-the-password")
    unknown = login(client, "nobody", "not-the-password")
    assert wrong.status_code == unknown.status_code == 401
    assert b"Invalid username or password." in wrong.data
    assert b"Invalid username or password." in unknown.data

def test_anonymous_account_redirects(client):
    assert get(client, "/account").status_code == 302
