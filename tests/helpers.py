"""Small test helpers. GET a real form, then POST its CSRF token."""
import html
import re
BASE = "https://localhost"
PASSWORD = "Learning-Portal-2026!"

def get(client, path):
    return client.get(path, base_url=BASE)

def token(client, path):
    page = get(client, path).get_data(as_text=True)
    match = re.search(r'name="csrf_token" value="([^"]+)"', page)
    return html.unescape(match.group(1)) if match else ""

def post(client, path, data=None, form_path=None, with_token=True):
    fields = dict(data or {})
    if with_token:
        fields["csrf_token"] = token(client, form_path or path)
    return client.post(path, data=fields, base_url=BASE,
                       headers={"Referer": BASE + (form_path or path)})

def login(client, username="alice", password=PASSWORD):
    return post(client, "/login", {"username": username, "password": password})
