"""Observe behaviour using Flask's test client and a disposable DB.
Run: python demo_probe.py
This makes no network requests and never prints cookie values.
"""
import tempfile
from pathlib import Path
from app import app, init_db
from tests.helpers import get, login, post

original = app.config.copy()
with tempfile.TemporaryDirectory() as directory:
    now = [1000.0]
    app.config.update(TESTING=True, DATABASE=str(Path(directory) / "demo.sqlite"), NOW=lambda: now[0])
    with app.app_context():
        init_db()
    browser = app.test_client()
    print("Login:", login(browser).status_code)
    print("Alice requests /staff:", get(browser, "/staff").status_code)
    if any(rule.rule.startswith("/feedback/") for rule in app.url_map.iter_rules()):
        print("Alice reads her own record:", get(browser, "/feedback/1").status_code)
        print("Alice reads Bob's record:", get(browser, "/feedback/2").status_code)
        print("Update without CSRF token:", post(browser, "/feedback/1", {"student_note":"Probe"}, with_token=False).status_code)
        copied_cookie = browser.get_cookie(app.config["SESSION_COOKIE_NAME"]).value
        print("POST logout:", post(browser, "/logout", form_path="/account").status_code)
        replay = app.test_client()
        replay.set_cookie(app.config["SESSION_COOKIE_NAME"], copied_cookie)
        print("Copied cookie after logout, /account:", get(replay, "/account").status_code)
        login(browser)
        now[0] += 301
        print("Session idle for 301 seconds, /account:", get(browser, "/account").status_code)
    else:
        print("Alice requests /admin:", get(browser, "/admin").status_code)
app.config.clear()
app.config.update(original)
