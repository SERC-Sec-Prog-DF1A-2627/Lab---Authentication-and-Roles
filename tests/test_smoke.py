from tests.helpers import get

def test_home_and_login_render(client):
    assert get(client, "/").status_code == 200
    assert get(client, "/login").status_code == 200
