"""Each test gets a fresh DB. No browser or running Flask server is needed."""
import os
import pytest
os.environ["LAB_HTTPS"] = "1"  # Exercise the HTTPS cookie configuration.
from app import app, init_db

@pytest.fixture
def client(tmp_path):
    original = app.config.copy()
    app.config.update(TESTING=True, DATABASE=str(tmp_path / "test.sqlite"))
    with app.app_context():
        init_db()
    # Do not preserve request contexts across separate simulated browsers.
    yield app.test_client()
    app.config.clear()
    app.config.update(original)

@pytest.fixture
def clock():
    # Tests advance this list's value. No real sleeping or clock changes.
    now = [1000.0]
    old = app.config.get("NOW")
    app.config["NOW"] = lambda: now[0]
    yield now
    app.config["NOW"] = old
