from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.models import User

import pytest

def test_dashboard_anonymous(client):
    url = reverse("dashboard")
    response = client.get(url)
    login_href = b'<a href="/users/accounts/login/">Login</a>'
    sign_up_href = b'<a href="/users/sign_up/">Sign up</a>'

    assert login_href in response.content
    assert sign_up_href in response.content

@pytest.mark.django_db
def test_dashboard_user(client):
    user = User.objects.create_user("user", "user@world.com", "pw")
    user.save()
    url = reverse("dashboard")
    client.login(username="user", password="pw")
    response = client.get(url, follow=True)
    logout_str = b'value="Logout"'
    pw_change_str =b'Change password'

    assert response.status_code == HTTPStatus.OK
    assert b"<title>django-bootstrap5 template title</title>" in response.content

    assert logout_str in response.content
    assert pw_change_str in response.content
