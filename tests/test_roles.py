import pytest
from tests.helpers import get, login

@pytest.mark.parametrize("user,path,expected", [
    ("alice", "/staff", 403), ("alice", "/admin", 403),
    ("sam", "/staff", 200), ("sam", "/admin", 403),
    ("ada", "/admin", 200), ("ada", "/staff", 403),
])
def test_role_matrix(client, user, path, expected):
    assert login(client, user).status_code == 302
    assert get(client, path).status_code == expected

def test_anonymous_staff_redirects(client):
    assert get(client, "/staff").status_code == 302
